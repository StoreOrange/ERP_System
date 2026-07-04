from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomerBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    identificacion: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None
    activo: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    identificacion: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[str] = None
    tipo: Optional[str] = None
    activo: Optional[bool] = None


class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None


class SalesInvoiceItemCreate(BaseModel):
    producto_id: int
    cantidad: Decimal
    precio_unitario: Decimal
    cod_producto: Optional[str] = None
    descripcion: Optional[str] = None
    unidad: Optional[str] = None
    combo_role: Optional[str] = None
    combo_group: Optional[str] = None


class SalesPaymentCreate(BaseModel):
    forma_codigo: str
    forma_nombre: str
    moneda: str
    monto: Decimal
    banco: Optional[str] = None
    cuenta: Optional[str] = None
    referencia: Optional[str] = None


class SalesInvoiceCreate(BaseModel):
    customer_name: str = "Consumidor final"
    customer_phone: Optional[str] = None
    customer_document: Optional[str] = None
    customer_address: Optional[str] = None
    vendor_name: Optional[str] = None
    bodega_id: int
    fecha: date
    condicion: str = "CONTADO"
    moneda: str = "CS"
    tasa_cambio: Optional[Decimal] = None
    observacion: Optional[str] = None
    usuario_registro: Optional[str] = None
    items: List[SalesInvoiceItemCreate]
    payments: List[SalesPaymentCreate] = Field(default_factory=list)


class SalesInvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    cod_producto: str
    descripcion: str
    unidad: Optional[str] = None
    cantidad: Decimal
    precio_unitario_usd: Decimal
    precio_unitario_cs: Decimal
    subtotal_usd: Decimal
    subtotal_cs: Decimal
    combo_role: Optional[str] = None
    combo_group: Optional[str] = None


class SalesPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    forma_codigo: str
    forma_nombre: str
    moneda: str
    monto: Decimal
    monto_usd: Decimal
    monto_cs: Decimal
    banco: Optional[str] = None
    cuenta: Optional[str] = None
    referencia: Optional[str] = None
    created_at: Optional[datetime] = None


class SalesInvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_number: str
    customer_name: str
    customer_phone: Optional[str] = None
    customer_document: Optional[str] = None
    customer_address: Optional[str] = None
    vendor_name: Optional[str] = None
    bodega_id: int
    egreso_id: Optional[int] = None
    fecha: date
    condicion: str
    moneda: str
    tasa_cambio: Optional[Decimal] = None
    subtotal_usd: Decimal
    subtotal_cs: Decimal
    total_usd: Decimal
    total_cs: Decimal
    paid_usd: Decimal
    paid_cs: Decimal
    balance_usd: Decimal
    balance_cs: Decimal
    change_usd: Decimal
    change_cs: Decimal
    status: str
    observacion: Optional[str] = None
    usuario_registro: Optional[str] = None
    created_at: Optional[datetime] = None
    items: List[SalesInvoiceItemResponse]
    payments: List[SalesPaymentResponse]


class SalesNextInvoiceResponse(BaseModel):
    invoice_number: str


class CashCloseMovementCreate(BaseModel):
    tipo: str
    concepto: str
    monto_cs: Decimal
    referencia: Optional[str] = None


class CashCloseCreate(BaseModel):
    fecha: date
    bodega_id: Optional[int] = None
    efectivo_fisico_cs: Decimal
    observacion: Optional[str] = None
    usuario_registro: Optional[str] = None
    movements: List[CashCloseMovementCreate] = Field(default_factory=list)


class CashCloseMovementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    concepto: str
    monto_cs: Decimal
    referencia: Optional[str] = None
    created_at: Optional[datetime] = None


class CashCloseSummaryResponse(BaseModel):
    fecha: date
    bodega_id: Optional[int] = None
    bodega_name: Optional[str] = None
    invoice_count: int = 0
    total_ventas_cs: Decimal
    total_ventas_usd: Decimal
    efectivo_ventas_cs: Decimal
    tarjeta_ventas_cs: Decimal
    transferencia_ventas_cs: Decimal
    otros_pagos_cs: Decimal
    has_closed: bool = False
    closed_id: Optional[int] = None


class CashCloseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cierre_numero: str
    fecha: date
    bodega_id: Optional[int] = None
    usuario_registro: Optional[str] = None
    total_ventas_cs: Decimal
    total_ventas_usd: Decimal
    efectivo_ventas_cs: Decimal
    tarjeta_ventas_cs: Decimal
    transferencia_ventas_cs: Decimal
    otros_pagos_cs: Decimal
    ingresos_caja_cs: Decimal
    egresos_caja_cs: Decimal
    efectivo_esperado_cs: Decimal
    efectivo_fisico_cs: Decimal
    diferencia_cs: Decimal
    resultado: str
    observacion: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    movements: List[CashCloseMovementResponse] = Field(default_factory=list)
