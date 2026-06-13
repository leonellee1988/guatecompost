# ============================================================
#  GuateCompost ERP — Punto de entrada
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st

# ─── CONFIGURACIÓN DE PÁGINA ─────────────────────────────────

st.set_page_config(
    page_title="GuateCompost ERP",
    page_icon="🌱",
    layout="wide"
)

# Ocultar menú automático de Streamlit
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# ─── MENÚ LATERAL ────────────────────────────────────────────

st.sidebar.title("🌱 GuateCompost ERP")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegación",
    options=["Inicio", "Productos", "Clientes", "Proveedores", "Insumos", "Ventas", "Compras", "Gastos", 'Inventarios']
)

# ─── CONTENIDO POR PÁGINA ────────────────────────────────────

if pagina == "Inicio":

    st.title("Bienvenido a GuateCompost ERP")
    st.markdown("Gestión simple para decisiones inteligentes.")
    st.markdown("---")

    # Primera fila

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("📦 **Productos**  \nCatálogo de productos")

    with col2:
        st.info("👥 **Clientes**  \nGestión de clientes activos")
    
    with col3:
        st.info("✏️ **Insumos**   \nCatálogo de insumos")
    
    with col4:
        st.info("🏷️ **Proveedores**   \nBase de datos de proveedores")

    st.markdown(" ")

    # Segunda fila

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.info("💰 **Ventas**  \nIngreso de transacciones de venta")
    
    with col6:
        st.info("🛒 **Compras**   \nRegistro de compras de productos")

    with col7:
        st.info("🛍️ **Compras insumos**   \nRegistro de adquisiciones de insumos")
    
    with col8:
        st.info("📋 **Inventarios**   \nInventario de productos terminados")

elif pagina == "Productos":
    from pages import productos
    productos.mostrar()

elif pagina == "Clientes":
    from pages import clientes
    clientes.mostrar()

elif pagina == "Proveedores":
    from pages import proveedores
    proveedores.mostrar()

elif pagina == "Insumos":
    from pages import insumos
    insumos.mostrar()

elif pagina == "Ventas":
    from pages import ventas
    ventas.mostrar()

elif pagina == "Compras":
    from pages import compras
    compras.mostrar()

elif pagina == "Gastos":
    from pages import gastos
    gastos.mostrar()

elif pagina == "Inventarios":
    from pages import inventarios
    inventarios.mostrar()