from pathlib import Path
import re
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, object_session

from ..database import get_db
from ..models.settings import BusinessSetting, CompanyEnvironment
from ..routers.auth import _get_user_from_token, bearer_scheme
from ..schemas.settings import BusinessSettingResponse, CompanyEnvironmentResponse

router = APIRouter(prefix="/settings", tags=["Settings"])

BACKEND_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BACKEND_DIR / "uploads" / "business"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _get_or_create_business_settings(db: Session) -> BusinessSetting:
    settings = db.query(BusinessSetting).first()
    if settings:
        return settings

    settings = BusinessSetting(
        business_name="Orange Tec",
        legal_name="Orange Tec",
        trade_name="Orange Tec",
        app_title="Orange Tec ERP",
        sidebar_subtitle="ERP Empresarial",
        address="",
        ruc="",
        phone="",
        phones="",
        email="",
        website="",
        theme_code="default",
        sales_interface_code="ropa",
        pricing_currency="CS",
    )
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


def _save_upload(file: UploadFile | None, current_path: str | None) -> str | None:
    if not file or not file.filename:
        return current_path

    extension = Path(file.filename).suffix.lower() or ".png"
    filename = f"{uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename
    destination.write_bytes(file.file.read())

    if current_path:
        relative_parts = current_path.removeprefix("/media/").split("/")
        old_file = BACKEND_DIR / "uploads" / Path(*relative_parts[1:])
        if old_file.exists() and old_file.is_file():
            try:
                old_file.unlink()
            except OSError:
                pass

    return f"/media/business/{filename}"


def _serialize(settings: BusinessSetting) -> dict:
    return {
        "id": settings.id,
        "business_name": settings.trade_name or settings.business_name,
        "legal_name": settings.legal_name,
        "trade_name": settings.trade_name or settings.business_name,
        "app_title": settings.app_title or f"{(settings.trade_name or settings.business_name or 'ERP')} ERP",
        "sidebar_subtitle": settings.sidebar_subtitle or "ERP Empresarial",
        "address": settings.address,
        "ruc": settings.ruc,
        "phone": settings.phone,
        "phones": settings.phones,
        "email": settings.email,
        "website": settings.website,
        "theme_code": settings.theme_code or "default",
        "sales_interface_code": settings.sales_interface_code or "ropa",
        "pricing_currency": settings.pricing_currency or "CS",
        "logo_login": settings.logo_login,
        "logo_sidebar": settings.logo_sidebar,
        "logo_invoice": settings.logo_invoice,
        "logo_favicon": settings.logo_favicon,
        "inventory_cs_only": bool(settings.inventory_cs_only),
        "weighted_inventory_enabled": bool(settings.weighted_inventory_enabled),
        "weighted_sales_enabled": bool(settings.weighted_sales_enabled),
        "recipe_explosion_on_ingreso": bool(settings.recipe_explosion_on_ingreso),
        "multi_branch_enabled": bool(settings.multi_branch_enabled),
        "price_auto_from_cost_enabled": bool(settings.price_auto_from_cost_enabled),
        "price_margin_percent": int(settings.price_margin_percent or 0),
        "environments": [
            {
                "id": row.id,
                "company_key": row.company_key,
                "company_name": row.company_name,
                "database_url": row.database_url,
                "is_active": bool(row.is_active),
            }
            for row in sorted(
                db_settings_environments(settings),
                key=lambda item: (not bool(item.is_active), item.company_name.lower()),
            )
        ],
    }


def db_settings_environments(_settings: BusinessSetting) -> list[CompanyEnvironment]:
    session = object_session(_settings)
    return list(session.query(CompanyEnvironment).all()) if session else []


def _to_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "on", "yes", "si"}


def _validate_company_key(value: str) -> str:
    key = (value or "").strip().lower()
    if not re.fullmatch(r"[a-z0-9_]+", key):
        raise HTTPException(status_code=400, detail="La clave de empresa solo admite letras, numeros y guion bajo")
    return key


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    return _get_user_from_token(credentials, db)


@router.get("/business/public", response_model=BusinessSettingResponse)
def get_business_settings_public(db: Session = Depends(get_db)):
    settings = _get_or_create_business_settings(db)
    return _serialize(settings)


@router.get("/business", response_model=BusinessSettingResponse)
def get_business_settings(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    settings = _get_or_create_business_settings(db)
    return _serialize(settings)


@router.put("/business", response_model=BusinessSettingResponse)
def update_business_settings(
    business_name: str = Form(...),
    legal_name: str | None = Form(None),
    trade_name: str | None = Form(None),
    app_title: str | None = Form(None),
    sidebar_subtitle: str | None = Form(None),
    address: str | None = Form(None),
    ruc: str | None = Form(None),
    phone: str | None = Form(None),
    phones: str | None = Form(None),
    email: str | None = Form(None),
    website: str | None = Form(None),
    theme_code: str | None = Form(None),
    sales_interface_code: str | None = Form(None),
    pricing_currency: str | None = Form(None),
    inventory_cs_only: str | None = Form(None),
    weighted_inventory_enabled: str | None = Form(None),
    weighted_sales_enabled: str | None = Form(None),
    recipe_explosion_on_ingreso: str | None = Form(None),
    multi_branch_enabled: str | None = Form(None),
    price_auto_from_cost_enabled: str | None = Form(None),
    price_margin_percent: int | None = Form(None),
    logo_login: UploadFile | None = File(None),
    logo_sidebar: UploadFile | None = File(None),
    logo_invoice: UploadFile | None = File(None),
    logo_favicon: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    settings = _get_or_create_business_settings(db)

    trade_name_value = (trade_name or business_name or "").strip() or "Orange Tec"
    settings.business_name = trade_name_value
    settings.trade_name = trade_name_value
    settings.legal_name = (legal_name or "").strip() or trade_name_value
    settings.app_title = (app_title or "").strip() or f"{trade_name_value} ERP"
    settings.sidebar_subtitle = (sidebar_subtitle or "").strip() or "ERP Empresarial"
    settings.address = (address or "").strip()
    settings.ruc = (ruc or "").strip()
    settings.phone = (phone or "").strip()
    settings.phones = (phones or "").strip()
    settings.email = (email or "").strip()
    settings.website = (website or "").strip()
    settings.theme_code = (theme_code or "default").strip() or "default"
    settings.sales_interface_code = (sales_interface_code or "ropa").strip().lower() or "ropa"
    currency_value = (pricing_currency or "CS").strip().upper() or "CS"
    settings.pricing_currency = "USD" if currency_value == "USD" else "CS"
    settings.inventory_cs_only = _to_bool(inventory_cs_only)
    settings.weighted_inventory_enabled = _to_bool(weighted_inventory_enabled)
    settings.weighted_sales_enabled = _to_bool(weighted_sales_enabled)
    settings.recipe_explosion_on_ingreso = _to_bool(recipe_explosion_on_ingreso)
    settings.multi_branch_enabled = _to_bool(multi_branch_enabled)
    settings.price_auto_from_cost_enabled = _to_bool(price_auto_from_cost_enabled)
    settings.price_margin_percent = max(int(price_margin_percent or 0), 0)
    settings.logo_login = _save_upload(logo_login, settings.logo_login)
    settings.logo_sidebar = _save_upload(logo_sidebar, settings.logo_sidebar)
    settings.logo_invoice = _save_upload(logo_invoice, settings.logo_invoice)
    settings.logo_favicon = _save_upload(logo_favicon, settings.logo_favicon)

    db.add(settings)
    db.commit()
    db.refresh(settings)
    return _serialize(settings)


@router.get("/environments", response_model=list[CompanyEnvironmentResponse])
def list_environments(
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    return db.query(CompanyEnvironment).order_by(CompanyEnvironment.company_name).all()


@router.post("/environments", response_model=CompanyEnvironmentResponse, status_code=status.HTTP_201_CREATED)
def create_environment(
    company_key: str = Form(...),
    company_name: str = Form(...),
    database_url: str = Form(...),
    activate: str | None = Form(None),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    key = _validate_company_key(company_key)
    exists = db.query(CompanyEnvironment).filter(CompanyEnvironment.company_key == key).first()
    if exists:
        raise HTTPException(status_code=400, detail="La clave de empresa ya existe")

    row = CompanyEnvironment(
        company_key=key,
        company_name=(company_name or "").strip() or key,
        database_url=(database_url or "").strip(),
        is_active=False,
    )
    if not row.database_url:
        raise HTTPException(status_code=400, detail="DATABASE_URL es requerida")
    if _to_bool(activate):
        db.query(CompanyEnvironment).update({CompanyEnvironment.is_active: False})
        row.is_active = True
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/environments/{environment_id}", response_model=CompanyEnvironmentResponse)
def update_environment(
    environment_id: int,
    company_name: str = Form(...),
    database_url: str = Form(...),
    activate: str | None = Form(None),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    row = db.query(CompanyEnvironment).filter(CompanyEnvironment.id == environment_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Entorno no encontrado")
    row.company_name = (company_name or "").strip() or row.company_key
    row.database_url = (database_url or "").strip()
    if not row.database_url:
        raise HTTPException(status_code=400, detail="DATABASE_URL es requerida")
    if _to_bool(activate):
        db.query(CompanyEnvironment).update({CompanyEnvironment.is_active: False})
        row.is_active = True
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.patch("/environments/{environment_id}/activate", response_model=CompanyEnvironmentResponse)
def activate_environment(
    environment_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    row = db.query(CompanyEnvironment).filter(CompanyEnvironment.id == environment_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Entorno no encontrado")
    db.query(CompanyEnvironment).update({CompanyEnvironment.is_active: False})
    row.is_active = True
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
