# ============================================================
#  GuateCompost ERP — Módulo de Insumos
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_insumos, insert_insumo

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("✏️ Insumos")
    st.markdown("---")

    if 'form_insumo_count' not in st.session_state:
        st.session_state['form_insumo_count'] = 0

    tab1, tab2 = st.tabs(["📋 Catálogo", "➕ Nuevo Insumo"])

    # ─── TAB 1: CATÁLOGO ─────────────────────────────────────

    with tab1:

        insumos = get_insumos()

        if not insumos:
            st.warning("No hay insumos registrados aún.")
            return

        datos = []
        for i in insumos:
            datos.append({
                "Nombre":       i["nombre"],
                "Descripción":  i["descripcion"]     or "—",
                "Unidad":       i["unidad_medida"]  or "—",
                "Costo (Q)":    f"Q {i['costo']:.2f}"  if i["costo"]  else "—",
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de insumos: {len(datos)}")

    # ─── TAB 2: NUEVO INSUMO ───────────────────────────────

    with tab2:

        if st.session_state.get('insumo_guardado'):
            st.success(f"✅ Insumo '{st.session_state['insumo_nombre']}' registrado correctamente.")
            st.session_state['insumo_guardado'] = False

        st.subheader("Registrar nuevo insumo")

        form_key = f"form_insumo_{st.session_state['form_insumo_count']}"

        with st.form(form_key):

            col1, col2 = st.columns(2)

            with col1:
                nombre          = st.text_input("Nombre *", placeholder="Ej: Insumos de oficina")
                descripcion     = st.text_area("Descripción", placeholder="Descripción del insumo")

            with col2:
                unidad_medida   = st.selectbox("Unidad de medida", options=[
                    "Caja", "Resma", "Litro", "Ciento", "Docena", "Rollo", "Onza", "Unidad"])
                costo           = st.number_input("Costo (Q) *", min_value=0.0, step=0.50)

            submitted = st.form_submit_button("💾 Guardar insumo")

            if submitted:
                if not nombre:
                    st.error("El nombre del insumo es obligatorio.")
                else:
                    insert_insumo(nombre, descripcion, unidad_medida, costo)
                    st.session_state['insumo_guardado']    = True
                    st.session_state['insumo_nombre']      = nombre
                    st.session_state['form_insumo_count'] += 1
                    st.rerun()