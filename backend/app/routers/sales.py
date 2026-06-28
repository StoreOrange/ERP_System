from decimal import Decimal, ROUND_HALF_UP
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models.inventory import Bodega, EgresoInventario, EgresoItem, EgresoTipo, Producto
from ..models.sales import Customer, SalesInvoice, SalesInvoiceItem, SalesPayment, SalesSequence
from ..models.settings import BusinessSetting
from ..routers.inventory import (
    _balances_by_bodega,
    _cost_pair_from_amount,
    _get_business_settings,
    _get_or_create_saldo,
    _normalize_currency,
    _product_cost_pair,
    _rebuild_global_saldo,
    _require_exchange_rate,
)
from ..schemas.sales import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    SalesInvoiceCreate,
    SalesInvoiceResponse,
    SalesNextInvoiceResponse,
)

router = APIRouter(prefix="/sales-api", tags=["Sales"])

MONEY = Decimal("0.01")


def _money(value: Decimal | int | float | str | None) -> Decimal:
    return Decimal(str(value or 0)).quantize(MONEY, rounding=ROUND_HALF_UP)


def _next_invoice_number(db: Session) -> str:
    sequence = db.query(SalesSequence).filter(SalesSequence.prefix == "POS").with_for_update().first()
    if not sequence:
        sequence = SalesSequence(prefix="POS", current_value=0, is_active=True)
        db.add(sequence)
        db.flush()
    sequence.current_value = int(sequence.current_value or 0) + 1
    return f"{sequence.prefix}-{sequence.current_value:06d}"


def _peek_invoice_number(db: Session) -> str:
    sequence = db.query(SalesSequence).filter(SalesSequence.prefix == "POS").first()
    next_value = int(sequence.current_value or 0) + 1 if sequence else 1
    return f"POS-{next_value:06d}"


def _resolve_venta_tipo(db: Session) -> EgresoTipo:
    tipo = db.query(EgresoTipo).filter(func.lower(func.trim(EgresoTipo.nombre)) == "venta").first()
    if tipo:
        return tipo
    tipo = EgresoTipo(nombre="Venta")
    db.add(tipo)
    db.flush()
    return tipo


def _to_currency_pair(amount: Decimal, moneda: str, tasa: Decimal) -> tuple[Decimal, Decimal]:
    if moneda == "USD":
        return _money(amount), _money(amount * tasa)
    return _money(amount / tasa) if tasa > 0 else Decimal("0.00"), _money(amount)


def _settings_rate(settings: BusinessSetting | None, payload_rate: Decimal | None, moneda: str) -> Decimal:
    if moneda == "USD":
        return _require_exchange_rate(moneda, payload_rate)
    return payload_rate or Decimal("0")


@router.get("/invoices/next", response_model=SalesNextInvoiceResponse)
def get_next_invoice(db: Session = Depends(get_db)):
    return SalesNextInvoiceResponse(invoice_number=_peek_invoice_number(db))


@router.get("/customers", response_model=List[CustomerResponse])
def list_customers(q: str | None = None, include_inactive: bool = False, db: Session = Depends(get_db)):
    query = db.query(Customer)
    if not include_inactive:
        query = query.filter(Customer.activo.is_(True))
    if q:
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Customer.nombre.ilike(term),
                Customer.identificacion.ilike(term),
                Customer.telefono.ilike(term),
                Customer.email.ilike(term),
            )
        )
    return query.order_by(Customer.nombre.asc()).limit(300).all()


@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    nombre = (payload.nombre or "").strip()
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre de cliente requerido")

    identificacion = (payload.identificacion or "").strip()
    if identificacion:
        exists = db.query(Customer).filter(func.lower(Customer.identificacion) == identificacion.lower()).first()
        if exists:
            raise HTTPException(status_code=400, detail="Ya existe un cliente con esa identificacion")

    customer = Customer(
        nombre=nombre,
        telefono=(payload.telefono or "").strip() or None,
        identificacion=identificacion or None,
        direccion=(payload.direccion or "").strip() or None,
        email=(payload.email or "").strip() or None,
        tipo=(payload.tipo or "").strip() or None,
        activo=bool(payload.activo),
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    data = payload.model_dump(exclude_unset=True)
    if "nombre" in data:
        nombre = (data["nombre"] or "").strip()
        if not nombre:
            raise HTTPException(status_code=400, detail="Nombre de cliente requerido")
        customer.nombre = nombre
    if "identificacion" in data:
        identificacion = (data.get("identificacion") or "").strip()
        if identificacion:
            exists = (
                db.query(Customer)
                .filter(func.lower(Customer.identificacion) == identificacion.lower(), Customer.id != customer.id)
                .first()
            )
            if exists:
                raise HTTPException(status_code=400, detail="Ya existe un cliente con esa identificacion")
        customer.identificacion = identificacion or None
    for field in ("telefono", "direccion", "email", "tipo"):
        if field in data:
            setattr(customer, field, (data.get(field) or "").strip() or None)
    if "activo" in data:
        customer.activo = bool(data["activo"])

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/invoices", response_model=List[SalesInvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    return (
        db.query(SalesInvoice)
        .options(joinedload(SalesInvoice.items), joinedload(SalesInvoice.payments))
        .order_by(SalesInvoice.id.desc())
        .limit(100)
        .all()
    )


@router.post("/invoices", response_model=SalesInvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: SalesInvoiceCreate, db: Session = Depends(get_db)):
    settings = _get_business_settings(db)
    if not payload.items:
        raise HTTPException(status_code=400, detail="Debes registrar al menos un item")

    condicion = (payload.condicion or "CONTADO").strip().upper()
    if condicion not in {"CONTADO", "CREDITO"}:
        raise HTTPException(status_code=400, detail="Condicion de venta invalida")

    moneda = _normalize_currency(payload.moneda)
    tasa = _settings_rate(settings, payload.tasa_cambio, moneda)
    if moneda == "CS" and any((payment.moneda or "").strip().upper() == "USD" for payment in payload.payments) and tasa <= 0:
        raise HTTPException(status_code=400, detail="La tasa de cambio es requerida para pagos en USD")

    bodega = db.query(Bodega).filter(Bodega.id == payload.bodega_id).first()
    if not bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    product_ids = [int(item.producto_id) for item in payload.items]
    balances = _balances_by_bodega(db, [payload.bodega_id], product_ids)
    venta_tipo = _resolve_venta_tipo(db)

    invoice_number = _next_invoice_number(db)
    egreso = EgresoInventario(
        tipo_id=venta_tipo.id,
        bodega_id=payload.bodega_id,
        bodega_destino_id=None,
        usuario_id=None,
        fecha=payload.fecha,
        moneda=moneda,
        tasa_cambio=payload.tasa_cambio,
        observacion=f"Factura {invoice_number}. {payload.observacion or ''}".strip()[:300],
        usuario_registro=payload.usuario_registro,
    )
    db.add(egreso)
    db.flush()

    invoice = SalesInvoice(
        invoice_number=invoice_number,
        customer_name=(payload.customer_name or "Consumidor final").strip() or "Consumidor final",
        customer_phone=payload.customer_phone,
        customer_document=payload.customer_document,
        customer_address=payload.customer_address,
        vendor_name=payload.vendor_name,
        bodega_id=payload.bodega_id,
        egreso_id=egreso.id,
        fecha=payload.fecha,
        condicion=condicion,
        moneda=moneda,
        tasa_cambio=payload.tasa_cambio,
        observacion=payload.observacion,
        usuario_registro=payload.usuario_registro,
        status="EMITIDA" if condicion == "CONTADO" else "CREDITO",
    )
    db.add(invoice)
    db.flush()

    totals_usd = Decimal("0")
    totals_cs = Decimal("0")
    egreso_total_usd = Decimal("0")
    egreso_total_cs = Decimal("0")
    requested_by_product: dict[int, Decimal] = {}

    for item in payload.items:
        product_id = int(item.producto_id)
        cantidad = Decimal(str(item.cantidad or 0))
        precio_unitario = Decimal(str(item.precio_unitario or 0))
        if cantidad <= 0 or precio_unitario < 0:
            raise HTTPException(status_code=400, detail="Cantidad y precio deben ser validos")
        combo_role = (item.combo_role or "").strip().lower() or None
        if combo_role and combo_role not in {"parent", "gift"}:
            raise HTTPException(status_code=400, detail="Rol de combo invalido")
        combo_group = (item.combo_group or "").strip() or None

        requested_by_product[product_id] = requested_by_product.get(product_id, Decimal("0")) + cantidad
        available = Decimal(str(balances.get((product_id, payload.bodega_id), Decimal("0")) or 0))
        if requested_by_product[product_id] > available:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para producto {product_id}. Disponible: {available}")

        producto = db.query(Producto).options(joinedload(Producto.unidad_medida)).filter(Producto.id == product_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {product_id} no encontrado")

        _get_or_create_saldo(db, producto.id)
        price_usd, price_cs = _to_currency_pair(precio_unitario, moneda, tasa)
        subtotal_usd = _money(price_usd * cantidad)
        subtotal_cs = _money(price_cs * cantidad)
        totals_usd += subtotal_usd
        totals_cs += subtotal_cs

        cost_usd, cost_cs = _product_cost_pair(producto, tasa, settings)
        egreso_subtotal_usd = _money(cost_usd * cantidad)
        egreso_subtotal_cs = _money(cost_cs * cantidad)
        egreso_total_usd += egreso_subtotal_usd
        egreso_total_cs += egreso_subtotal_cs

        db.add(
            SalesInvoiceItem(
                invoice_id=invoice.id,
                producto_id=producto.id,
                cod_producto=item.cod_producto or producto.cod_producto,
                descripcion=item.descripcion or producto.descripcion,
                unidad=item.unidad or getattr(producto.unidad_medida, "abreviatura", None) or "UND",
                cantidad=cantidad,
                precio_unitario_usd=price_usd,
                precio_unitario_cs=price_cs,
                subtotal_usd=subtotal_usd,
                subtotal_cs=subtotal_cs,
                combo_role=combo_role,
                combo_group=combo_group,
            )
        )
        db.add(
            EgresoItem(
                egreso_id=egreso.id,
                producto_id=producto.id,
                cantidad=cantidad,
                costo_unitario_usd=cost_usd,
                costo_unitario_cs=cost_cs,
                subtotal_usd=egreso_subtotal_usd,
                subtotal_cs=egreso_subtotal_cs,
            )
        )

    paid_usd = Decimal("0")
    paid_cs = Decimal("0")
    if condicion == "CONTADO" and not payload.payments:
        raise HTTPException(status_code=400, detail="La venta de contado requiere al menos una forma de pago")

    for payment in payload.payments:
        payment_currency = _normalize_currency(payment.moneda)
        amount = Decimal(str(payment.monto or 0))
        if amount <= 0:
            raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor que cero")
        amount_usd, amount_cs = _to_currency_pair(amount, payment_currency, tasa)
        paid_usd += amount_usd
        paid_cs += amount_cs
        db.add(
            SalesPayment(
                invoice_id=invoice.id,
                forma_codigo=(payment.forma_codigo or "").strip() or "cash",
                forma_nombre=(payment.forma_nombre or "").strip() or "Efectivo",
                moneda=payment_currency,
                monto=_money(amount),
                monto_usd=amount_usd,
                monto_cs=amount_cs,
                banco=payment.banco,
                cuenta=payment.cuenta,
                referencia=payment.referencia,
            )
        )

    if condicion == "CONTADO" and paid_cs < _money(totals_cs):
        raise HTTPException(status_code=400, detail="El pago no cubre el total de la factura")

    balance_cs = max(_money(totals_cs - paid_cs), Decimal("0.00"))
    change_cs = max(_money(paid_cs - totals_cs), Decimal("0.00"))
    balance_usd = _money(balance_cs / tasa) if tasa > 0 else Decimal("0.00")
    change_usd = _money(change_cs / tasa) if tasa > 0 else Decimal("0.00")

    invoice.subtotal_usd = _money(totals_usd)
    invoice.subtotal_cs = _money(totals_cs)
    invoice.total_usd = _money(totals_usd)
    invoice.total_cs = _money(totals_cs)
    invoice.paid_usd = _money(paid_usd)
    invoice.paid_cs = _money(paid_cs)
    invoice.balance_usd = balance_usd
    invoice.balance_cs = balance_cs
    invoice.change_usd = change_usd
    invoice.change_cs = change_cs

    egreso.total_usd = egreso_total_usd
    egreso.total_cs = egreso_total_cs

    for product_id in product_ids:
        _rebuild_global_saldo(db, product_id)

    db.commit()
    return (
        db.query(SalesInvoice)
        .options(joinedload(SalesInvoice.items), joinedload(SalesInvoice.payments))
        .filter(SalesInvoice.id == invoice.id)
        .first()
    )
