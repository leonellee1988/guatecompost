# ============================================================
#  GuateCompost ERP — Punto de entrada
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st

# ─── CONFIGURACIÓN DE PÁGINA ─────────────────────────────────
st.set_page_config(
    page_title="LEERP",
    page_icon="⚙️",
    layout="wide"
)

# ─── CSS GLOBAL  ─────────────────────────────────────────────
st.markdown("""
    <style>
    /* Ocultar nav automático */
    [data-testid="stSidebarNav"] { display: none; }

    /* Reducir padding global del contenedor */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Reducir espacio del header de Streamlit */
    [data-testid="stHeader"] {
        height: 0rem !important;
        min-height: 0rem !important;
    }

    /* Panels */
    .panel-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 14px;
    }
    .panel {
        background-color: #1e3a5f;
        border-radius: 10px;
        padding: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: left;
        cursor: pointer;
    }
    .panel:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        background-color: #254e7a;
    }
    .panel-emoji  { font-size: 1.6rem; }
    .panel-titulo {
        color: #5dade2;
        font-weight: bold;
        font-size: 1rem;
        margin: 6px 0 4px 0;
    }
    .panel-desc { color: #aab7c4; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# ─── MENÚ LATERAL ────────────────────────────────────────────
st.sidebar.title("⚙️ LEERP")
st.sidebar.markdown("<hr style='margin-top: 0rem; margin-bottom: 0rem;'>", unsafe_allow_html=True)

# Inicializar página en session_state
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Inicio"

def nav_button(label, key):
    """Botón de navegación que resalta si está activo."""
    is_active = st.session_state["pagina"] == label
    btn_style = "primary" if is_active else "secondary"
    if st.sidebar.button(label, key=key, type=btn_style, use_container_width=True):
        st.session_state["pagina"] = label
        st.rerun()

st.sidebar.markdown("##### 🏠 General")
nav_button("Inicio", "btn_inicio")

st.sidebar.markdown("##### 📑 Maestros")
nav_button("Productos",   "btn_productos")
nav_button("Clientes",    "btn_clientes")
nav_button("Proveedores", "btn_proveedores")
nav_button("Insumos",     "btn_insumos")

st.sidebar.markdown("##### 💳 Transacciones")
nav_button("Ventas",   "btn_ventas")
nav_button("Compras",  "btn_compras")
nav_button("Gastos",   "btn_gastos")

st.sidebar.markdown("##### 📊 Inventario")
nav_button("Inventarios", "btn_inventarios")

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='padding: 10px 0; text-align: center;'>
        <p style='color: #5dade2; font-weight: bold; 
                  margin-bottom: 2px; font-size: 0.85rem;'>
            ⚙️ LEERP v1.0
        </p>
        <p style='color: #aab7c4; font-size: 0.75rem; margin-bottom: 2px;'>
            Desarrollado por
        </p>
        <p style='color: #ffffff; font-weight: bold; 
                  font-size: 0.85rem; margin-bottom: 2px;'>
            Edwin Lee Tiño
        </p>
        <p style='color: #aab7c4; font-size: 0.75rem; margin-bottom: 6px;'>
            BI & Data Analytics
        </p>
        <a href='mailto:leonellee1988@tutamail.com' 
           style='color: #5dade2; font-size: 0.75rem;'>
            📧 Contáctame
        </a>
    </div>
""", unsafe_allow_html=True)

# ─── Leer página activa ───────────────────────────────────────
pagina = st.session_state["pagina"]

# ─── CONTENIDO POR PÁGINA ────────────────────────────────────

if pagina == "Inicio":

    st.title("Bienvenido a LEERP")
    st.markdown("""
    <p style='margin-bottom: 0.3rem;'>
    Gestión simple para decisiones inteligentes.</p>
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    # Configuración de los paneles 
    st.markdown("""
    <style>
    .panel-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 20px;
    }
    .panel {
        background-color: #1e3a5f;
        border-radius: 10px;
        padding: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: left;
    }
    .panel:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        background-color: #254e7a;
    }
    .panel-emoji  { font-size: 1.6rem; }
    .panel-titulo {
        color: #5dade2;
        font-weight: bold;
        font-size: 1rem;
        margin: 6px 0 4px 0;
    }
    .panel-desc { color: #aab7c4; font-size: 0.85rem; }
    </style>

    <div class="panel-grid">
        <div class="panel">
            <div class="panel-emoji">📦</div>
            <div class="panel-titulo">Productos</div>
            <div class="panel-desc">Catálogo de productos disponibles</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">👥</div>
            <div class="panel-titulo">Clientes</div>
            <div class="panel-desc">Gestión de clientes activos</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">✏️</div>
            <div class="panel-titulo">Insumos</div>
            <div class="panel-desc">Catálogo de insumos operativos</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">🚚</div>
            <div class="panel-titulo">Proveedores</div>
            <div class="panel-desc">Gestión de proveedores activos</div>
        </div>
    </div>

    <div class="panel-grid">
        <div class="panel">
            <div class="panel-emoji">💰</div>
            <div class="panel-titulo">Ventas</div>
            <div class="panel-desc">Ingreso de transacciones de venta</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">🛒</div>
            <div class="panel-titulo">Compras</div>
            <div class="panel-desc">Registro de compras de productos</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">🛍️</div>
            <div class="panel-titulo">Compras Insumos</div>
            <div class="panel-desc">Registro de adquisiciones de insumos</div>
        </div>
        <div class="panel">
            <div class="panel-emoji">📊</div>
            <div class="panel-titulo">Inventarios</div>
            <div class="panel-desc">Stock y valorización de productos</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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