# ============================================================
#  GuateCompost ERP — Módulo de Productos
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_productos, insert_producto, delete_producto

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("📦 Productos")
    st.markdown("""
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    if 'form_producto_count' not in st.session_state:
        st.session_state['form_producto_count'] = 0

    tab1, tab2, tab3 = st.tabs(["📋 Catálogo", "➕ Nuevo Producto", "🗑️ Desactivar"])

    # ─── TAB 1: CATÁLOGO ─────────────────────────────────────

    with tab1:

        productos = get_productos()

        if not productos:
            st.warning("No hay productos registrados aún.")

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
                    "Jardín", "Agricultura", "Asesoría técnica", "Otro"
                ])
                unidad_medida = st.selectbox("Unidad de medida", options=[
                   "4 onzas", "8 onzas", "1 libra", "10 libras", "1 quintal", "1 litro", "4 litros", "20 litros", "Hora", "Unidad"
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
    
    # ─── TAB 3: DESACTIVAR ───────────────────────────────────
    with tab3:
        st.subheader("Desactivar producto")
        st.warning("El producto no se eliminará permanentemente. "
                "Solo dejará de aparecer en el sistema.")

        # Limpiar mensaje si el usuario NO viene de una acción en este tab
        if st.session_state.get("msg_desactivar") and not st.session_state.get("accion_desactivar"):
            st.session_state["msg_desactivar"] = None

        # Mostrar mensaje persistente si existe
        if st.session_state.get("msg_desactivar"):
            st.success(st.session_state["msg_desactivar"])
            st.session_state["msg_desactivar"] = None
            st.session_state["accion_desactivar"] = False  # Resetear bandera

        productos_lista = get_productos()
        if not productos_lista:
            st.info("No hay productos activos.")
        else:
            opciones = {p["nombre"]: p["id_producto"] for p in productos_lista}
            producto_sel = st.selectbox(
                "Seleccione el producto a desactivar",
                options=["— Seleccione un producto —"] + list(opciones.keys())
            )
            if producto_sel != "— Seleccione un producto —":
                st.error(f"¿Está seguro que desea desactivar **{producto_sel}**?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Sí, desactivar", key="btn_desactivar_producto"):
                        delete_producto(opciones[producto_sel])
                        st.session_state["msg_desactivar"] = f"Producto '{producto_sel}' desactivado correctamente."
                        st.session_state["accion_desactivar"] = True
                        st.rerun()
                with col2:
                    if st.button("❌ Cancelar", key="btn_cancelar_producto"):
                        st.rerun()