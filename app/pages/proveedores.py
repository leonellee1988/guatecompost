# ============================================================
#  GuateCompost ERP — Módulo de Proveedores
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_proveedores, insert_proveedor

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("🏷️ Proveedores")
    st.markdown("---")

    if 'form_proveedor_count' not in st.session_state:
        st.session_state['form_proveedor_count'] = 0

    tab1, tab2 = st.tabs(["📋 Directorio", "➕ Nuevo Proveedor"])

    # ─── TAB 1: DIRECTORIO ─────────────────────────────────────

    with tab1:

        proveedores = get_proveedores()

        if not proveedores:
            st.warning("No hay proveedores registrados aún.")
            return

        datos = []
        for p in proveedores:
            datos.append({
                "Nombre":       p["nombre"],
                "Contacto":     p["contacto"]     or "—",
                "NIT":          p["nit"]  or "—",
                "Teléfono":     p["telefono"] or "—",
                "Correo":       p["correo"] or "—",
                "Dirección":    p["direccion"] or "—"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de proveedores: {len(datos)}")

    # ─── TAB 2: NUEVO PROVEEDOR ───────────────────────────────

    with tab2:

        if st.session_state.get('proveedor_guardado'):
            st.success(f"✅ Proveedor '{st.session_state['proveedor_nombre']}' registrado correctamente.")
            st.session_state['proveedor_guardado'] = False

        st.subheader("Registrar nuevo proveedor")

        form_key = f"form_proveedor_{st.session_state['form_proveedor_count']}"

        with st.form(form_key):

            col1, col2 = st.columns(2)

            with col1:
                nombre        = st.text_input("Nombre *", placeholder="Ej: Bioinsumos Guatemala")
                contacto      = st.text_input("Contacto", placeholder="Ej: Edwin Leonel Lee")
                nit           = st.text_input("NIT", placeholder="Ej: 1234567-8")

            with col2:
                telefono      = st.text_input("Teléfono", placeholder="Ej: 55551234")
                correo        = st.text_input("Correo", placeholder="Ej: proveedor@gmail.com")
                direccion     = st.text_input("Dirección", placeholder="Ej: Km 45, Carretera a Escuintla")

            submitted = st.form_submit_button("💾 Guardar proveedor")

            if submitted:
                if not nombre:
                    st.error("El nombre del proveedor es obligatorio.")
                else:
                    insert_proveedor(nombre, contacto, nit, telefono, correo, direccion)
                    st.session_state['proveedor_guardado']    = True
                    st.session_state['proveedor_nombre']      = nombre
                    st.session_state['form_proveedor_count'] += 1
                    st.rerun()