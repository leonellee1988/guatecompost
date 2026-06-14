# ============================================================
#  LEERP — Exportador SQLite → Google Sheets
#  Autor: Edwin Lee Tiño
# ============================================================

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sqlite3
import os

# ─── CONFIGURACIÓN ───────────────────────────────────────────

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

CREDENTIALS_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'config', 'credentials.json'
)

DB_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'guatecompost.db'
)

# ← Pega aquí el ID de tu Google Sheet
SHEET_ID = "1aGr56_uuxYBke94A10_lyd2gwiFClJpBXJYTfHCYyEY"

# ─── CONEXIÓN ────────────────────────────────────────────────

def conectar_sheets():
    creds = Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return gspread.authorize(creds)

def conectar_sqlite():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ─── EXPORTAR ────────────────────────────────────────────────

def exportar_hoja(gc, sheet, nombre_hoja, query, conn):
    df = pd.read_sql_query(query, conn)
    try:
        ws = sheet.worksheet(nombre_hoja)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=nombre_hoja, rows=1000, cols=20)
    ws.update([df.columns.tolist()] + df.values.tolist())
    print(f"✅ {nombre_hoja} exportada — {len(df)} filas")

def exportar_todo():
    print("Conectando a Google Sheets...")
    gc     = conectar_sheets()
    sheet  = gc.open_by_key(SHEET_ID)
    conn   = conectar_sqlite()

    exportar_hoja(gc, sheet, "Ventas", """
        SELECT
            vc.id_venta,
            vc.fecha_venta,
            c.nombre AS cliente,
            p.nombre AS producto,
            p.categoria,
            vd.cantidad,
            vd.precio_unitario,
            vd.cantidad * vd.precio_unitario AS subtotal
        FROM venta_cabecera vc
        JOIN cliente c      ON vc.id_cliente  = c.id_cliente
        JOIN venta_detalle vd ON vc.id_venta  = vd.id_venta
        JOIN producto p     ON vd.id_producto = p.id_producto
        ORDER BY vc.fecha_venta DESC
    """, conn)

    exportar_hoja(gc, sheet, "Compras", """
        SELECT
            cc.id_compra,
            cc.fecha_compra,
            pr.nombre AS proveedor,
            p.nombre  AS producto,
            cd.cantidad,
            cd.costo_unitario,
            cd.cantidad * cd.costo_unitario AS subtotal
        FROM compra_cabecera cc
        JOIN proveedor pr    ON cc.id_proveedor = pr.id_proveedor
        JOIN compra_detalle cd ON cc.id_compra  = cd.id_compra
        JOIN producto p     ON cd.id_producto   = p.id_producto
        ORDER BY cc.fecha_compra DESC
    """, conn)

    exportar_hoja(gc, sheet, "Stock", """
        SELECT
            p.nombre,
            p.categoria,
            p.unidad_medida,
            p.costo,
            p.precio,
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
                 p.unidad_medida, p.costo, p.precio, ii.cantidad
        ORDER BY p.categoria, p.nombre
    """, conn)

    exportar_hoja(gc, sheet, "Gastos", """
        SELECT
            gc.id_gasto,
            gc.fecha_gasto,
            gc.descripcion,
            pr.nombre AS proveedor,
            i.nombre  AS insumo,
            gd.cantidad,
            gd.costo_unitario,
            gd.cantidad * gd.costo_unitario AS subtotal
        FROM gasto_cabecera gc
        JOIN proveedor pr  ON gc.id_proveedor = pr.id_proveedor
        JOIN gasto_detalle gd ON gc.id_gasto  = gd.id_gasto
        JOIN insumo i      ON gd.id_insumo    = i.id_insumo
        ORDER BY gc.fecha_gasto DESC
    """, conn)

    conn.close()
    print("\nExportación completada exitosamente.")

if __name__ == "__main__":
    exportar_todo()