from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import or_, text

from .core.security import hash_password
from .database import Base, SessionLocal, engine
from .models.inventory import Bodega, EgresoTipo, IngresoTipo, Linea, Marca, Producto, Proveedor, Segmento, UnidadMedida
from .models.settings import BusinessSetting, CompanyEnvironment
from .models.user import Role, User
from .routers import auth, inventory, settings

app = FastAPI(title="ERP System Backend")
BACKEND_DIR = Path(__file__).resolve().parents[1]
UPLOADS_DIR = BACKEND_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(settings.router)
app.mount("/media", StaticFiles(directory=UPLOADS_DIR), name="media")


@app.get("/")
def root():
    return {"message": "API ERP lista"}


@app.get("/sales", include_in_schema=False)
def sales_entry():
    return RedirectResponse(url="http://127.0.0.1:5173/app/sales", status_code=307)


@app.get("/sales/", include_in_schema=False)
def sales_entry_slash():
    return RedirectResponse(url="http://127.0.0.1:5173/app/sales", status_code=307)


def create_initial_admin():
    db = SessionLocal()
    admin_email = "administrador"
    admin_password = "020416"
    admin_name = "Administrador"

    try:
        admin_role = db.query(Role).filter(Role.name == "administrador").first()
        if not admin_role:
            admin_role = Role(name="administrador")
            db.add(admin_role)
            db.flush()

        existing = (
            db.query(User)
            .filter(
                or_(
                    User.email == admin_email,
                    User.email == "admin@erp.com",
                    User.full_name == admin_name,
                )
            )
            .first()
        )

        if not existing:
            existing = User(
                full_name=admin_name,
                email=admin_email,
                hashed_password=hash_password(admin_password),
                is_active=True,
            )
            db.add(existing)
            db.flush()
        else:
            existing.full_name = admin_name
            existing.email = admin_email
            existing.hashed_password = hash_password(admin_password)
            existing.is_active = True

        if admin_role not in existing.roles:
            existing.roles.append(admin_role)

        db.commit()
        db.refresh(existing)
        print(">>> Usuario admin listo (administrador / 020416)")
    finally:
        db.close()


def seed_inventory_catalogs():
    db = SessionLocal()
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS marcas (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(120) UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT NOW()
                    )
                    """
                )
            )
            connection.execute(
                text(
                    """
                    ALTER TABLE productos
                    ADD COLUMN IF NOT EXISTS marca_id INTEGER REFERENCES marcas(id)
                    """
                )
            )
            connection.execute(
                text(
                    """
                    ALTER TABLE productos
                    ADD COLUMN IF NOT EXISTS usa_codigo_barra BOOLEAN DEFAULT FALSE
                    """
                )
            )
            connection.execute(
                text(
                    """
                    ALTER TABLE productos
                    ADD COLUMN IF NOT EXISTS codigo_barra VARCHAR(120)
                    """
                )
            )
            connection.execute(
                text(
                    """
                    ALTER TABLE productos
                    ADD COLUMN IF NOT EXISTS tipo_producto VARCHAR(30) DEFAULT 'DIRECTO'
                    """
                )
            )
            connection.execute(
                text(
                    """
                    CREATE UNIQUE INDEX IF NOT EXISTS ix_productos_codigo_barra
                    ON productos (codigo_barra)
                    WHERE codigo_barra IS NOT NULL
                    """
                )
            )

        if not db.query(Bodega).first():
            db.add(Bodega(code="BOD-001", name="Bodega Principal", activo=True))

        default_lineas = [
            ("LIN-001", "General"),
        ]
        for cod_linea, linea in default_lineas:
            exists = db.query(Linea).filter(Linea.cod_linea == cod_linea).first()
            if not exists:
                db.add(Linea(cod_linea=cod_linea, linea=linea, activo=True))

        default_segmentos = ["General"]
        for nombre in default_segmentos:
            exists = db.query(Segmento).filter(Segmento.segmento == nombre).first()
            if not exists:
                db.add(Segmento(segmento=nombre, activo=True))

        default_units = [
            ("UND", "Unidad", "Und"),
            ("CJ", "Caja", "Cj"),
            ("LB", "Libra", "Lb"),
        ]
        for codigo, nombre, abreviatura in default_units:
            exists = (
                db.query(UnidadMedida)
                .filter(or_(UnidadMedida.codigo == codigo, UnidadMedida.nombre == nombre))
                .first()
            )
            if not exists:
                db.add(UnidadMedida(codigo=codigo, nombre=nombre, abreviatura=abreviatura, activo=True))
            else:
                exists.codigo = codigo
                exists.nombre = nombre
                exists.abreviatura = abreviatura
                exists.activo = True

        existing_product_brands = (
            db.query(Producto.marca)
            .filter(Producto.marca.isnot(None), Producto.marca != "")
            .distinct()
            .all()
        )
        for (brand_name,) in existing_product_brands:
            normalized = (brand_name or "").strip()
            if not normalized:
                continue
            brand = db.query(Marca).filter(Marca.nombre == normalized).first()
            if not brand:
                db.add(Marca(nombre=normalized, activo=True))

        db.flush()

        for product in db.query(Producto).filter(Producto.marca_id.is_(None), Producto.marca.isnot(None), Producto.marca != "").all():
            normalized = (product.marca or "").strip()
            if not normalized:
                continue
            brand = db.query(Marca).filter(Marca.nombre == normalized).first()
            if brand:
                product.marca_id = brand.id

        default_ingresos = [
            ("Inventario Inicial", False),
            ("Compras Locales", True),
            ("Importacion", True),
            ("Ajustes de Inventario", False),
            ("Produccion", False),
            ("Apertura de Pacas", False),
            ("Clasificacion de mermas", False),
            ("Perdidas", False),
        ]
        for nombre, requiere_proveedor in default_ingresos:
            exists = db.query(IngresoTipo).filter(IngresoTipo.nombre == nombre).first()
            if not exists:
                db.add(IngresoTipo(nombre=nombre, requiere_proveedor=requiere_proveedor))

        default_egresos = [
            "Inventario Fisico",
            "Traslado entre bodegas",
            "Merma",
            "Perdida",
            "Reposicion a Cliente",
            "Produccion por receta",
            "Produccion de Abierta",
            "Produccion embalaje",
            "Produccion perdida",
            "Ajuste por Faltante",
        ]
        for nombre in default_egresos:
            exists = db.query(EgresoTipo).filter(EgresoTipo.nombre == nombre).first()
            if not exists:
                db.add(EgresoTipo(nombre=nombre))

        default_proveedores = [
            ("Proveedor Local", "LOCAL"),
            ("Proveedor Extranjero", "EXTRANJERO"),
        ]
        for nombre, tipo in default_proveedores:
            exists = db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
            if not exists:
                db.add(Proveedor(nombre=nombre, tipo=tipo, activo=True))

        db.commit()
    finally:
        db.close()


def seed_business_settings():
    db = SessionLocal()
    try:
        with engine.begin() as connection:
            for statement in [
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS legal_name VARCHAR(180)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS trade_name VARCHAR(180)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS app_title VARCHAR(180)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS sidebar_subtitle VARCHAR(200)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS phone VARCHAR(80)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS email VARCHAR(180)",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS theme_code VARCHAR(60) DEFAULT 'default'",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS sales_interface_code VARCHAR(60) DEFAULT 'ropa'",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS pricing_currency VARCHAR(10) DEFAULT 'CS'",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS inventory_cs_only BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS weighted_inventory_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS weighted_sales_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS recipe_explosion_on_ingreso BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS multi_branch_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS price_auto_from_cost_enabled BOOLEAN DEFAULT FALSE",
                "ALTER TABLE business_settings ADD COLUMN IF NOT EXISTS price_margin_percent INTEGER DEFAULT 0",
            ]:
                connection.execute(text(statement))

        settings = db.query(BusinessSetting).first()
        if not settings:
            db.add(
                BusinessSetting(
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
            )
            db.commit()
            settings = db.query(BusinessSetting).first()
        if settings:
            legacy_interface_map = {
                "sales_ropa": "ropa",
                "sales_zapatos": "zapatos",
                "sales_restaurante": "restaurante",
                "sales_comestibles": "comestibles",
                "sales_utilitario": "ropa",
                "sales_roc": "ropa",
            }
            settings.trade_name = settings.trade_name or settings.business_name or "Orange Tec"
            settings.legal_name = settings.legal_name or settings.trade_name
            settings.app_title = settings.app_title or f"{settings.trade_name} ERP"
            settings.sidebar_subtitle = settings.sidebar_subtitle or "ERP Empresarial"
            settings.theme_code = settings.theme_code or "default"
            normalized_sales_interface = (settings.sales_interface_code or "ropa").strip().lower() or "ropa"
            normalized_sales_interface = legacy_interface_map.get(normalized_sales_interface, normalized_sales_interface)
            if normalized_sales_interface not in {"ropa", "zapatos", "restaurante", "comestibles"}:
                normalized_sales_interface = "ropa"
            settings.sales_interface_code = normalized_sales_interface
            settings.pricing_currency = (settings.pricing_currency or "CS").upper()
            if settings.pricing_currency not in {"CS", "USD"}:
                settings.pricing_currency = "CS"
            settings.phone = settings.phone or ""
            settings.email = settings.email or ""
            db.add(settings)
            db.commit()

        if not db.query(CompanyEnvironment).first():
            db.add(
                CompanyEnvironment(
                    company_key="principal",
                    company_name=(settings.trade_name if settings else "Orange Tec"),
                    database_url=str(engine.url),
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()


create_initial_admin()
seed_inventory_catalogs()
seed_business_settings()
