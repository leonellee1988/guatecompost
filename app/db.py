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