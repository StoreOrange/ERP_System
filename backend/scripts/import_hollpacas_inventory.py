from __future__ import annotations

import os
from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine, func, or_, text
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.inventory import (
    Bodega,
    EgresoItem,
    EgresoInventario,
    EgresoTipo,
    IngresoInventario,
    IngresoItem,
    IngresoTipo,
    Linea,
    Producto,
    SaldoProducto,
    Segmento,
    UnidadMedida,
)

SOURCE_DB_URL = os.getenv(
    "HOLLPACAS_DB_URL",
    "postgresql://user:1234@localhost:5432/hollpacas",
)


def _d(value) -> Decimal:
    return Decimal(str(value or 0))


def import_catalogs_and_inventory() -> dict[str, int]:
    source_engine = create_engine(SOURCE_DB_URL)
    target_db: Session = SessionLocal()

    counters = {
        "lineas": 0,
        "segmentos": 0,
        "unidades": 0,
        "bodegas": 0,
        "productos": 0,
        "saldos": 0,
        "existencias_bodega": 0,
        "ingresos": 0,
        "ingreso_items": 0,
        "egresos": 0,
        "egreso_items": 0,
    }

    try:
        with source_engine.connect() as conn:
            source_lineas = conn.execute(
                text(
                    """
                    select id, cod_linea, linea, coalesce(activo, true) as activo
                    from lineas
                    order by id
                    """
                )
            ).mappings().all()
            source_segmentos = conn.execute(
                text(
                    """
                    select id, segmento
                    from segmentos
                    order by id
                    """
                )
            ).mappings().all()
            source_unidades = conn.execute(
                text(
                    """
                    select id, codigo, nombre, abreviatura, coalesce(activo, true) as activo
                    from unidades_medida
                    order by id
                    """
                )
            ).mappings().all()
            source_bodegas = conn.execute(
                text(
                    """
                    select id, code, name, coalesce(activo, true) as activo
                    from bodegas
                    order by id
                    """
                )
            ).mappings().all()
            source_ingreso_tipos = conn.execute(
                text(
                    """
                    select id, nombre, coalesce(requiere_proveedor, false) as requiere_proveedor
                    from ingreso_tipos
                    order by id
                    """
                )
            ).mappings().all()
            source_egreso_tipos = conn.execute(
                text(
                    """
                    select id, nombre
                    from egreso_tipos
                    order by id
                    """
                )
            ).mappings().all()
            source_productos = conn.execute(
                text(
                    """
                    select
                        p.id,
                        p.cod_producto,
                        p.descripcion,
                        p.segmento_id,
                        p.linea_id,
                        p.unidad_medida_id,
                        p.marca,
                        p.precio_venta1,
                        p.precio_venta2,
                        p.precio_venta3,
                        p.activo,
                        p.servicio_producto,
                        p.es_por_peso,
                        p.costo_producto,
                        p.referencia_producto,
                        p.usuario_registro,
                        p.maquina_registro,
                        s.existencia
                    from productos p
                    left join saldos_productos s on s.producto_id = p.id
                    order by p.id
                    """
                )
            ).mappings().all()
            source_ingresos = conn.execute(
                text(
                    """
                    select id, tipo_id, bodega_id, fecha, moneda, tasa_cambio, total_usd, total_cs,
                           observacion, usuario_registro
                    from ingresos_inventario
                    order by id
                    """
                )
            ).mappings().all()
            source_ingreso_items = conn.execute(
                text(
                    """
                    select id, ingreso_id, producto_id, cantidad, costo_unitario_usd, costo_unitario_cs,
                           subtotal_usd, subtotal_cs
                    from ingreso_items
                    order by id
                    """
                )
            ).mappings().all()
            source_egresos = conn.execute(
                text(
                    """
                    select id, tipo_id, bodega_id, bodega_destino_id, fecha, moneda, tasa_cambio,
                           total_usd, total_cs, observacion, usuario_registro
                    from egresos_inventario
                    order by id
                    """
                )
            ).mappings().all()
            source_egreso_items = conn.execute(
                text(
                    """
                    select id, egreso_id, producto_id, cantidad, costo_unitario_usd, costo_unitario_cs,
                           subtotal_usd, subtotal_cs
                    from egreso_items
                    order by id
                    """
                )
            ).mappings().all()

        linea_map: dict[int, int] = {}
        for row in source_lineas:
            existing = (
                target_db.query(Linea)
                .filter(Linea.cod_linea == row["cod_linea"])
                .first()
            )
            if not existing:
                existing = Linea(
                    cod_linea=row["cod_linea"],
                    linea=row["linea"],
                    activo=bool(row["activo"]),
                )
                target_db.add(existing)
                target_db.flush()
                counters["lineas"] += 1
            else:
                existing.linea = row["linea"]
                existing.activo = bool(row["activo"])
            linea_map[int(row["id"])] = existing.id

        segmento_map: dict[int, int] = {}
        for row in source_segmentos:
            existing = (
                target_db.query(Segmento)
                .filter(Segmento.segmento == row["segmento"])
                .first()
            )
            if not existing:
                existing = Segmento(
                    segmento=row["segmento"],
                )
                target_db.add(existing)
                target_db.flush()
                counters["segmentos"] += 1
            segmento_map[int(row["id"])] = existing.id

        unidad_map: dict[int, int] = {}
        for row in source_unidades:
            existing = (
                target_db.query(UnidadMedida)
                .filter(
                    or_(
                        UnidadMedida.codigo == row["codigo"],
                        UnidadMedida.nombre == row["nombre"],
                    )
                )
                .first()
            )
            if not existing:
                existing = UnidadMedida(
                    codigo=row["codigo"],
                    nombre=row["nombre"],
                    abreviatura=row["abreviatura"],
                    activo=bool(row["activo"]),
                )
                target_db.add(existing)
                target_db.flush()
                counters["unidades"] += 1
            else:
                existing.codigo = row["codigo"]
                existing.nombre = row["nombre"]
                existing.abreviatura = row["abreviatura"]
                existing.activo = bool(row["activo"])
            unidad_map[int(row["id"])] = existing.id

        bodega_map: dict[int, int] = {}
        for row in source_bodegas:
            existing = target_db.query(Bodega).filter(Bodega.code == row["code"]).first()
            if not existing:
                existing = Bodega(
                    code=row["code"],
                    name=row["name"],
                    activo=bool(row["activo"]),
                )
                target_db.add(existing)
                counters["bodegas"] += 1
            else:
                existing.name = row["name"]
                existing.activo = bool(row["activo"])
            target_db.flush()
            bodega_map[int(row["id"])] = existing.id

        ingreso_tipo_map: dict[int, int] = {}
        for row in source_ingreso_tipos:
            existing = target_db.query(IngresoTipo).filter(IngresoTipo.nombre == row["nombre"]).first()
            if not existing:
                existing = IngresoTipo(
                    nombre=row["nombre"],
                    requiere_proveedor=bool(row["requiere_proveedor"]),
                )
                target_db.add(existing)
                target_db.flush()
            else:
                existing.requiere_proveedor = bool(row["requiere_proveedor"])
            ingreso_tipo_map[int(row["id"])] = existing.id

        egreso_tipo_map: dict[int, int] = {}
        for row in source_egreso_tipos:
            existing = target_db.query(EgresoTipo).filter(EgresoTipo.nombre == row["nombre"]).first()
            if not existing:
                existing = EgresoTipo(nombre=row["nombre"])
                target_db.add(existing)
                target_db.flush()
            egreso_tipo_map[int(row["id"])] = existing.id

        product_map: dict[int, int] = {}
        for row in source_productos:
            existing = (
                target_db.query(Producto)
                .filter(Producto.cod_producto == row["cod_producto"])
                .first()
            )
            default_unit = (
                target_db.query(UnidadMedida)
                .filter(or_(UnidadMedida.codigo == "UND", UnidadMedida.nombre == "Unidad"))
                .first()
            )
            payload = {
                "descripcion": row["descripcion"],
                "segmento_id": segmento_map.get(int(row["segmento_id"])) if row["segmento_id"] else None,
                "linea_id": linea_map.get(int(row["linea_id"])) if row["linea_id"] else None,
                "unidad_medida_id": (
                    unidad_map.get(int(row["unidad_medida_id"]))
                    if row["unidad_medida_id"]
                    else default_unit.id if default_unit else None
                ),
                "marca": row["marca"],
                "presentacion": None,
                "precio_venta1": _d(row["precio_venta1"]),
                "precio_venta2": _d(row["precio_venta2"]),
                "precio_venta3": _d(row["precio_venta3"]),
                "activo": bool(row["activo"]),
                "servicio_producto": bool(row["servicio_producto"]),
                "es_por_peso": bool(row["es_por_peso"]),
                "costo_producto": _d(row["costo_producto"]),
                "referencia_producto": row["referencia_producto"],
                "usuario_registro": row["usuario_registro"],
                "maquina_registro": row["maquina_registro"],
            }

            if not existing:
                existing = Producto(cod_producto=row["cod_producto"], **payload)
                target_db.add(existing)
                target_db.flush()
                counters["productos"] += 1
            else:
                for key, value in payload.items():
                    setattr(existing, key, value)

            saldo = (
                target_db.query(SaldoProducto)
                .filter(SaldoProducto.producto_id == existing.id)
                .first()
            )
            if not saldo:
                saldo = SaldoProducto(producto_id=existing.id, existencia=_d(row["existencia"]))
                target_db.add(saldo)
                counters["saldos"] += 1
            else:
                saldo.existencia = _d(row["existencia"])
            product_map[int(row["id"])] = existing.id

        imported_ingresos = (
            target_db.query(IngresoInventario)
            .filter(IngresoInventario.usuario_registro == "importador_hollpacas")
            .all()
        )
        for ingreso in imported_ingresos:
            target_db.delete(ingreso)

        imported_egresos = (
            target_db.query(EgresoInventario)
            .filter(EgresoInventario.usuario_registro == "importador_hollpacas")
            .all()
        )
        for egreso in imported_egresos:
            target_db.delete(egreso)

        temporary_ingresos = (
            target_db.query(IngresoInventario)
            .filter(IngresoInventario.observacion == "Importacion inicial HollywoodPacas")
            .all()
        )
        for ingreso in temporary_ingresos:
            target_db.delete(ingreso)
        target_db.flush()

        if source_ingresos or source_egresos:
            ingreso_header_map: dict[int, int] = {}
            ingreso_items_by_header: dict[int, list] = {}
            for row in source_ingreso_items:
                ingreso_items_by_header.setdefault(int(row["ingreso_id"]), []).append(row)

            for row in source_ingresos:
                bodega_id = bodega_map.get(int(row["bodega_id"])) if row["bodega_id"] else None
                tipo_id = ingreso_tipo_map.get(int(row["tipo_id"])) if row["tipo_id"] else None
                if not bodega_id or not tipo_id:
                    continue
                ingreso = IngresoInventario(
                    tipo_id=tipo_id,
                    bodega_id=bodega_id,
                    proveedor_id=None,
                    usuario_id=None,
                    fecha=row["fecha"],
                    moneda=row["moneda"] or "CS",
                    tasa_cambio=_d(row["tasa_cambio"]) if row["tasa_cambio"] else None,
                    total_usd=_d(row["total_usd"]),
                    total_cs=_d(row["total_cs"]),
                    observacion=f"Hollpacas #{row['id']}: {row['observacion'] or ''}".strip(),
                    usuario_registro="importador_hollpacas",
                )
                target_db.add(ingreso)
                target_db.flush()
                ingreso_header_map[int(row["id"])] = ingreso.id
                counters["ingresos"] += 1

                for item in ingreso_items_by_header.get(int(row["id"]), []):
                    producto_id = product_map.get(int(item["producto_id"]))
                    if not producto_id:
                        continue
                    target_db.add(
                        IngresoItem(
                            ingreso_id=ingreso.id,
                            producto_id=producto_id,
                            cantidad=_d(item["cantidad"]),
                            costo_unitario_usd=_d(item["costo_unitario_usd"]),
                            costo_unitario_cs=_d(item["costo_unitario_cs"]),
                            subtotal_usd=_d(item["subtotal_usd"]),
                            subtotal_cs=_d(item["subtotal_cs"]),
                        )
                    )
                    counters["ingreso_items"] += 1

            egreso_items_by_header: dict[int, list] = {}
            for row in source_egreso_items:
                egreso_items_by_header.setdefault(int(row["egreso_id"]), []).append(row)

            for row in source_egresos:
                bodega_id = bodega_map.get(int(row["bodega_id"])) if row["bodega_id"] else None
                tipo_id = egreso_tipo_map.get(int(row["tipo_id"])) if row["tipo_id"] else None
                if not bodega_id or not tipo_id:
                    continue
                destino_id = (
                    bodega_map.get(int(row["bodega_destino_id"]))
                    if row["bodega_destino_id"]
                    else None
                )
                egreso = EgresoInventario(
                    tipo_id=tipo_id,
                    bodega_id=bodega_id,
                    bodega_destino_id=destino_id,
                    usuario_id=None,
                    fecha=row["fecha"],
                    moneda=row["moneda"] or "CS",
                    tasa_cambio=_d(row["tasa_cambio"]) if row["tasa_cambio"] else None,
                    total_usd=_d(row["total_usd"]),
                    total_cs=_d(row["total_cs"]),
                    observacion=f"Hollpacas #{row['id']}: {row['observacion'] or ''}".strip(),
                    usuario_registro="importador_hollpacas",
                )
                target_db.add(egreso)
                target_db.flush()
                counters["egresos"] += 1

                for item in egreso_items_by_header.get(int(row["id"]), []):
                    producto_id = product_map.get(int(item["producto_id"]))
                    if not producto_id:
                        continue
                    target_db.add(
                        EgresoItem(
                            egreso_id=egreso.id,
                            producto_id=producto_id,
                            cantidad=_d(item["cantidad"]),
                            costo_unitario_usd=_d(item["costo_unitario_usd"]),
                            costo_unitario_cs=_d(item["costo_unitario_cs"]),
                            subtotal_usd=_d(item["subtotal_usd"]),
                            subtotal_cs=_d(item["subtotal_cs"]),
                        )
                    )
                    counters["egreso_items"] += 1

            target_db.flush()
            for producto_id in product_map.values():
                total_entradas = (
                    target_db.query(func.coalesce(func.sum(IngresoItem.cantidad), 0))
                    .filter(IngresoItem.producto_id == producto_id)
                    .scalar()
                )
                total_salidas = (
                    target_db.query(func.coalesce(func.sum(EgresoItem.cantidad), 0))
                    .filter(EgresoItem.producto_id == producto_id)
                    .scalar()
                )
                saldo = (
                    target_db.query(SaldoProducto)
                    .filter(SaldoProducto.producto_id == producto_id)
                    .first()
                )
                if saldo:
                    saldo.existencia = _d(total_entradas) - _d(total_salidas)
        else:
            default_bodega = (
                target_db.query(Bodega)
                .filter(or_(Bodega.code == "BOD-001", Bodega.name == "Bodega Principal"))
                .order_by(Bodega.id)
                .first()
            )
            if not default_bodega:
                default_bodega = target_db.query(Bodega).filter(Bodega.activo.is_(True)).order_by(Bodega.id).first()

            positive_saldos = (
                target_db.query(SaldoProducto)
                .join(Producto, Producto.id == SaldoProducto.producto_id)
                .filter(SaldoProducto.existencia > 0)
                .order_by(Producto.id)
                .all()
            )
            initial_items: list[tuple[Producto, Decimal]] = []
            for saldo in positive_saldos:
                existing_ingresos = (
                    target_db.query(IngresoItem.id)
                    .filter(IngresoItem.producto_id == saldo.producto_id)
                    .first()
                )
                existing_egresos = (
                    target_db.query(EgresoItem.id)
                    .filter(EgresoItem.producto_id == saldo.producto_id)
                    .first()
                )
                if not existing_ingresos and not existing_egresos and saldo.producto:
                    initial_items.append((saldo.producto, _d(saldo.existencia)))

            if default_bodega and initial_items:
                ingreso_tipo = (
                    target_db.query(IngresoTipo)
                    .filter(IngresoTipo.nombre == "Inventario Inicial")
                    .first()
                )
                if not ingreso_tipo:
                    ingreso_tipo = IngresoTipo(nombre="Inventario Inicial", requiere_proveedor=False)
                    target_db.add(ingreso_tipo)
                    target_db.flush()

                ingreso = IngresoInventario(
                    tipo_id=ingreso_tipo.id,
                    bodega_id=default_bodega.id,
                    proveedor_id=None,
                    usuario_id=None,
                    fecha=date.today(),
                    moneda="CS",
                    tasa_cambio=None,
                    observacion="Importacion inicial HollywoodPacas",
                    usuario_registro="importador",
                    total_usd=Decimal("0"),
                    total_cs=Decimal("0"),
                )
                target_db.add(ingreso)
                target_db.flush()

                total_cs = Decimal("0")
                for producto, cantidad in initial_items:
                    costo_cs = _d(producto.costo_producto)
                    subtotal_cs = cantidad * costo_cs
                    total_cs += subtotal_cs
                    target_db.add(
                        IngresoItem(
                            ingreso_id=ingreso.id,
                            producto_id=producto.id,
                            cantidad=cantidad,
                            costo_unitario_usd=Decimal("0"),
                            costo_unitario_cs=costo_cs,
                            subtotal_usd=Decimal("0"),
                            subtotal_cs=subtotal_cs,
                        )
                    )
                    counters["existencias_bodega"] += 1
                ingreso.total_cs = total_cs

        target_db.commit()
        return counters
    finally:
        target_db.close()
        source_engine.dispose()


if __name__ == "__main__":
    result = import_catalogs_and_inventory()
    print(result)
