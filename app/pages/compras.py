# ============================================================
#  GuateCompost ERP — Módulo de Compras
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_compras, get_proveedores, get_productos, insert_compra, delete_compra

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("🛒 Compras")
    st.markdown("""
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    if 'form_compra_count' not in st.session_state:
        st.session_state['form_compra_count'] = 0

    if 'compra_detalle' not in st.session_state:
        st.session_state['compra_detalle'] = []

    if 'form_detalle_count' not in st.session_state:
        st.session_state['form_detalle_count'] = 0

    tab1, tab2, tab3 = st.tabs(["📋 Historial", "➕ Nueva Compra", "🗑️ Eliminar Compra"])

    # ─── TAB 1: HISTORIAL ────────────────────────────────────

    with tab1:

        compras = get_compras()

        if not compras:
            st.warning("No hay compras registradas aún.")
            return

        datos = []
        for c in compras:
            datos.append({
                "ID":       c["id_compra"],
                "Fecha":    c["fecha_compra"],
                "Cliente":  c["proveedor"],
                "Total":    f"Q {c['total']:,.2f}"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de compras: {len(datos)}")

    # ─── TAB 2: NUEVA COMPRA ──────────────────────────────────

    with tab2:

        if st.session_state.get('compra_guardada'):
            st.success(f"✅ Compra registrada correctamente.")
            st.session_state['compra_guardada'] = False

        st.subheader("Registrar nueva compra")

        # ─── CABECERA ────────────────────────────────────────

        proveedores  = get_proveedores()
        productos = get_productos()

        opciones_proveedores = {p["nombre"]: p["id_proveedor"] for p in proveedores}
        opciones_productos = {p["nombre"]: {
            "id":     p["id_producto"],
            "costo": p["costo"],
            "unidad_medida": p["unidad_medida"]
        } for p in productos}

        with st.form("form_compra_cabecera"):
            col1, col2 = st.columns(2)
            with col1:
                proveedor_nombre = st.selectbox("Proveedor *",
                    options=["— Seleccione un proveedor —"] + list(opciones_proveedores.keys()))
            with col2:
                fecha = st.date_input("Fecha *", value=date.today())

            agregar = st.form_submit_button("Continuar →")

            if agregar:
                if proveedor_nombre == "— Seleccione un proveedor —":
                    st.error("Debe seleccionar un proveedor.")
                else:
                    st.session_state['compra_proveedor_id']     = opciones_proveedores[proveedor_nombre]
                    st.session_state['compra_proveedor_nombre'] = proveedor_nombre
                    st.session_state['compra_fecha']          = str(fecha)
                    st.session_state['compra_detalle']        = []

        # ─── DETALLE ─────────────────────────────────────────

        if st.session_state.get('compra_proveedor_id'):

            st.markdown("---")
            st.markdown(f"**Proveedor:** {st.session_state['compra_proveedor_nombre']} "
                        f"| **Fecha:** {st.session_state['compra_fecha']}")

            # Selector de producto fuera del form
            producto_preview = st.selectbox(
                "Producto *",
                options=["— Seleccione un producto —"] + list(opciones_productos.keys()),
                key=f"preview_producto_{st.session_state['form_detalle_count']}"
            )

            if producto_preview != "— Seleccione un producto —":
                costo_ref = float(opciones_productos[producto_preview]["costo"])
                unidad     = opciones_productos[producto_preview]["unidad_medida"]
                st.caption(f"💡 Costo sugerido del catálogo: Q{costo_ref:.2f}")
                st.caption(f"📦 Unidad de medida: {unidad}")
            else:
                costo_ref = 0.0

            form_detalle_key = f"form_compra_detalle_{st.session_state['form_detalle_count']}"

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

                add_item = st.form_submit_button("➕ Agregar producto")
                guardar  = st.form_submit_button("💾 Guardar compra")

                if add_item:
                    if producto_preview == "— Seleccione un producto —":
                        st.error("Debe seleccionar un producto válido.")
                    else:
                        id_producto = opciones_productos[producto_preview]["id"]
                        ya_existe = any(
                            i['id_producto'] == id_producto
                            for i in st.session_state['compra_detalle']
                        )
                        if ya_existe:
                            st.error(f"'{producto_preview}' ya está en el detalle.")
                        else:
                            st.session_state['compra_detalle'].append({
                                'id_producto':     id_producto,
                                'nombre':          producto_preview,
                                'cantidad':        cantidad,
                                'costo_unitario': costo
                            })
                            st.session_state['form_detalle_count'] += 1
                            st.rerun()

                if guardar:
                    if not st.session_state['compra_detalle']:
                        st.error("Debe agregar al menos un producto.")
                    else:
                        insert_compra(
                            st.session_state['compra_fecha'],
                            st.session_state['compra_proveedor_id'],
                            st.session_state['compra_detalle']
                        )
                        st.session_state['compra_guardada']     = True
                        st.session_state['compra_proveedor_id']   = None
                        st.session_state['compra_detalle']      = []
                        st.session_state['form_detalle_count'] = 0
                        st.session_state['form_compra_count']  += 1
                        st.rerun()

            # Mostrar detalle acumulado
            if st.session_state['compra_detalle']:
                st.markdown("#### Productos agregados")
                total = 0
                for idx, item in enumerate(st.session_state['compra_detalle']):
                    subtotal = item['cantidad'] * item['costo_unitario']
                    total += subtotal
                    col_item, col_del = st.columns([8, 1])
                    with col_item:
                        st.write(f"• {item['nombre']} — "
                                 f"{item['cantidad']} x Q{item['costo_unitario']:.2f} "
                                 f"= **Q{subtotal:.2f}**")
                    with col_del:
                        if st.button("🗑️", key=f"del_item_{idx}"):
                            st.session_state['compra_detalle'].pop(idx)
                            st.rerun()
                st.markdown(f"### Total: Q{total:,.2f}")

    # ─── TAB 3: ELIMINAR COMPRA ───────────────────────────────────
    with tab3:
        st.subheader("Eliminar compra")
        st.error("⚠️ Esta acción es permanente. "
                 "La compra y todo su detalle serán eliminados de la base de datos.")

        # Limpiar mensaje si el usuario NO viene de una acción en este tab
        if st.session_state.get("msg_eliminar") and not st.session_state.get("accion_eliminar"):
            st.session_state["msg_eliminar"] = None

        # Mostrar mensaje persistente si existe
        if st.session_state.get("msg_eliminar"):
            st.success(st.session_state["msg_eliminar"])
            st.session_state["msg_eliminar"] = None
            st.session_state["accion_eliminar"] = False  # Resetear bandera

        compras_lista = get_compras()
        if not compras_lista:
            st.info("No hay registro de compras.")
        else:
            opciones = {f"Compra #{c['id_compra']} — {c['proveedor']} — {c['fecha_compra']} — Q{c['total']:,.2f}": c['id_compra'] for c in compras_lista}
            compra_sel = st.selectbox(
                "Seleccione la compra a eliminar",
                options=["— Seleccione una compra —"] + list(opciones.keys())
            )
            if compra_sel != "— Seleccione una compra —":
                st.error(f"¿Está seguro que desea eliminar **{compra_sel}**?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Sí, eliminar", key="btn_eliminar_compra"):
                        delete_compra(opciones[compra_sel])
                        st.session_state["msg_eliminar"] = f"Compra '{compra_sel}' eliminada correctamente."
                        st.session_state["accion_eliminar"] = True
                        st.rerun()
                with col2:
                    if st.button("❌ Cancelar", key="btn_cancelar_compra"):
                        st.rerun()