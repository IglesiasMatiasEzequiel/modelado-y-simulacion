import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from core.interpolacion.lagrange import Lagrange

def renderizar_lagrange():
    
    col_in, col_plot = st.columns([1, 2]) 
    
    with col_in:
        with st.container(border=True):
            st.subheader("Datos de Muestreo", divider="gray")
            st.info("Ingresá los puntos conocidos. Podés agregar o eliminar filas.")
            
            df_inicial = pd.DataFrame({"X": [1.0, 3.0, 5.0], "Y": [2.0, 4.0, 1.0]})
            
            df_editado = st.data_editor(
                df_inicial,
                num_rows="dynamic", # Permite al usuario agregar filas nuevas
                use_container_width=True,
                hide_index=True
            )
            
            calcular = st.button("Calcular Polinomio", use_container_width=True, type="primary")

    if calcular:
        df_limpio = df_editado.dropna()
        
        if len(df_limpio) < 2:
            st.error("Se necesitan al menos 2 puntos para trazar una interpolación.")
            return
            
        if df_limpio["X"].duplicated().any():
            st.error("Los valores de X deben ser únicos (no puede haber dos Y distintos para el mismo X).")
            return
            
        x_list = df_limpio["X"].tolist()
        y_list = df_limpio["Y"].tolist()
        
        try:
            simulador = Lagrange()
            f_interp, pol_str, log_pasos = simulador.ejecutar(x_list, y_list)
            
            with col_plot:
                with st.container(border=True):
                    st.subheader("Resultado de Interpolación", divider="gray")
                    
                    st.success("¡Polinomio encontrado exitosamente!")
                    st.markdown(f"**Polinomio simplificado:**\n`P(x) = {pol_str}`")
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=x_list, y=y_list,
                        mode='markers',
                        marker=dict(color='red', size=12, symbol='circle-open', line=dict(width=2)),
                        name='Puntos Conocidos'
                    ))
                    
                    x_min, x_max = min(x_list), max(x_list)
                    margen = (x_max - x_min) * 0.1 if x_max != x_min else 1.0
                    x_range = np.linspace(x_min - margen, x_max + margen, 200)
                    y_range = f_interp(x_range)
                    
                    fig.add_trace(go.Scatter(
                        x=x_range, y=y_range,
                        mode='lines',
                        line=dict(color='dodgerblue', width=2),
                        name='P(x) Interpolado'
                    ))
                    
                    fig.update_layout(
                        title="Curva de Interpolación de Lagrange",
                        xaxis_title="X", yaxis_title="Y",
                        hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.popover("🔍 Ver desarrollo matemático paso a paso", use_container_width=True):
                        st.markdown("### Construcción de los términos $L_i(x)$")
                        for linea in log_pasos:
                            st.markdown(linea)
                            
        except Exception as e:
            with col_plot:
                st.error(f"Error al calcular la interpolación. Detalle: {e}")