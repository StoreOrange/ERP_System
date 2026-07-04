import json
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import _get_user_from_token, bearer_scheme

router = APIRouter(prefix="/upgrade", tags=["Upgrade"])

STATE_DIR = Path(os.getenv("UPGRADE_STATE_DIR", "/var/lib/erp-upgrade"))
STATUS_FILE = STATE_DIR / "status.json"
LOG_FILE = STATE_DIR / "upgrade.log"
CHECK_REQUEST_FILE = STATE_DIR / "check.request"
UPGRADE_REQUEST_FILE = STATE_DIR / "upgrade.request"


def _current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    return _get_user_from_token(credentials, db)


def _require_admin(user: User = Depends(_current_user)) -> User:
    role_names = {role.name.lower() for role in user.roles}
    if "administrador" not in role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un administrador puede ejecutar actualizaciones",
        )
    return user


def _read_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _tail_log(lines: int = 80) -> list[str]:
    if not LOG_FILE.exists():
        return []
    try:
        content = LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return content[-lines:]


def _write_request(path: Path, user: User) -> dict:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {
            "requested_at": datetime.now(timezone.utc).isoformat(),
            "requested_by": user.email,
            "requested_by_name": user.full_name,
        }
        path.write_text(json.dumps(payload, ensure_ascii=True), encoding="utf-8")
        return payload
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo escribir la solicitud de actualizacion. Verifica el volumen /var/lib/erp-upgrade.",
        ) from exc


@router.get("/status")
def get_upgrade_status(_user: User = Depends(_require_admin)):
    status_payload = _read_json_file(STATUS_FILE)
    if not status_payload:
        status_payload = {
            "state": "unavailable",
            "label": "Agente no configurado",
            "message": "No hay estado del agente de actualizacion en la VPS.",
            "pending_updates": False,
        }

    status_payload["log_tail"] = _tail_log()
    status_payload["agent_ready"] = STATUS_FILE.exists()
    status_payload["request_pending"] = CHECK_REQUEST_FILE.exists() or UPGRADE_REQUEST_FILE.exists()
    return status_payload


@router.post("/check")
def request_upgrade_check(user: User = Depends(_require_admin)):
    payload = _write_request(CHECK_REQUEST_FILE, user)
    return {
        "message": "Solicitud de verificacion enviada",
        "request": payload,
    }


@router.post("/run")
def request_upgrade_run(user: User = Depends(_require_admin)):
    payload = _write_request(UPGRADE_REQUEST_FILE, user)
    return {
        "message": "Solicitud de actualizacion enviada",
        "request": payload,
    }
