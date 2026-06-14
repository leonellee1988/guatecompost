-- ============================================================
--  LEERP — Limpieza de datos de prueba
--  ⚠️  EJECUTAR SOLO EN AMBIENTE DE PRUEBAS
--  Autor: Edwin Lee Tiño
-- ============================================================

PRAGMA foreign_keys = OFF;

-- Transaccionales primero
DELETE FROM venta_detalle;
DELETE FROM venta_cabecera;
DELETE FROM compra_detalle;
DELETE FROM compra_cabecera;
DELETE FROM gasto_detalle;
DELETE FROM gasto_cabecera;
DELETE FROM inventario_inicial;

-- Maestros
DELETE FROM producto;
DELETE FROM cliente;
DELETE FROM proveedor;
DELETE FROM insumo;

-- Reiniciar contadores de IDs
DELETE FROM sqlite_sequence WHERE name IN (
    'producto', 'cliente', 'proveedor', 'insumo',
    'venta_cabecera', 'compra_cabecera', 'gasto_cabecera'
);

PRAGMA foreign_keys = ON;