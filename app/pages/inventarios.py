# ============================================================
#  GuateCompost ERP — Módulo de Inventarios
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_stock_actual, get_movimientos, get_productos

STOCK_MINIMO = 10  # Umbral provisional — definir con cliente

def mostrar():

    st.title("📊 Inventarios")
    st.markdown("""
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📦 Stock Actual",
        "📈 Movimientos",
        "💵 Valorización"
    ])

    # ─── TAB 1: STOCK ACTUAL ─────────────────────────────────

    with tab1:

        st.subheader("Stock actual por producto")

        stock = get_stock_actual()

        if not stock:
            st.warning("No hay productos registrados.")

        # Métricas resumen
        total_productos  = len(stock)
        bajo_minimo      = sum(1 for s in stock if s["stock_actual"] < STOCK_MINIMO)
        valorizacion_total = sum(s["valorizacion"] for s in stock)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total productos", total_productos)
        with col2:
            st.metric("Bajo mínimo", bajo_minimo, delta=f"-{bajo_minimo}" if bajo_minimo > 0 else None)
        with col3:
            st.metric("Valorización total", f"Q {valorizacion_total:,.2f}")

        st.markdown("---")

        # Tabla de stock
        datos = []
        for s in stock:
            alerta = "🔴 Bajo" if s["stock_actual"] < STOCK_MINIMO else "🟢 OK"
            datos.append({
                "Producto":      s["nombre"],
                "Categoría":     s["categoria"]    or "—",
                "Unidad":        s["unidad_medida"] or "—",
                "Stock":         round(s["stock_actual"], 2),
                "Estado":        alerta,
                "Valorización":  f"Q {s['valorizacion']:,.2f}"
            })

        st.dataframe(datos, width='stretch', hide_index=True)

    # ─── TAB 2: MOVIMIENTOS ──────────────────────────────────

    with tab2:

        st.subheader("Movimientos por producto")

        productos = get_productos()

        if not productos:
            st.warning("No hay productos registrados.")

        opciones = {p["nombre"]: p["id_producto"] for p in productos}

        producto_sel = st.selectbox(
            "Seleccione un producto",
            options=["— Seleccione un producto —"] + list(opciones.keys())
        )

        if producto_sel != "— Seleccione un producto —":

            movimientos = get_movimientos(opciones[producto_sel])

            if not movimientos:
                st.info("Este producto no tiene movimientos registrados.")
            else:
                datos = []
                for m in movimientos:
                    datos.append({
                        "Fecha":        m["fecha"],
                        "Tipo":         m["tipo"],
                        "Cantidad":     m["cantidad"],
                        "Precio/Costo": f"Q {m['precio_costo']:,.2f}",
                        "Total":        f"Q {m['cantidad'] * m['precio_costo']:,.2f}"
                    })

                # Resumen entradas vs salidas
                entradas = sum(m["cantidad"] for m in movimientos if m["tipo"] == "Entrada")
                salidas  = sum(m["cantidad"] for m in movimientos if m["tipo"] == "Salida")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total entradas", round(entradas, 2))
                with col2:
                    st.metric("Total salidas", round(salidas, 2))
                with col3:
                    st.metric("Balance", round(entradas - salidas, 2))

                st.markdown("---")
                st.dataframe(datos, width='stretch', hide_index=True)

    # ─── TAB 3: VALORIZACIÓN ─────────────────────────────────

    with tab3:

        st.subheader("Valorización del inventario")
        st.caption("Stock actual de cada producto multiplicado por su costo unitario.")

        stock = get_stock_actual()

        if not stock:
            st.warning("No hay productos registrados.")
            return

        datos = []
        for s in stock:
            datos.append({
                "Producto":      s["nombre"],
                "Categoría":     s["categoria"] or "—",
                "Stock":         round(s["stock_actual"], 2),
                "Costo unit.":   f"Q {s['costo']:,.2f}",
                "Valorización":  f"Q {s['valorizacion']:,.2f}"
            })

        # Total general
        total = sum(s["valorizacion"] for s in stock)
        st.metric("Valorización total del inventario", f"Q {total:,.2f}")
        st.markdown("---")
        st.dataframe(datos, width='stretch', hide_index=True)