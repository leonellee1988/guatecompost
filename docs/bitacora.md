# Bitácora del Proyecto — GuateCompost ERP

## 2026
### Sesión 1
- Definición del alcance: ERP de distribución para cliente de compostaje
- Diseño del modelo de datos: 11 tablas normalizadas
- Herramientas seleccionadas: SQLite3, Python, Streamlit, Looker Studio
- Decisión: inventario calculado (stock = inventario_inicial + compras - ventas)
- Decisión: arquitectura local, un solo usuario
- ERD documentado en dbdiagram.io → exportado a docs/erd.png
- Base de datos creada exitosamente con crear_bd.sql

### Sesión 2
- Datos de prueba cargados con datos_prueba.sql (8 productos, 6 clientes,
  3 proveedores, 6 insumos, 3 compras, 7 ventas, 3 gastos operativos)
- Validadas 3 consultas SQL de negocio: ventas por cliente, stock actual
  y margen bruto por producto
- Conexión Python → SQLite3 establecida con librería nativa sqlite3
- Conceptos aprendidos: connection, cursor, fetchall(), row_factory,
  rutas relativas con os.path.join, formato de columnas en f-strings
- Archivo creado: app/test_conexion.py

### Sesión 3
- Entorno virtual creado con venv y activado correctamente
- .gitignore configurado en raíz del proyecto
- Streamlit instalado y configurado
- Arquitectura de la app definida: main.py + db.py + pages/
- main.py creado: navegación lateral, pantalla de inicio con columnas
- db.py creado: capa de datos con get_connection(), get_productos(),
  insert_producto(), get_clientes(), insert_cliente()
- Módulo productos.py creado: catálogo con margen calculado y
  formulario de ingreso con validaciones
- Conceptos aprendidos: st.tabs, st.form, st.rerun(), st.columns,
  context manager, parámetros seguros con ? (prevención SQL Injection)
- Decisión: navegación centralizada en main.py, menú automático
  de Streamlit ocultado con CSS
- Producto de prueba agregado y verificado en la BD exitosamente

### Sesión 4
- Módulo clientes.py creado siguiendo patrón consistente con productos.py
- Bug resuelto: formulario limpio después de guardar con key dinámico
  en st.form (form_cliente_count / form_producto_count)
- Bug resuelto: mensaje de éxito ubicado en tab2 donde está el usuario
- Decisión de diseño: no regresar al pool automáticamente después de
  guardar — el usuario navega manualmente al catálogo
- Decisión de diseño: patrón consistente entre módulos — misma
  estructura, mismas inicializaciones, misma mecánica
- Concepto aprendido: session_state — memoria de Streamlit entre
  recargas, clave para controlar formularios y mensajes
- Concepto aprendido: separación de responsabilidades — db.py maneja
  datos, pages/ maneja interfaz. Si migras de SQLite3 a PostgreSQL,
  solo cambias db.py
- Limpieza de código muerto: botón duplicado y producto_tab_activo
  eliminados de productos.py

  ### Sesión 5
- Módulos proveedores.py e insumos.py creados de forma autónoma
  por Edwin — primer ejercicio independiente exitoso
- Bugs corregidos en db.py: conn.commit() fuera del with en
  insert_proveedor() e insert_insumo(), comas faltantes en VALUES
  de insert_insumo()
- Correcciones menores en proveedores.py: guiones "—" consistentes,
  typo en mensaje de warning
- main.py actualizado: pantalla de inicio rediseñada en 2 filas de 4
  módulos (Productos, Clientes, Insumos, Proveedores / Ventas,
  Compras, Compras Insumos, Inventarios)
- Concepto aprendido: las columnas de Streamlit en bloques separados
  requieren variables diferentes para evitar conflicto de context manager
- Decisión: el desarrollador no necesita dominar el 100% del código UI —
  el foco de aprendizaje está en db.py y las consultas SQL

  ### Sesión 6
- Módulo ventas.py creado: el más complejo del sistema
- Patrón cabecera/detalle implementado con dos formularios separados
- Concepto aprendido: cursor.lastrowid — obtener el ID recién 
  generado para vincular cabecera y detalle en la misma transacción
- Concepto aprendido: diccionario por comprensión para convertir
  listas de BD en opciones legibles para selectbox
- Concepto aprendido: any() para validar duplicados en listas
- Bug resuelto: UNIQUE constraint — la BD rechazó correctamente
  productos duplicados en el mismo detalle
- Bug resuelto: precio no editable dentro de st.form — solución:
  selector de producto fuera del form, precio_ref como valor inicial
- Bug resuelto: forms anidados — la indentación incorrecta metía
  el form del detalle dentro del form de la cabecera
- Bug resuelto: KeyError en form_detalle_count — inicialización
  movida al inicio de mostrar()
- Validaciones agregadas: producto no seleccionado, detalle vacío,
  cliente no seleccionado
- Decisión de diseño: precio sugerido del catálogo es editable —
  permite descuentos y negociación en tiempo real
- Concepto aprendido: la indentación en Python ES la estructura —
  una sangría incorrecta cambia completamente el comportamiento

  ### Sesión 7
- Módulo compras.py creado de forma autónoma por Edwin siguiendo
  patrón de ventas.py — cabecera/detalle con proveedor e insumos
- Módulo gastos.py creado de forma autónoma por Edwin —
  incluye campo descripcion en cabecera
- Bug resuelto: insert_gasto() faltaba parámetro descripcion —
  agregado al form de cabecera, session_state y llamada a la función
- Funcionalidad agregada: desactivar registros en todos los módulos
  maestros (producto, cliente, proveedor, insumo)
- Funcionalidad agregada: eliminar venta completa con DELETE en
  cascada — primero detalle, luego cabecera
- Funcionalidad agregada: eliminar línea de detalle durante ingreso
  usando list.pop(idx) sobre session_state — sin tocar la BD
- Concepto aprendido: enumerate() para identificar índice de cada
  ítem en una lista al renderizar botones por fila
- Concepto aprendido: soft delete vs hard delete — tablas maestro
  usan UPDATE activo=0, tablas transaccionales usan DELETE físico
- Concepto aprendido: ALTER TABLE ADD COLUMN para modificar tablas
  existentes sin perder datos — campo activo INTEGER DEFAULT 1
- Mejora UX: unidad de medida visible al seleccionar producto/insumo
  en ventas, compras y gastos
- SQL actualizado: todas las funciones get_() filtran WHERE activo=1
- Patrón de mensaje persistente con session_state consolidado en
  todos los módulos

  ### Sesión 8
- Módulo inventarios.py creado: tres vistas — Stock Actual,
  Movimientos y Valorización
- Funciones agregadas en db.py: get_stock_actual() con cálculo
  completo de stock e inventario_inicial + compras - ventas,
  get_movimientos() con UNION ALL para entradas y salidas,
  get_stock_producto() para validación en tiempo real
- Concepto aprendido: UNION ALL — combina dos consultas en una
  sola tabla de resultados sin eliminar duplicados
- Concepto aprendido: st.metric — widget para KPIs con valor
  grande, etiqueta y delta opcional
- Validación de negocio agregada en ventas.py: alerta visual
  de stock bajo/agotado al seleccionar producto, bloqueo de
  venta si cantidad supera stock disponible
- Concepto aprendido: validación en dos capas — visual
  (Streamlit) y lógica (Python) antes de escribir en BD
- Rediseño visual completo de main.py:
  - CSS global: padding, header, paneles hover
  - Paneles HTML con efecto hover — sin botones visibles
  - Sidebar reorganizado con grupos: General, Maestros,
    Transacciones, Inventario
  - Función nav_button() creada — botón activo resaltado
    en rojo con type="primary"
  - Sección "Desarrollado por Edwin Lee Tiño" en sidebar
- Decisión de marca: ERP renombrado a LEERP v1.0
- Decisión estratégica: LEERP como producto comercializable
  para micro y pequeñas empresas — modelo config.json por
  cliente pendiente de implementar
- Script sql/limpiar_bd.sql creado para resetear datos de
  prueba — incluye limpieza de sqlite_sequence para reiniciar
  IDs desde 1
- Concepto aprendido: sqlite_sequence — tabla interna de
  SQLite que controla los contadores de AUTOINCREMENT
- Bug resuelto: return en tab1 cancelaba toda la función
  mostrar() cuando la BD estaba vacía — eliminado en todos
  los módulos maestros
- Prueba integral completada con datos reales — sistema
  estable y listo para siguiente fase

### Sesión 9
- Conexión Google Sheets establecida exitosamente
- APIs habilitadas en Google Cloud: Google Sheets API y Google Drive API
- Cuenta de servicio creada: leerp-sheets@chrome-epigram-259923.iam.gserviceaccount.com
- Credenciales JSON descargadas y almacenadas en config/credentials.json
- config/credentials.json agregado al .gitignore — nunca sube a GitHub
- Lección de seguridad: credenciales expuestas en chat → clave
  eliminada y regenerada inmediatamente
- Librerías instaladas: gspread, google-auth, pandas
- Script exportar_sheets.py creado con 4 hojas: Ventas, Compras,
  Stock y Gastos
- Concepto aprendido: pd.read_sql_query() — ejecuta una consulta
  SQL y devuelve un DataFrame de pandas listo para exportar
- Google Sheet creado: "LEERP - Dashboard" compartido con la
  cuenta de servicio como Editor
- Módulo dashboard.py creado con botón de sincronización
- Sincronización probada exitosamente — 4 hojas actualizadas
  en Google Sheets desde el ERP con un solo clic
- Datos de prueba v2 cargados: 10 productos, 5 clientes,
  5 proveedores, 10 insumos, inventario inicial, 50 compras,
  100 ventas, 20 gastos — período enero-junio 2026
- Script sql/limpiar_bd.sql creado para resetear datos
- Mockup del dashboard diseñado con pantone del portafolio
  de Edwin: navy #0A1628, blue #0070C0, lblue #90CDF4
- Decisión estratégica: guardar versión pre-dashboard en
  GitHub antes de construir Looker Studio

### Sesión 10
- Migración crítica: SQLite3 local → PostgreSQL en Neon (cloud)
- db.py refactorizado: conexión con psycopg2 y variables de entorno
- Archivo .env creado con credenciales de Neon
- .env agregado a .gitignore — credenciales nunca van a GitHub
- ERP desplegado en Streamlit Cloud — acceso desde cualquier
  dispositivo y sistema operativo
- Conexión directa Power BI → Neon PostgreSQL establecida
  exitosamente — eliminando la dependencia de Google Sheets
- Star Schema identificado como arquitectura correcta para
  el modelo de datos en Power BI: tablas de hechos (ventas,
  compras, gastos) + tablas de dimensión (fecha, producto,
  cliente, proveedor)
- Decisión: abandonar Google Sheets como intermediario —
  Power BI se conecta directamente a PostgreSQL
- Dashboard de ventas completado en Power BI con filtros
  interactivos de fecha, producto y cliente
- datos_prueba_v3.sql generado: 150 ventas, 60 compras,
  24 gastos — período Ene-Dic 2025 con ventas > compras
- Lección aprendida: el producto cartesiano en SQL causa
  inflación de datos — siempre preagregar con CTEs antes
  de hacer JOINs entre tablas de hechos diferentes
- Lección aprendida: Looker Studio requiere tabla de fechas
  y Star Schema para cruzar fuentes temporalmente —
  igual que Power BI