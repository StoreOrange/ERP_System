from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal


class CompanyEnvironmentBase(BaseModel):
    company_key: str
    company_name: str
    database_url: str


class CompanyEnvironmentResponse(CompanyEnvironmentBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class ExchangeRateResponse(BaseModel):
    id: int
    effective_date: date
    period_type: str
    rate: Decimal
    notes: str | None = None
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class BusinessSettingBase(BaseModel):
    business_name: str
    legal_name: str | None = None
    trade_name: str | None = None
    app_title: str | None = None
    sidebar_subtitle: str | None = None
    address: str | None = None
    ruc: str | None = None
    phone: str | None = None
    phones: str | None = None
    email: str | None = None
    website: str | None = None
    theme_code: str | None = "default"
    sales_interface_code: str | None = "ecommerce"
    pricing_currency: str | None = "CS"
    inventory_cs_only: bool = False
    weighted_inventory_enabled: bool = False
    weighted_sales_enabled: bool = False
    recipe_explosion_on_ingreso: bool = False
    multi_branch_enabled: bool = False
    price_auto_from_cost_enabled: bool = False
    price_margin_percent: int = Field(default=0, ge=0)


class BusinessSettingResponse(BusinessSettingBase):
    id: int
    logo_login: str | None = None
    logo_sidebar: str | None = None
    logo_invoice: str | None = None
    logo_favicon: str | None = None
    environments: list[CompanyEnvironmentResponse] = []

    class Config:
        orm_mode = True
