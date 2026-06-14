# ============================================================
#  LEERP — Módulo Dashboard BI
#  Autor: Edwin Lee Tiño
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def mostrar():

    st.title("📡 Dashboard BI")
    st.markdown("---")

    st.markdown("""
        Sincroniza los datos del ERP con Google Sheets para
        actualizar los dashboards en Looker Studio.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
            **¿Cuándo actualizar?**  \n
            Cada vez que registres ventas, compras o gastos
            importantes y quieras verlos reflejados en el dashboard.
        """)

    with col2:
        st.warning("""
            **Tiempo estimado**  \n
            La sincronización toma entre 10 y 30 segundos
            dependiendo del volumen de datos.
        """)

    st.markdown("---")

    if st.button("📡 Sincronizar con Google Sheets",
                 type="primary",
                 use_container_width=True):
        with st.spinner("Sincronizando datos..."):
            try:
                from exportar_sheets import exportar_todo
                exportar_todo()
                st.success("✅ Datos sincronizados correctamente. "
                           "Tu dashboard en Looker Studio está actualizado.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error en la sincronización: {e}")

    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #4A7FA5; font-size: 0.85rem;'>
            Los dashboards se visualizan en
            <a href='https://lookerstudio.google.com'
               target='_blank' style='color: #90CDF4;'>
               Looker Studio
            </a>
        </div>
    """, unsafe_allow_html=True)