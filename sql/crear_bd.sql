-- ============================================================
--  GuateCompost ERP — Creación de base de datos
--  Autor: Edwin Lee Tiño
--  Versión: 1.0 | 2026
-- ============================================================

PRAGMA foreign_keys = ON;

-- ─── TABLAS MAESTRO ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS producto (
    id_producto   INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    descripcion   TEXT,
    categoria     TEXT,
    unidad_medida TEXT,
    costo         REAL,
    precio        REAL
);

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente    INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    nit           TEXT,
    telefono      TEXT,
    correo        TEXT,
    direccion     TEXT
);

CREATE TABLE IF NOT EXISTS proveedor (
    id_proveedor  INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    contacto      TEXT,
    nit           TEXT,
    telefono      TEXT,
    correo        TEXT,
    direccion     TEXT
);

CREATE TABLE IF NOT EXISTS insumo (
    id_insumo     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre        TEXT    NOT NULL,
    descripcion   TEXT,
    unidad_medida TEXT,
    costo         REAL
);

-- ─── CADENA COMERCIAL ────────────────────────────────────────

CREATE TABLE IF NOT EXISTS venta_cabecera (
    id_venta    INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_venta TEXT    NOT NULL,
    id_cliente  INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

CREATE TABLE IF NOT EXISTS venta_detalle (
    id_venta        INTEGER NOT NULL,
    id_producto     INTEGER NOT NULL,
    cantidad        REAL    NOT NULL,
    precio_unitario REAL    NOT NULL,
    PRIMARY KEY (id_venta, id_producto),
    FOREIGN KEY (id_venta)    REFERENCES venta_cabecera(id_venta),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE IF NOT EXISTS compra_cabecera (
    id_compra    INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_compra TEXT    NOT NULL,
    id_proveedor INTEGER NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);

CREATE TABLE IF NOT EXISTS compra_detalle (
    id_compra      INTEGER NOT NULL,
    id_producto    INTEGER NOT NULL,
    cantidad       REAL    NOT NULL,
    costo_unitario REAL    NOT NULL,
    PRIMARY KEY (id_compra, id_producto),
    FOREIGN KEY (id_compra)   REFERENCES compra_cabecera(id_compra),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- ─── CADENA DE GASTOS OPERATIVOS ─────────────────────────────

CREATE TABLE IF NOT EXISTS gasto_cabecera (
    id_gasto     INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_gasto  TEXT    NOT NULL,
    id_proveedor INTEGER NOT NULL,
    descripcion  TEXT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
);

CREATE TABLE IF NOT EXISTS gasto_detalle (
    id_gasto       INTEGER NOT NULL,
    id_insumo      INTEGER NOT NULL,
    cantidad       REAL    NOT NULL,
    costo_unitario REAL    NOT NULL,
    PRIMARY KEY (id_gasto, id_insumo),
    FOREIGN KEY (id_gasto)   REFERENCES gasto_cabecera(id_gasto),
    FOREIGN KEY (id_insumo)  REFERENCES insumo(id_insumo)
);

-- ─── INVENTARIO ──────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS inventario_inicial (
    id_producto  INTEGER PRIMARY KEY,
    cantidad     REAL    NOT NULL,
    fecha_corte  TEXT    NOT NULL,
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);