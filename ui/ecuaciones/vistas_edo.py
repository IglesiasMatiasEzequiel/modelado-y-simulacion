import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.ecuaciones.edo import EcuacionesDiferenciales

def renderizar_edo():
    col_in, col_plot = st.columns([1, 2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("Configuración", divider="gray")
            
            f_str = st.text_input("Derivada dy/dx = f(x, y)", value="y - x**2 + 1")
            
            c1, c2 = st.columns(2)
            with c1:
                x0 = st.number_input("x Inicial (x₀)", value=0.0, step=0.1)
                y0 = st.number_input("y Inicial (y₀)", value=0.5, step=0.1)
            with c2:
                xf = st.number_input("x Final (x_f)", value=2.0, step=0.5)
                n = st.number_input("Intervalos (N)", min_value=1, value=10, step=1)
                
            metodo = st.selectbox("Método de Resolución", ["Euler", "Heun", "Runge-Kutta 4"])
            
            st.markdown("---")
            calcular = st.button("Resolver EDO", type="primary", use_container_width=True)

    if calcular:
        if x0 >= xf:
            st.error("El valor de x₀ debe ser estrictamente menor que x_f.")
            return

        motor = EcuacionesDiferenciales()
        iteraciones, log_pasos, x_raw, y_raw, err = motor.ejecutar(f_str, x0, y0, xf, n, metodo)

        if err:
            with col_plot:
                st.error(err)
        else:
            with col_plot:
                with st.container(border=True):
                    st.subheader("Gráfica de la Solución Aproximada", divider="gray")
                    
                    st.success(f"**Valor Final Aproximado:** $y({xf}) \\approx {y_raw[-1]:.6f}$")

                    fig = go.Figure()

                    # Color dinámico según el método
                    colores = {"Euler": "crimson", "Heun": "darkorange", "Runge-Kutta 4": "mediumseagreen"}
                    color_metodo = colores.get(metodo, "dodgerblue")

                    fig.add_trace(go.Scatter(
                        x=x_raw, y=y_raw, mode='lines+markers',
                        line=dict(color=color_metodo, width=3),
                        marker=dict(size=6, symbol='circle'),
                        name=f'Aprox. {metodo}'
                    ))

                    fig.add_trace(go.Scatter(
                        x=[x0], y=[y0], mode='markers',
                        marker=dict(color='black', size=10, symbol='diamond'),
                        name='Condición Inicial (x₀, y₀)'
                    ))

                    fig.update_layout(
                        xaxis_title="X", yaxis_title="Y", height=400,
                        margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    with st.popover("🔍 Ver Tabla de Datos y Desarrollo Analítico", use_container_width=True):
                        st.markdown("### Cálculos de la Iteración 1")
                        for linea in log_pasos:
                            st.markdown(linea)
                            
                        st.divider()
                        st.markdown("### Tabla de Iteraciones Completa")
                        df_iters = pd.DataFrame(iteraciones)
                        st.dataframe(df_iters, use_container_width=True, hide_index=True)