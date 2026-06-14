# ============================================================
#  GuateCompost ERP — Módulo de Gastos
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_gastos, get_proveedores, get_insumos, insert_gasto, delete_gasto

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("🛍️ Gastos (compra de insumos)")
    st.markdown("""
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    if 'form_gasto_count' not in st.session_state:
        st.session_state['form_gasto_count'] = 0

    if 'gasto_detalle' not in st.session_state:
        st.session_state['gasto_detalle'] = []

    if 'form_detalle_count' not in st.session_state:
        st.session_state['form_detalle_count'] = 0
    
    if 'gasto_descripcion' not in st.session_state:
        st.session_state['gasto_descripcion'] = ""

    tab1, tab2, tab3 = st.tabs(["📋 Historial", "➕ Nuevo Gasto", "🗑️ Eliminar Gasto"])

    # ─── TAB 1: HISTORIAL ────────────────────────────────────

    with tab1:

        gastos = get_gastos()

        if not gastos:
            st.warning("No hay gastos registrados aún.")

        datos = []
        for g in gastos:
            datos.append({
                "ID":       g["id_gasto"],
                "Fecha":    g["fecha_gasto"],
                "Proveedor":  g["proveedor"],
                "Total":    f"Q {g['total']:,.2f}"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de gastos: {len(datos)}")

    # ─── TAB 2: NUEVO GASTO ──────────────────────────────────

    with tab2:

        if st.session_state.get('gasto_guardado'):
            st.success(f"✅ Gasto registrado correctamente.")
            st.session_state['gasto_guardado'] = False

        st.subheader("Registrar nuevo gasto")

        # ─── CABECERA ────────────────────────────────────────

        proveedores  = get_proveedores()
        insumos = get_insumos()

        opciones_proveedores = {p["nombre"]: p["id_proveedor"] for p in proveedores}
        opciones_insumos = {i["nombre"]: {
            "id":     i["id_insumo"],
            "costo": i["costo"],
            "unidad_medida": i["unidad_medida"]
        } for i in insumos}

        with st.form("form_gasto_cabecera"):
            col1, col2 = st.columns(2)
            with col1:
                proveedor_nombre = st.selectbox("Proveedor *",
                    options=["— Seleccione un proveedor —"] + list(opciones_proveedores.keys()))
            with col2:
                fecha = st.date_input("Fecha *", value=date.today())
            descripcion = st.text_input("Descripción *", placeholder="Ej: Compra de papelería enero")

            agregar = st.form_submit_button("Continuar →")

            if agregar:
                if proveedor_nombre == "— Seleccione un proveedor —":
                    st.error("Debe seleccionar un proveedor.")
                else:
                    st.session_state['gasto_proveedor_id']     = opciones_proveedores[proveedor_nombre]
                    st.session_state['gasto_proveedor_nombre'] = proveedor_nombre
                    st.session_state['gasto_fecha']          = str(fecha)
                    st.session_state['gasto_descripcion']    = descripcion
                    st.session_state['gasto_detalle']        = []

        # ─── DETALLE ─────────────────────────────────────────

        if st.session_state.get('gasto_proveedor_id'):

            st.markdown("---")
            st.markdown(f"**Proveedor:** {st.session_state['gasto_proveedor_nombre']} "
                        f"| **Fecha:** {st.session_state['gasto_fecha']}")

            # Selector de insumo fuera del form
            insumo_preview = st.selectbox(
                "Insumo *",
                options=["— Seleccione un insumo —"] + list(opciones_insumos.keys()),
                key=f"preview_insumo_{st.session_state['form_detalle_count']}"
            )

            if insumo_preview != "— Seleccione un insumo —":
                costo_ref = float(opciones_insumos[insumo_preview]["costo"])
                unidad     = opciones_insumos[insumo_preview]["unidad_medida"]
                st.caption(f"💡 Costo sugerido del catálogo: Q{costo_ref:.2f}")
                st.caption(f"📦 Unidad de medida: {unidad}")
            else:
                costo_ref = 0.0

            form_detalle_key = f"form_gasto_detalle_{st.session_state['form_detalle_count']}"

            with st.form(form_detalle_key):
                col1, col2 = st.columns(2)
                with col1:
                    cantidad = st.number_input("Cantidad", min_value=0.1, step=0.5)
                with col2:
                    costo = st.number_input(
                        "Costo unitario (Q) — modificable",
                        min_value=0.0,
                        step=0.50,
                        value=costo_ref,
                        help="Costo sugerido del catálogo. Puede modificarlo."
                    )

                add_item = st.form_submit_button("➕ Agregar insumo")
                guardar  = st.form_submit_button("💾 Guardar gasto")

                if add_item:
                    if insumo_preview == "— Seleccione un insumo —":
                        st.error("Debe seleccionar un insumo válido.")
                    else:
                        id_insumo = opciones_insumos[insumo_preview]["id"]
                        ya_existe = any(
                            i['id_insumo'] == id_insumo
                            for i in st.session_state['gasto_detalle']
                        )
                        if ya_existe:
                            st.error(f"'{insumo_preview}' ya está en el detalle.")
                        else:
                            st.session_state['gasto_detalle'].append({
                                'id_insumo':     id_insumo,
                                'nombre':          insumo_preview,
                                'cantidad':        cantidad,
                                'costo_unitario': costo
                            })
                            st.session_state['form_detalle_count'] += 1
                            st.rerun()

                if guardar:
                    if not st.session_state['gasto_detalle']:
                        st.error("Debe agregar al menos un insumo.")
                    else:
                        insert_gasto(
                            st.session_state['gasto_fecha'],
                            st.session_state['gasto_proveedor_id'],
                            st.session_state['gasto_descripcion'],
                            st.session_state['gasto_detalle']
                        )
                        st.session_state['gasto_guardado']     = True
                        st.session_state['gasto_proveedor_id']   = None
                        st.session_state['gasto_detalle']      = []
                        st.session_state['form_detalle_count'] = 0
                        st.session_state['form_gasto_count']  += 1
                        st.rerun()

            # Mostrar detalle acumulado
            if st.session_state['gasto_detalle']:
                st.markdown("#### Insumos agregados")
                total = 0
                for idx, item in enumerate(st.session_state['gasto_detalle']):
                    subtotal = item['cantidad'] * item['costo_unitario']
                    total += subtotal
                    col_item, col_del = st.columns([8, 1])
                    with col_item:
                        st.write(f"• {item['nombre']} — "
                                 f"{item['cantidad']} x Q{item['costo_unitario']:.2f} "
                                 f"= **Q{subtotal:.2f}**")
                    with col_del:
                        if st.button("🗑️", key=f"del_item_{idx}"):
                            st.session_state['gasto_detalle'].pop(idx)
                            st.rerun()
                st.markdown(f"### Total: Q{total:,.2f}")

    # ─── TAB 3: ELIMINAR GASTO ───────────────────────────────────
    with tab3:
        st.subheader("Eliminar gasto")
        st.error("⚠️ Esta acción es permanente. "
                 "El gasto y todo su detalle serán eliminados de la base de datos.")

        # Limpiar mensaje si el usuario NO viene de una acción en este tab
        if st.session_state.get("msg_eliminar") and not st.session_state.get("accion_eliminar"):
            st.session_state["msg_eliminar"] = None

        # Mostrar mensaje persistente si existe
        if st.session_state.get("msg_eliminar"):
            st.success(st.session_state["msg_eliminar"])
            st.session_state["msg_eliminar"] = None
            st.session_state["accion_eliminar"] = False  # Resetear bandera

        gastos_lista = get_gastos()
        if not gastos_lista:
            st.info("No hay registro de gastos.")
        else:
            opciones = {f"Gasto #{g['id_gasto']} — {g['proveedor']} — {g['fecha_gasto']} — Q{g['total']:,.2f}": g['id_gasto'] for g in gastos_lista}
            gasto_sel = st.selectbox(
                "Seleccione el gasto a eliminar",
                options=["— Seleccione un gasto —"] + list(opciones.keys())
            )
            if gasto_sel != "— Seleccione un gasto —":
                st.error(f"¿Está seguro que desea eliminar **{gasto_sel}**?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Sí, eliminar", key="btn_eliminar_gasto"):
                        delete_gasto(opciones[gasto_sel])
                        st.session_state["msg_eliminar"] = f"Gasto '{gasto_sel}' eliminada correctamente."
                        st.session_state["accion_eliminar"] = True
                        st.rerun()
                with col2:
                    if st.button("❌ Cancelar", key="btn_cancelar_gasto"):
                        st.rerun()