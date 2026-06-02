# ============================================================
#  GuateCompost ERP — Módulo de Ventas
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_ventas, get_clientes, get_productos, insert_venta

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("💰 Ventas")
    st.markdown("---")

    if 'form_venta_count' not in st.session_state:
        st.session_state['form_venta_count'] = 0

    if 'venta_detalle' not in st.session_state:
        st.session_state['venta_detalle'] = []

    if 'form_detalle_count' not in st.session_state:
        st.session_state['form_detalle_count'] = 0

    tab1, tab2 = st.tabs(["📋 Historial", "➕ Nueva Venta"])

    # ─── TAB 1: HISTORIAL ────────────────────────────────────

    with tab1:

        ventas = get_ventas()

        if not ventas:
            st.warning("No hay ventas registradas aún.")
            return

        datos = []
        for v in ventas:
            datos.append({
                "ID":       v["id_venta"],
                "Fecha":    v["fecha_venta"],
                "Cliente":  v["cliente"],
                "Total":    f"Q {v['total']:,.2f}"
            })

        st.dataframe(datos, width='stretch', hide_index=True)
        st.caption(f"Total de ventas: {len(datos)}")

    # ─── TAB 2: NUEVA VENTA ──────────────────────────────────

    with tab2:

        if st.session_state.get('venta_guardada'):
            st.success(f"✅ Venta registrada correctamente.")
            st.session_state['venta_guardada'] = False

        st.subheader("Registrar nueva venta")

        # ─── CABECERA ────────────────────────────────────────

        clientes  = get_clientes()
        productos = get_productos()

        opciones_clientes = {c["nombre"]: c["id_cliente"] for c in clientes}
        opciones_productos = {p["nombre"]: {
            "id":     p["id_producto"],
            "precio": p["precio"]
        } for p in productos}

        with st.form("form_venta_cabecera"):
            col1, col2 = st.columns(2)
            with col1:
                cliente_nombre = st.selectbox("Cliente *",
                    options=["— Seleccione un cliente —"] + list(opciones_clientes.keys()))
            with col2:
                fecha = st.date_input("Fecha *", value=date.today())

            agregar = st.form_submit_button("Continuar →")

            if agregar:
                if cliente_nombre == "— Seleccione un cliente —":
                    st.error("Debe seleccionar un cliente.")
                else:
                    st.session_state['venta_cliente_id']     = opciones_clientes[cliente_nombre]
                    st.session_state['venta_cliente_nombre'] = cliente_nombre
                    st.session_state['venta_fecha']          = str(fecha)
                    st.session_state['venta_detalle']        = []

        # ─── DETALLE ─────────────────────────────────────────
        # OJO: este bloque está al mismo nivel que el form de cabecera
        # 8 espacios de indentación — dentro de tab2 pero FUERA del form

        if st.session_state.get('venta_cliente_id'):

            st.markdown("---")
            st.markdown(f"**Cliente:** {st.session_state['venta_cliente_nombre']} "
                        f"| **Fecha:** {st.session_state['venta_fecha']}")

            # Selector de producto fuera del form
            producto_preview = st.selectbox(
                "Producto *",
                options=["— Seleccione un producto —"] + list(opciones_productos.keys()),
                key=f"preview_producto_{st.session_state['form_detalle_count']}"
            )

            if producto_preview != "— Seleccione un producto —":
                precio_ref = float(opciones_productos[producto_preview]["precio"])
                st.caption(f"💡 Precio sugerido del catálogo: Q{precio_ref:.2f}")
            else:
                precio_ref = 0.0

            form_detalle_key = f"form_venta_detalle_{st.session_state['form_detalle_count']}"

            with st.form(form_detalle_key):
                col1, col2 = st.columns(2)
                with col1:
                    cantidad = st.number_input("Cantidad", min_value=0.1, step=0.5)
                with col2:
                    precio = st.number_input(
                        "Precio unitario (Q) — modificable",
                        min_value=0.0,
                        step=0.50,
                        value=precio_ref,
                        help="Precio sugerido del catálogo. Puede modificarlo."
                    )

                add_item = st.form_submit_button("➕ Agregar producto")
                guardar  = st.form_submit_button("💾 Guardar venta")

                if add_item:
                    if producto_preview == "— Seleccione un producto —":
                        st.error("Debe seleccionar un producto válido.")
                    else:
                        id_producto = opciones_productos[producto_preview]["id"]
                        ya_existe = any(
                            i['id_producto'] == id_producto
                            for i in st.session_state['venta_detalle']
                        )
                        if ya_existe:
                            st.error(f"'{producto_preview}' ya está en el detalle.")
                        else:
                            st.session_state['venta_detalle'].append({
                                'id_producto':     id_producto,
                                'nombre':          producto_preview,
                                'cantidad':        cantidad,
                                'precio_unitario': precio
                            })
                            st.session_state['form_detalle_count'] += 1
                            st.rerun()

                if guardar:
                    if not st.session_state['venta_detalle']:
                        st.error("Debe agregar al menos un producto.")
                    else:
                        insert_venta(
                            st.session_state['venta_fecha'],
                            st.session_state['venta_cliente_id'],
                            st.session_state['venta_detalle']
                        )
                        st.session_state['venta_guardada']     = True
                        st.session_state['venta_cliente_id']   = None
                        st.session_state['venta_detalle']      = []
                        st.session_state['form_detalle_count'] = 0
                        st.session_state['form_venta_count']  += 1
                        st.rerun()

            # Mostrar detalle acumulado
            if st.session_state['venta_detalle']:
                st.markdown("#### Productos agregados")
                total = 0
                for item in st.session_state['venta_detalle']:
                    subtotal = item['cantidad'] * item['precio_unitario']
                    total += subtotal
                    st.write(f"• {item['nombre']} — "
                             f"{item['cantidad']} x Q{item['precio_unitario']:.2f} "
                             f"= **Q{subtotal:.2f}**")
                st.markdown(f"### Total: Q{total:,.2f}")