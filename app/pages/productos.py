# ============================================================
#  GuateCompost ERP — Módulo de Productos
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_productos, insert_producto

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("📦 Productos")
    st.markdown("---")

    if 'form_producto_count' not in st.session_state:
        st.session_state['form_producto_count'] = 0

    tab1, tab2 = st.tabs(["📋 Catálogo", "➕ Nuevo Producto"])

    # ─── TAB 1: CATÁLOGO ─────────────────────────────────────

    with tab1:

        productos = get_productos()

        if not productos:
            st.warning("No hay productos registrados aún.")
            return

        datos = []
        for p in productos:
            datos.append({
                "Nombre":     p["nombre"],
                "Categoría":  p["categoria"]     or "—",
                "Unidad":     p["unidad_medida"]  or "—",
                "Costo (Q)":  f"Q {p['costo']:.2f}"  if p["costo"]  else "—",
                "Precio (Q)": f"Q {p['precio']:.2f}" if p["precio"] else "—",
                "Margen":     f"{((p['precio']-p['costo'])/p['precio']*100):.1f}%"
                              if p["precio"] and p["costo"] else "—"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de productos: {len(datos)}")

    # ─── TAB 2: NUEVO PRODUCTO ───────────────────────────────

    with tab2:

        if st.session_state.get('producto_guardado'):
            st.success(f"✅ Producto '{st.session_state['producto_nombre']}' registrado correctamente.")
            st.session_state['producto_guardado'] = False

        st.subheader("Registrar nuevo producto")

        form_key = f"form_producto_{st.session_state['form_producto_count']}"

        with st.form(form_key):

            col1, col2 = st.columns(2)

            with col1:
                nombre        = st.text_input("Nombre *", placeholder="Ej: Abono Orgánico Premium")
                categoria     = st.selectbox("Categoría", options=[
                    "Abono", "Foliar", "Compost", "Bioinsumo", "Fitosanitario", "Otro"
                ])
                unidad_medida = st.selectbox("Unidad de medida", options=[
                    "Saco 25kg", "Saco 20kg", "Saco 10kg", "Kilo", "Litro", "Unidad"
                ])

            with col2:
                descripcion = st.text_area("Descripción", placeholder="Descripción del producto")
                costo       = st.number_input("Costo (Q) *", min_value=0.0, step=0.50)
                precio      = st.number_input("Precio (Q) *", min_value=0.0, step=0.50)

            submitted = st.form_submit_button("💾 Guardar producto")

            if submitted:
                if not nombre:
                    st.error("El nombre del producto es obligatorio.")
                elif precio <= costo:
                    st.error("El precio debe ser mayor al costo.")
                else:
                    insert_producto(nombre, descripcion, categoria, unidad_medida, costo, precio)
                    st.session_state['producto_guardado']    = True
                    st.session_state['producto_nombre']      = nombre
                    st.session_state['form_producto_count'] += 1
                    st.rerun()