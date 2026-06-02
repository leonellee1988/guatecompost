# ============================================================
#  GuateCompost ERP — Módulo de Clientes
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_clientes, insert_cliente

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("👥 Clientes")
    st.markdown("---")

    if 'form_cliente_count' not in st.session_state:
        st.session_state['form_cliente_count'] = 0

    tab1, tab2 = st.tabs(["📋 Directorio", "➕ Nuevo Cliente"])

    # ─── TAB 1: DIRECTORIO ───────────────────────────────────

    with tab1:

        clientes = get_clientes()

        if not clientes:
            st.warning("No hay clientes registrados aún.")
            return

        datos = []
        for c in clientes:
            datos.append({
                "Nombre":    c["nombre"],
                "NIT":       c["nit"]       or "—",
                "Teléfono":  c["telefono"]  or "—",
                "Correo":    c["correo"]    or "—",
                "Dirección": c["direccion"] or "—"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de clientes: {len(datos)}")

    # ─── TAB 2: NUEVO CLIENTE ────────────────────────────────

    with tab2:

        if st.session_state.get('cliente_guardado'):
            st.success(f"✅ Cliente '{st.session_state['cliente_nombre']}' registrado correctamente.")
            st.session_state['cliente_guardado'] = False

        st.subheader("Registrar nuevo cliente")

        form_key = f"form_cliente_{st.session_state['form_cliente_count']}"

        with st.form(form_key):

            col1, col2 = st.columns(2)

            with col1:
                nombre    = st.text_input("Nombre *", placeholder="Ej: Finca San Isidro")
                nit       = st.text_input("NIT", placeholder="Ej: 1234567-8")
                telefono  = st.text_input("Teléfono", placeholder="Ej: 55551234")

            with col2:
                correo    = st.text_input("Correo", placeholder="Ej: cliente@gmail.com")
                direccion = st.text_area("Dirección", placeholder="Ej: Km 45, Carretera a Escuintla")

            submitted = st.form_submit_button("💾 Guardar cliente")

            if submitted:
                if not nombre:
                    st.error("El nombre del cliente es obligatorio.")
                else:
                    insert_cliente(nombre, nit, telefono, correo, direccion)
                    st.session_state['cliente_guardado'] = True
                    st.session_state['cliente_nombre']   = nombre
                    st.session_state['form_cliente_count'] += 1
                    st.rerun()