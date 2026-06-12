# ============================================================
#  GuateCompost ERP — Módulo de Clientes
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_clientes, insert_cliente, delete_cliente

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("👥 Clientes")
    st.markdown("---")

    if 'form_cliente_count' not in st.session_state:
        st.session_state['form_cliente_count'] = 0

    tab1, tab2, tab3 = st.tabs(["📋 Directorio", "➕ Nuevo Cliente", "🗑️ Desactivar"])

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
    
    # ─── TAB 3: DESACTIVAR ───────────────────────────────────
    with tab3:
        st.subheader("Desactivar cliente")
        st.warning("El cliente no se eliminará permanentemente. "
                "Solo dejará de aparecer en el sistema.")

        # Limpiar mensaje si el usuario NO viene de una acción en este tab
        if st.session_state.get("msg_desactivar") and not st.session_state.get("accion_desactivar"):
            st.session_state["msg_desactivar"] = None

        # Mostrar mensaje persistente si existe
        if st.session_state.get("msg_desactivar"):
            st.success(st.session_state["msg_desactivar"])
            st.session_state["msg_desactivar"] = None
            st.session_state["accion_desactivar"] = False  # Resetear bandera

        clientes_lista = get_clientes()
        if not clientes_lista:
            st.info("No hay clientes activos.")
        else:
            opciones = {p["nombre"]: p["id_cliente"] for p in clientes_lista}
            cliente_sel = st.selectbox(
                "Seleccione el cliente a desactivar",
                options=["— Seleccione un cliente —"] + list(opciones.keys())
            )
            if cliente_sel != "— Seleccione un cliente —":
                st.error(f"¿Está seguro que desea desactivar **{cliente_sel}**?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Sí, desactivar", key="btn_desactivar_cliente"):
                        delete_cliente(opciones[cliente_sel])
                        st.session_state["msg_desactivar"] = f"Cliente '{cliente_sel}' desactivado correctamente."
                        st.session_state["accion_desactivar"] = True
                        st.rerun()
                with col2:
                    if st.button("❌ Cancelar", key="btn_cancelar_cliente"):
                        st.rerun()