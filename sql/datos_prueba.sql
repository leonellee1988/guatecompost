-- ============================================================
--  GuateCompost ERP — Datos de prueba
--  Autor: Edwin Lee Tiño
--  Versión: 1.0 | 2026
-- ============================================================

PRAGMA foreign_keys = ON;

-- ─── PRODUCTOS ───────────────────────────────────────────────

INSERT INTO producto (nombre, descripcion, categoria, unidad_medida, costo, precio) VALUES
('Abono Orgánico Premium',   'Compost maduro de alta calidad, ideal para hortalizas',         'Abono',       'Saco 25kg', 45.00,  75.00),
('Humus de Lombriz',         'Abono orgánico de lombriz roja californiana',                   'Abono',       'Saco 10kg', 38.00,  65.00),
('Fertilizante Foliar',      'Solución nutritiva para aplicación directa en hojas',           'Foliar',      'Litro',     22.00,  40.00),
('Bocashi Fermentado',       'Abono fermentado de origen japonés, acción rápida',             'Abono',       'Saco 20kg', 40.00,  68.00),
('Compost Estabilizado',     'Materia orgánica descompuesta, mejora estructura del suelo',    'Compost',     'Saco 25kg', 35.00,  58.00),
('Té de Compost',            'Extracto líquido bioactivo para fertirrigación',                'Foliar',      'Litro',     18.00,  35.00),
('Micorrizas en Polvo',      'Hongos benéficos que mejoran absorción de nutrientes',          'Bioinsumo',   'Kilo',      55.00,  95.00),
('Caldo Bordelés',           'Fungicida natural a base de cobre y cal',                      'Fitosanitario','Litro',    20.00,  38.00);

-- ─── CLIENTES ────────────────────────────────────────────────

INSERT INTO cliente (nombre, nit, telefono, correo, direccion) VALUES
('Finca San Isidro',         '1234567-8', '55551001', 'finca.sanisidro@gmail.com',    'Km 45, Carretera a Escuintla'),
('Vivero El Jardín',         '2345678-9', '55552002', 'vivero.eljardin@gmail.com',    '3a Calle 12-45, Zona 1, Chimaltenango'),
('Cooperativa Agrícola Maya','3456789-0', '55553003', 'coopagri.maya@outlook.com',    'Aldea San Juan, San Marcos'),
('Huerta Familiar López',    '4567890-1', '55554004', 'huertalopez@gmail.com',        'Colonia El Maestro, Mazatenango'),
('Agro Servicios del Norte', '5678901-2', '55555005', 'agroservnorte@gmail.com',      'Zona 3, Cobán, Alta Verapaz'),
('Proyecto Orgánico USAC',   '6789012-3', '55556006', 'proyorg.usac@usac.edu.gt',     'Ciudad Universitaria, Zona 12, Guatemala');

-- ─── PROVEEDORES ─────────────────────────────────────────────

INSERT INTO proveedor (nombre, contacto, nit, telefono, correo, direccion) VALUES
('BioInsumos Guatemala',  'Carlos Monterroso', '9876543-2', '24441001', 'ventas@bioinsumos.gt',     'Zona 10, Guatemala Ciudad'),
('Orgánicos del Altiplano','María Ajú',        '8765432-1', '77782001', 'contacto@orgaltiplano.com','Quetzaltenango, Zona 3'),
('AgroNatural S.A.',      'Roberto Cifuentes', '7654321-0', '24443001', 'rcifuentes@agronatural.gt','Escuintla, Calle Principal');

-- ─── INSUMOS ─────────────────────────────────────────────────

INSERT INTO insumo (nombre, descripcion, unidad_medida, costo) VALUES
('Papel bond carta',     'Resma 500 hojas',                      'Resma',  45.00),
('Tinta negra impresora','Cartucho compatible HP',               'Unidad',  85.00),
('Bolsas plásticas',     'Bolsas para empaque de productos',     'Ciento',  30.00),
('Folder manila',        'Folder tamaño carta',                  'Unidad',   1.50),
('Lapiceros azules',     'Caja de lapiceros',                    'Caja',    18.00),
('Cinta adhesiva',       'Rollo transparente para empaque',      'Rollo',    8.00);

-- ─── INVENTARIO INICIAL ──────────────────────────────────────

INSERT INTO inventario_inicial (id_producto, cantidad, fecha_corte) VALUES
(1, 50.0, '2026-01-01'),
(2, 30.0, '2026-01-01'),
(3, 40.0, '2026-01-01'),
(4, 25.0, '2026-01-01'),
(5, 60.0, '2026-01-01'),
(6, 35.0, '2026-01-01'),
(7, 15.0, '2026-01-01'),
(8, 20.0, '2026-01-01');

-- ─── COMPRAS ─────────────────────────────────────────────────

INSERT INTO compra_cabecera (fecha_compra, id_proveedor) VALUES
('2026-01-10', 1),
('2026-02-05', 2),
('2026-03-12', 3);

INSERT INTO compra_detalle (id_compra, id_producto, cantidad, costo_unitario) VALUES
(1, 1, 30.0, 45.00),
(1, 3, 20.0, 22.00),
(1, 7, 10.0, 55.00),
(2, 2, 25.0, 38.00),
(2, 4, 20.0, 40.00),
(2, 5, 30.0, 35.00),
(3, 6, 25.0, 18.00),
(3, 8, 15.0, 20.00);

-- ─── VENTAS ──────────────────────────────────────────────────

INSERT INTO venta_cabecera (fecha_venta, id_cliente) VALUES
('2026-01-15', 1),
('2026-01-22', 2),
('2026-02-03', 3),
('2026-02-18', 1),
('2026-03-05', 4),
('2026-03-14', 5),
('2026-03-28', 6);

INSERT INTO venta_detalle (id_venta, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 10.0, 75.00),
(1, 3,  5.0, 40.00),
(2, 2,  8.0, 65.00),
(2, 5, 12.0, 58.00),
(3, 4, 15.0, 68.00),
(3, 7,  3.0, 95.00),
(4, 1, 20.0, 75.00),
(4, 6, 10.0, 35.00),
(5, 3, 18.0, 40.00),
(5, 8,  7.0, 38.00),
(6, 2, 10.0, 65.00),
(6, 5, 15.0, 58.00),
(7, 1, 12.0, 75.00),
(7, 4,  8.0, 68.00);

-- ─── GASTOS OPERATIVOS ───────────────────────────────────────

INSERT INTO gasto_cabecera (fecha_gasto, id_proveedor, descripcion) VALUES
('2026-01-08', 1, 'Compra de papelería enero'),
('2026-02-10', 2, 'Insumos de oficina febrero'),
('2026-03-06', 3, 'Reposición materiales empaque');

INSERT INTO gasto_detalle (id_gasto, id_insumo, cantidad, costo_unitario) VALUES
(1, 1, 2.0, 45.00),
(1, 2, 1.0, 85.00),
(1, 4, 10.0, 1.50),
(2, 5, 3.0, 18.00),
(2, 6, 5.0,  8.00),
(3, 3, 4.0, 30.00),
(3, 6, 3.0,  8.00);