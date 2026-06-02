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