# ============================================================
#  LEERP — Exportador SQLite → Google Sheets
#  Autor: Edwin Lee Tiño
# ============================================================
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import sqlite3
import os
from datetime import date, timedelta

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

# ─── UTILIDAD BASE ───────────────────────────────────────────
def exportar_hoja(gc, sheet, nombre_hoja, df):
    """Recibe un DataFrame y lo sube a la hoja indicada."""
    try:
        ws = sheet.worksheet(nombre_hoja)
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=nombre_hoja, rows=5000, cols=30)

    if df.empty:
        ws.update([df.columns.tolist()])
        print(f"⚠️  {nombre_hoja} — sin datos (encabezados exportados)")
        return

    ws.update([df.columns.tolist()] + df.values.tolist())
    print(f"✅  {nombre_hoja} — {len(df)} filas exportadas")

def query_to_df(conn, sql):
    return pd.read_sql_query(sql, conn)

# ─── TABLAS MAESTRAS ─────────────────────────────────────────
def exportar_maestras(gc, sheet, conn):
    print("\n📋 Exportando tablas maestras...")

    exportar_hoja(gc, sheet, "M_Producto", query_to_df(conn, """
        SELECT
            id_producto,
            nombre,
            descripcion,
            categoria,
            unidad_medida,
            costo,
            precio,
            activo
        FROM producto
        ORDER BY categoria, nombre
    """))

    exportar_hoja(gc, sheet, "M_Cliente", query_to_df(conn, """
        SELECT
            id_cliente,
            nombre,
            nit,
            telefono,
            correo,
            direccion,
            activo
        FROM cliente
        ORDER BY nombre
    """))

    exportar_hoja(gc, sheet, "M_Proveedor", query_to_df(conn, """
        SELECT
            id_proveedor,
            nombre,
            contacto,
            nit,
            telefono,
            correo,
            direccion,
            activo
        FROM proveedor
        ORDER BY nombre
    """))

    exportar_hoja(gc, sheet, "M_Insumo", query_to_df(conn, """
        SELECT
            id_insumo,
            nombre,
            descripcion,
            unidad_medida,
            costo,
            activo
        FROM insumo
        ORDER BY nombre
    """))

# ─── TABLAS TRANSACCIONALES ──────────────────────────────────
def exportar_ventas(gc, sheet, conn):
    print("\n💰 Exportando ventas...")

    exportar_hoja(gc, sheet, "T_Venta_Cabecera", query_to_df(conn, """
        SELECT
            vc.id_venta,
            vc.fecha_venta,
            c.nombre        AS cliente,
            c.id_cliente
        FROM venta_cabecera vc
        JOIN cliente c ON vc.id_cliente = c.id_cliente
        ORDER BY vc.fecha_venta DESC
    """))

    exportar_hoja(gc, sheet, "T_Venta_Detalle", query_to_df(conn, """
        SELECT
            vd.id_venta,
            vc.fecha_venta,
            c.nombre        AS cliente,
            c.id_cliente,
            p.id_producto,
            p.nombre        AS producto,
            p.categoria,
            p.unidad_medida,
            vd.cantidad,
            vd.precio_unitario,
            vd.cantidad * vd.precio_unitario AS subtotal
        FROM venta_detalle vd
        JOIN venta_cabecera vc ON vd.id_venta    = vc.id_venta
        JOIN cliente c         ON vc.id_cliente  = c.id_cliente
        JOIN producto p        ON vd.id_producto = p.id_producto
        ORDER BY vc.fecha_venta DESC
    """))

def exportar_compras(gc, sheet, conn):
    print("\n🛒 Exportando compras...")

    exportar_hoja(gc, sheet, "T_Compra_Cabecera", query_to_df(conn, """
        SELECT
            cc.id_compra,
            cc.fecha_compra,
            pr.nombre       AS proveedor,
            pr.id_proveedor
        FROM compra_cabecera cc
        JOIN proveedor pr ON cc.id_proveedor = pr.id_proveedor
        ORDER BY cc.fecha_compra DESC
    """))

    exportar_hoja(gc, sheet, "T_Compra_Detalle", query_to_df(conn, """
        SELECT
            cd.id_compra,
            cc.fecha_compra,
            pr.nombre       AS proveedor,
            pr.id_proveedor,
            p.id_producto,
            p.nombre        AS producto,
            p.categoria,
            p.unidad_medida,
            cd.cantidad,
            cd.costo_unitario,
            cd.cantidad * cd.costo_unitario AS subtotal
        FROM compra_detalle cd
        JOIN compra_cabecera cc ON cd.id_compra   = cc.id_compra
        JOIN proveedor pr       ON cc.id_proveedor = pr.id_proveedor
        JOIN producto p         ON cd.id_producto  = p.id_producto
        ORDER BY cc.fecha_compra DESC
    """))

def exportar_gastos(gc, sheet, conn):
    print("\n📑 Exportando gastos...")

    exportar_hoja(gc, sheet, "T_Gasto_Cabecera", query_to_df(conn, """
        SELECT
            gc.id_gasto,
            gc.fecha_gasto,
            gc.descripcion,
            pr.nombre       AS proveedor,
            pr.id_proveedor
        FROM gasto_cabecera gc
        JOIN proveedor pr ON gc.id_proveedor = pr.id_proveedor
        ORDER BY gc.fecha_gasto DESC
    """))

    exportar_hoja(gc, sheet, "T_Gasto_Detalle", query_to_df(conn, """
        SELECT
            gd.id_gasto,
            gc.fecha_gasto,
            gc.descripcion,
            pr.nombre       AS proveedor,
            pr.id_proveedor,
            i.id_insumo,
            i.nombre        AS insumo,
            i.unidad_medida,
            gd.cantidad,
            gd.costo_unitario,
            gd.cantidad * gd.costo_unitario AS subtotal
        FROM gasto_detalle gd
        JOIN gasto_cabecera gc ON gd.id_gasto  = gc.id_gasto
        JOIN proveedor pr      ON gc.id_proveedor = pr.id_proveedor
        JOIN insumo i          ON gd.id_insumo = i.id_insumo
        ORDER BY gc.fecha_gasto DESC
    """))

def exportar_consolidado_temporal(gc, sheet, conn):
    print("\n📊 Exportando consolidado temporal...")

    exportar_hoja(gc, sheet, "A_Consolidado_Temporal", query_to_df(conn, """
        SELECT
            fecha,
            strftime('%Y-%m', fecha)  AS mes_anio,
            strftime('%Y', fecha)     AS anio,
            tipo,
            SUM(monto)                AS total
        FROM (
            SELECT
                vc.fecha_venta              AS fecha,
                'Venta'                     AS tipo,
                vd.cantidad * vd.precio_unitario AS monto
            FROM venta_detalle vd
            JOIN venta_cabecera vc ON vd.id_venta = vc.id_venta

            UNION ALL

            SELECT
                cc.fecha_compra             AS fecha,
                'Compra'                    AS tipo,
                cd.cantidad * cd.costo_unitario AS monto
            FROM compra_detalle cd
            JOIN compra_cabecera cc ON cd.id_compra = cc.id_compra

            UNION ALL

            SELECT
                gc.fecha_gasto              AS fecha,
                'Gasto'                     AS tipo,
                gd.cantidad * gd.costo_unitario AS monto
            FROM gasto_detalle gd
            JOIN gasto_cabecera gc ON gd.id_gasto = gc.id_gasto
        )
        GROUP BY mes_anio, tipo
        ORDER BY fecha, tipo
    """))

# ─── TABLA FECHA ─────────────────────────────────────────────
def generar_tabla_fecha(fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
    """
    Genera la dimensión tiempo completa entre dos fechas.
    Incluye todos los campos necesarios para Looker Studio.
    """
    dias = []
    actual = date.fromisoformat(fecha_inicio)
    fin    = date.fromisoformat(fecha_fin)

    MESES_ES = {
        1:'Enero', 2:'Febrero', 3:'Marzo',    4:'Abril',
        5:'Mayo',  6:'Junio',   7:'Julio',     8:'Agosto',
        9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'
    }
    DIAS_ES = {
        0:'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves',
        4:'Viernes', 5:'Sábado', 6:'Domingo'
    }

    while actual <= fin:
        dias.append({
            # ── Claves
            "fecha":            actual.isoformat(),          # 2026-01-15
            "fecha_id":         int(actual.strftime("%Y%m%d")),  # 20260115

            # ── Día
            "dia":              actual.day,
            "dia_semana_num":   actual.weekday() + 1,        # 1=Lunes … 7=Domingo
            "dia_semana":       DIAS_ES[actual.weekday()],
            "es_fin_semana":    1 if actual.weekday() >= 5 else 0,

            # ── Semana
            "semana_anio":      actual.isocalendar()[1],     # Semana ISO 1-53
            "inicio_semana":    (actual - timedelta(days=actual.weekday())).isoformat(),

            # ── Mes
            "mes_num":          actual.month,
            "mes_nombre":       MESES_ES[actual.month],
            "mes_anio":         actual.strftime("%Y-%m"),    # 2026-01
            "trimestre":        (actual.month - 1) // 3 + 1,
            "trimestre_nombre": f"Q{(actual.month - 1) // 3 + 1} {actual.year}",

            # ── Año
            "anio":             actual.year,
            "semestre":         1 if actual.month <= 6 else 2,
        })
        actual += timedelta(days=1)

    return pd.DataFrame(dias)

def exportar_fecha(gc, sheet, conn):
    print("\n📅 Exportando dimensión fecha...")

    # Tomar rango dinámico desde los datos reales
    cursor = conn.execute("""
        SELECT MIN(fecha) AS f_min, MAX(fecha) AS f_max FROM (
            SELECT fecha_venta  AS fecha FROM venta_cabecera
            UNION ALL
            SELECT fecha_compra AS fecha FROM compra_cabecera
            UNION ALL
            SELECT fecha_gasto  AS fecha FROM gasto_cabecera
        )
    """)
    row = cursor.fetchone()

    # Extender 1 mes antes y 1 mes después para tener contexto
    f_min = date.fromisoformat(row["f_min"]).replace(day=1)
    f_max = date.fromisoformat(row["f_max"])
    f_max = (f_max.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    df_fecha = generar_tabla_fecha(f_min.isoformat(), f_max.isoformat())
    exportar_hoja(gc, sheet, "D_Fecha", df_fecha)

# ─── EJECUCIÓN PRINCIPAL ─────────────────────────────────────
def exportar_todo():
    print("=" * 50)
    print("  LEERP — Exportación completa a Google Sheets")
    print("=" * 50)

    gc    = conectar_sheets()
    sheet = gc.open_by_key(SHEET_ID)
    conn  = conectar_sqlite()

    exportar_maestras(gc, sheet, conn)
    exportar_ventas(gc, sheet, conn)
    exportar_compras(gc, sheet, conn)
    exportar_gastos(gc, sheet, conn)
    exportar_fecha(gc, sheet, conn)
    exportar_consolidado_temporal(gc, sheet, conn)

    conn.close()
    print("\n" + "=" * 50)
    print("  ✅ Exportación completada exitosamente")
    print("=" * 50)

if __name__ == "__main__":
    exportar_todo()