# ============================================================
#  GuateCompost ERP — Test de conexión Python → SQLite3
#  Autor: Edwin Lee Tiño
# ============================================================

import sqlite3
import os

# ─── CONEXIÓN ────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'guatecompost.db')
# print(f'La ruta de nuestra base de datos es: {DB_PATH}')

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# ─── CONSULTA 1: productos ────────────────────────────────────

print('\n Productos')
print('-' * 45)

cursor.execute("""
SELECT nombre, categoria, precio 
FROM producto
ORDER BY categoria, nombre
""")

for fila in cursor.fetchall():
    print(f'{fila['nombre']:<28} {fila['categoria']:<15} Q.{fila['precio']:.2f}')

# ─── CIERRE ───────────────────────────────────────────────────

conn.close()
print('\n Conexión cerrada correctamente.\n')