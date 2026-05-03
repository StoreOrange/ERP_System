from __future__ import annotations

from decimal import Decimal

from sqlalchemy import create_engine, or_, text
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.inventory import Bodega, Linea, Producto, SaldoProducto, Segmento, UnidadMedida

SOURCE_DB_URL = "postgresql://user:1234@localhost:5432/hollpacas"


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

        for row in source_productos:
            existing = (
                target_db.query(Producto)
                .filter(Producto.cod_producto == row["cod_producto"])
                .first()
            )
            payload = {
                "descripcion": row["descripcion"],
                "segmento_id": segmento_map.get(int(row["segmento_id"])) if row["segmento_id"] else None,
                "linea_id": linea_map.get(int(row["linea_id"])) if row["linea_id"] else None,
                "unidad_medida_id": unidad_map.get(int(row["unidad_medida_id"])) if row["unidad_medida_id"] else None,
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

        target_db.commit()
        return counters
    finally:
        target_db.close()
        source_engine.dispose()


if __name__ == "__main__":
    result = import_catalogs_and_inventory()
    print(result)
