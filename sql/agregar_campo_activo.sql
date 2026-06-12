-- ============================================================
--  GuateCompost ERP — Agregar campo activo a tablas maestro
--  Autor: Edwin Lee Tiño
--  Versión: 1.0 | 2026
-- ============================================================

ALTER TABLE producto  ADD COLUMN activo INTEGER NOT NULL DEFAULT 1;
ALTER TABLE cliente   ADD COLUMN activo INTEGER NOT NULL DEFAULT 1;
ALTER TABLE proveedor ADD COLUMN activo INTEGER NOT NULL DEFAULT 1;
ALTER TABLE insumo    ADD COLUMN activo INTEGER NOT NULL DEFAULT 1;