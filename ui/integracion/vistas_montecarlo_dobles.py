import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from core.integracion.motecarlo_dobles import MonteCarloDoble

def renderizar_montecarlo_doble():
    col_in, col_plot = st.columns([1, 2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("Configuración 3D", divider="gray")
                
            f_str = st.text_input("Función z = f(x, y)", value="sin(x) + cos(y) + 3", key="mc2_f")
            
            st.markdown("**Límites en X**")
            cx1, cx2 = st.columns(2)
            with cx1: ax = st.number_input("a_x", value=-2.0, step=0.5, key="mc2_ax")
            with cx2: bx = st.number_input("b_x", value=2.0, step=0.5, key="mc2_bx")

            st.markdown("**Límites en Y**")
            cy1, cy2 = st.columns(2)
            with cy1: ay = st.number_input("a_y", value=-2.0, step=0.5, key="mc2_ay")
            with cy2: by = st.number_input("b_y", value=2.0, step=0.5, key="mc2_by")
                
            st.markdown("---")
            n_puntos = st.number_input("Cantidad de Puntos (N)", min_value=10, max_value=5000, value=500, step=100, key="mc2_n")
            calcular = st.button("Lanzar Muestreo 3D", type="primary", use_container_width=True, key="btn_mc2")

    if calcular:
        if ax >= bx or ay >= by:
            st.error("Los límites inferiores deben ser menores a los superiores en ambos ejes.")
            return
            
        motor = MonteCarloDoble()
        volumen, iteraciones, log_pasos, x_raw, y_raw, z_raw, f_lamb, err = motor.ejecutar(f_str, ax, bx, ay, by, n_puntos)

        if err:
            with col_plot: st.error(err)
        else:
            with col_plot:
                with st.container(border=True):
                    st.subheader("Gráfica: Superficie Real vs Muestras", divider="gray")
                    st.success(f"**Volumen Estimado:** $V \\approx {volumen:.6f}$")

                    fig = go.Figure()

                    # 1. Dibujamos la Sábana (Superficie Analítica Real)
                    grid_res = 30
                    x_grid = np.linspace(ax, bx, grid_res)
                    y_grid = np.linspace(ay, by, grid_res)
                    X, Y = np.meshgrid(x_grid, y_grid)
                    Z = np.zeros_like(X)
                    
                    # Blindaje de dominio para la sábana
                    for i in range(X.shape[0]):
                        for j in range(X.shape[1]):
                            try:
                                Z[i, j] = float(f_lamb(X[i, j], Y[i, j]))
                            except:
                                Z[i, j] = None 

                    fig.add_trace(go.Surface(
                        x=x_grid, y=y_grid, z=Z, 
                        opacity=0.6, colorscale='Viridis', name='f(x,y)'
                    ))

                    # 2. Dibujamos los puntos del muestreo (Scatter 3D)
                    # Limitamos a 2000 puntos en gráfico para que el navegador no explote
                    max_plot = int(min(n_puntos, 2000))
                    fig.add_trace(go.Scatter3d(
                        x=x_raw[:max_plot], y=y_raw[:max_plot], z=z_raw[:max_plot],
                        mode='markers', marker=dict(size=3, color='crimson', opacity=0.8),
                        name='Muestras de Altura'
                    ))

                    fig.update_layout(
                        scene=dict(
                            xaxis_title='Eje X', yaxis_title='Eje Y', zaxis_title='Altura Z'
                        ),
                        height=500, margin=dict(l=0, r=0, t=0, b=0)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    with st.popover("🔍 Ver Tabla de Datos y Análisis Teórico", use_container_width=True):
                        st.markdown("### Cálculos de Probabilidad")
                        for linea in log_pasos:
                            st.markdown(linea)
                            
                        st.divider()
                        st.markdown(f"### Muestra de Puntos (Primeros {min(n_puntos, 100)})")
                        st.dataframe(pd.DataFrame(iteraciones), use_container_width=True, hide_index=True)