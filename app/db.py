# ============================================================
#  GuateCompost ERP — Capa de base de datos
#  Autor: Edwin Lee Tiño
# ============================================================

import sqlite3
import os

# ─── CONEXIÓN ────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guatecompost.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ─── PRODUCTOS ───────────────────────────────────────────────

def get_productos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id_producto, nombre, categoria,
                   unidad_medida, costo, precio
            FROM producto
            WHERE activo = 1
            ORDER BY categoria, nombre
        """).fetchall()

def insert_producto(nombre, descripcion, categoria,
                    unidad_medida, costo, precio):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO producto
                (nombre, descripcion, categoria, unidad_medida, costo, precio)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, descripcion, categoria, unidad_medida, costo, precio))
        conn.commit()

def delete_producto(id_producto):
    with get_connection() as conn:
        conn.execute("""
            UPDATE producto SET activo = 0
            WHERE id_producto = ?
        """, (id_producto,))
        conn.commit()

# ─── CLIENTES ────────────────────────────────────────────────

def get_clientes():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id_cliente, nombre, nit, telefono, correo, direccion
            FROM cliente
            WHERE activo = 1
            ORDER BY nombre
        """).fetchall()

def insert_cliente(nombre, nit, telefono, correo, direccion):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO cliente (nombre, nit, telefono, correo, direccion)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, nit, telefono, correo, direccion))
        conn.commit()

def delete_cliente(id_cliente):
    with get_connection() as conn:
        conn.execute("""
            UPDATE cliente SET activo = 0
            WHERE id_cliente = ?
        """, (id_cliente,))
        conn.commit()

# ─── PROVEEDORES ─────────────────────────────────────────────

def get_proveedores():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id_proveedor, nombre, contacto, nit, telefono, correo, direccion
            FROM proveedor
            WHERE activo = 1
            ORDER BY nombre
        """).fetchall()

def insert_proveedor(nombre, contacto, nit, telefono, correo, direccion):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO proveedor (nombre, contacto, nit, telefono, correo, direccion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, contacto, nit, telefono, correo, direccion))
        conn.commit()

def delete_proveedor(id_proveedor):
    with get_connection() as conn:
        conn.execute("""
            UPDATE proveedor SET activo = 0
            WHERE id_proveedor = ?
        """, (id_proveedor,))
        conn.commit()

# ─── INSUMOS ─────────────────────────────────────────────────

def get_insumos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id_insumo, nombre, descripcion, unidad_medida, costo
            FROM insumo
            WHERE activo = 1
            ORDER BY nombre
        """).fetchall()

def insert_insumo(nombre, descripcion, unidad_medida, costo):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO insumo (nombre, descripcion, unidad_medida, costo)
            VALUES (?, ?, ?, ?)
        """, (nombre, descripcion, unidad_medida, costo))
        conn.commit()

def delete_insumo(id_insumo):
    with get_connection() as conn:
        conn.execute("""
            UPDATE insumo SET activo = 0
            WHERE id_insumo = ?
        """, (id_insumo,))
        conn.commit()

# ─── VENTAS ──────────────────────────────────────────────────

def get_ventas():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                vc.id_venta,
                vc.fecha_venta,
                c.nombre AS cliente,
                SUM(vd.cantidad * vd.precio_unitario) AS total
            FROM venta_cabecera vc
            JOIN cliente c ON vc.id_cliente = c.id_cliente
            JOIN venta_detalle vd ON vc.id_venta = vd.id_venta
            GROUP BY vc.id_venta, vc.fecha_venta, c.nombre
            ORDER BY vc.fecha_venta DESC
        """).fetchall()

def insert_venta(fecha, id_cliente, detalle):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO venta_cabecera (fecha_venta, id_cliente)
            VALUES (?, ?)
        """, (fecha, id_cliente))
        id_venta = cursor.lastrowid
        for item in detalle:
            conn.execute("""
                INSERT INTO venta_detalle
                    (id_venta, id_producto, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (id_venta, item['id_producto'],
                  item['cantidad'], item['precio_unitario']))
        conn.commit()

def delete_venta(id_venta):
    with get_connection() as conn:
        conn.execute("DELETE FROM venta_detalle WHERE id_venta = ?", (id_venta,))
        conn.execute("DELETE FROM venta_cabecera WHERE id_venta = ?", (id_venta,))
        conn.commit()

def delete_venta_item(id_venta, id_producto):
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM venta_detalle
            WHERE id_venta = ? AND id_producto = ?
        """, (id_venta, id_producto))
        conn.commit()

# ─── COMPRAS ──────────────────────────────────────────────────

def get_compras():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                cc.id_compra,
                cc.fecha_compra,
                p.nombre AS proveedor,
                SUM(cd.cantidad * cd.costo_unitario) AS total
            FROM compra_cabecera cc
            JOIN proveedor p ON cc.id_proveedor = p.id_proveedor
            JOIN compra_detalle cd ON cc.id_compra = cd.id_compra
            GROUP BY cc.id_compra, cc.fecha_compra, p.nombre
            ORDER BY cc.fecha_compra DESC
        """).fetchall()

def insert_compra(fecha, id_proveedor, detalle):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO compra_cabecera (fecha_compra, id_proveedor)
            VALUES (?, ?)
        """, (fecha, id_proveedor))
        id_compra = cursor.lastrowid
        for item in detalle:
            conn.execute("""
                INSERT INTO compra_detalle
                    (id_compra, id_producto, cantidad, costo_unitario)
                VALUES (?, ?, ?, ?)
            """, (id_compra, item['id_producto'],
                  item['cantidad'], item['costo_unitario']))
        conn.commit()

def delete_compra(id_compra):
    with get_connection() as conn:
        conn.execute("DELETE FROM compra_detalle WHERE id_compra = ?", (id_compra,))
        conn.execute("DELETE FROM compra_cabecera WHERE id_compra = ?", (id_compra,))
        conn.commit()

def delete_compra_item(id_compra, id_producto):
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM compra_detalle
            WHERE id_compra = ? AND id_producto = ?
        """, (id_compra, id_producto))
        conn.commit()

# ─── GASTOS OPERATIVOS ──────────────────────────────────────────────────

def get_gastos():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                gc.id_gasto,
                gc.fecha_gasto,
                gc.descripcion,
                p.nombre AS proveedor,
                SUM(gd.cantidad * gd.costo_unitario) AS total
            FROM gasto_cabecera gc
            JOIN proveedor p ON gc.id_proveedor = p.id_proveedor
            JOIN gasto_detalle gd ON gc.id_gasto = gd.id_gasto
            GROUP BY gc.id_gasto, gc.fecha_gasto, p.nombre
            ORDER BY gc.fecha_gasto DESC
        """).fetchall()

def insert_gasto(fecha, id_proveedor, descripcion, detalle):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO gasto_cabecera (fecha_gasto, id_proveedor, descripcion)
            VALUES (?, ?, ?)
        """, (fecha, id_proveedor, descripcion))
        id_gasto = cursor.lastrowid
        for item in detalle:
            conn.execute("""
                INSERT INTO gasto_detalle
                    (id_gasto, id_insumo, cantidad, costo_unitario)
                VALUES (?, ?, ?, ?)
            """, (id_gasto, item['id_insumo'],
                  item['cantidad'], item['costo_unitario']))
        conn.commit()

def delete_gasto(id_gasto):
    with get_connection() as conn:
        conn.execute("DELETE FROM gasto_detalle WHERE id_gasto = ?", (id_gasto,))
        conn.execute("DELETE FROM gasto_cabecera WHERE id_gasto = ?", (id_gasto,))
        conn.commit()

def delete_gasto_item(id_gasto, id_insumo):
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM gasto_detalle
            WHERE id_gasto = ? AND id_insumo = ?
        """, (id_gasto, id_insumo))
        conn.commit()

# ─── INVENTARIO ──────────────────────────────────────────────

def get_stock_actual():
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                p.id_producto,
                p.nombre,
                p.categoria,
                p.unidad_medida,
                p.costo,
                COALESCE(ii.cantidad, 0)
                    + COALESCE(SUM(DISTINCT cd.cantidad), 0)
                    - COALESCE(SUM(DISTINCT vd.cantidad), 0) AS stock_actual,
                (COALESCE(ii.cantidad, 0)
                    + COALESCE(SUM(DISTINCT cd.cantidad), 0)
                    - COALESCE(SUM(DISTINCT vd.cantidad), 0))
                    * p.costo AS valorizacion
            FROM producto p
            LEFT JOIN inventario_inicial ii ON p.id_producto = ii.id_producto
            LEFT JOIN compra_detalle cd     ON p.id_producto = cd.id_producto
            LEFT JOIN venta_detalle vd      ON p.id_producto = vd.id_producto
            WHERE p.activo = 1
            GROUP BY p.id_producto, p.nombre, p.categoria,
                     p.unidad_medida, p.costo, ii.cantidad
            ORDER BY p.categoria, p.nombre
        """).fetchall()

def get_movimientos(id_producto):
    with get_connection() as conn:
        return conn.execute("""
            SELECT
                fecha_venta  AS fecha,
                'Salida'     AS tipo,
                p.nombre     AS producto,
                vd.cantidad,
                vd.precio_unitario AS precio_costo
            FROM venta_detalle vd
            JOIN venta_cabecera vc ON vd.id_venta    = vc.id_venta
            JOIN producto p        ON vd.id_producto = p.id_producto
            WHERE vd.id_producto = ?

            UNION ALL

            SELECT
                fecha_compra AS fecha,
                'Entrada'    AS tipo,
                p.nombre     AS producto,
                cd.cantidad,
                cd.costo_unitario AS precio_costo
            FROM compra_detalle cd
            JOIN compra_cabecera cc ON cd.id_compra   = cc.id_compra
            JOIN producto p         ON cd.id_producto = p.id_producto
            WHERE cd.id_producto = ?

            ORDER BY fecha DESC
        """, (id_producto, id_producto)).fetchall()