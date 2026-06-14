# ============================================================
#  GuateCompost ERP — Módulo de Ventas
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_ventas, get_clientes, get_productos, insert_venta, delete_venta, get_stock_producto

# ─── FUNCIÓN PRINCIPAL ───────────────────────────────────────

def mostrar():

    st.title("💰 Ventas")
    st.markdown("""
    <hr style='margin-top: 0.3rem;'>
    """, unsafe_allow_html=True)

    if 'form_venta_count' not in st.session_state:
        st.session_state['form_venta_count'] = 0

    if 'venta_detalle' not in st.session_state:
        st.session_state['venta_detalle'] = []

    if 'form_detalle_count' not in st.session_state:
        st.session_state['form_detalle_count'] = 0

    tab1, tab2, tab3 = st.tabs(["📋 Historial", "➕ Nueva Venta", "🗑️ Eliminar Venta"])

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
            "precio": p["precio"],
            "unidad_medida": p["unidad_medida"]
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
                unidad     = opciones_productos[producto_preview]["unidad_medida"]
                id_prev    = opciones_productos[producto_preview]["id"]
                stock_disp = get_stock_producto(id_prev)
                st.caption(f"💡 Precio sugerido del catálogo: Q{precio_ref:.2f}")
                st.caption(f"📦 Unidad de medida: {unidad}")

                # Alerta visual de stock
                if stock_disp <= 0:
                    st.error(f"🔴 Sin stock disponible para este producto.")
                elif stock_disp < 10:
                    st.warning(f"⚠️ Stock bajo: {round(stock_disp, 2)} {unidad} disponibles.")
                else:
                    st.success(f"🟢 Stock disponible: {round(stock_disp, 2)} {unidad}.")

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
                        id_producto  = opciones_productos[producto_preview]["id"]
                        stock_disp   = get_stock_producto(id_producto)

                        # Validar stock suficiente
                        ya_en_detalle = sum(
                            i['cantidad'] for i in st.session_state['venta_detalle']
                            if i['id_producto'] == id_producto
                        )

                        if stock_disp <= 0:
                            st.error(f"❌ No hay stock disponible para '{producto_preview}'.")
                        elif cantidad > (stock_disp - ya_en_detalle):
                            st.error(f"❌ Stock insuficiente. "
                                    f"Disponible: {round(stock_disp - ya_en_detalle, 2)} unidades.")
                        else:
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
                for idx, item in enumerate(st.session_state['venta_detalle']):
                    subtotal = item['cantidad'] * item['precio_unitario']
                    total += subtotal
                    col_item, col_del = st.columns([8, 1])
                    with col_item:
                        st.write(f"• {item['nombre']} — "
                                 f"{item['cantidad']} x Q{item['precio_unitario']:.2f} "
                                 f"= **Q{subtotal:.2f}**")
                    with col_del:
                        if st.button("🗑️", key=f"del_item_{idx}"):
                            st.session_state['venta_detalle'].pop(idx)
                            st.rerun()
                st.markdown(f"### Total: Q{total:,.2f}")

    # ─── TAB 3: ELIMINAR VENTA ───────────────────────────────────
    with tab3:
        st.subheader("Eliminar venta")
        st.error("⚠️ Esta acción es permanente. "
                 "La venta y todo su detalle serán eliminados de la base de datos.")

        # Limpiar mensaje si el usuario NO viene de una acción en este tab
        if st.session_state.get("msg_eliminar") and not st.session_state.get("accion_eliminar"):
            st.session_state["msg_eliminar"] = None

        # Mostrar mensaje persistente si existe
        if st.session_state.get("msg_eliminar"):
            st.success(st.session_state["msg_eliminar"])
            st.session_state["msg_eliminar"] = None
            st.session_state["accion_eliminar"] = False  # Resetear bandera

        ventas_lista = get_ventas()
        if not ventas_lista:
            st.info("No hay registro de ventas.")
        else:
            opciones = {f"Venta #{v['id_venta']} — {v['cliente']} — {v['fecha_venta']} — Q{v['total']:,.2f}": v['id_venta'] for v in ventas_lista}
            venta_sel = st.selectbox(
                "Seleccione la venta a eliminar",
                options=["— Seleccione una venta —"] + list(opciones.keys())
            )
            if venta_sel != "— Seleccione una venta —":
                st.error(f"¿Está seguro que desea eliminar **{venta_sel}**?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Sí, eliminar", key="btn_eliminar_venta"):
                        delete_venta(opciones[venta_sel])
                        st.session_state["msg_eliminar"] = f"Venta '{venta_sel}' eliminada correctamente."
                        st.session_state["accion_eliminar"] = True
                        st.rerun()
                with col2:
                    if st.button("❌ Cancelar", key="btn_cancelar_venta"):
                        st.rerun()