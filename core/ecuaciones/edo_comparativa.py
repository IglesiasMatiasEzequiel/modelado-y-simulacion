import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.ecuaciones.edo import EcuacionesDiferenciales

def renderizar_comparativa_edo():
    st.header("Comparativa: Euler vs Heun vs RK4")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            f_str = st.text_input("dy/dx = f(x, y)", value="y - x**2 + 1")
            xf = st.number_input("x Final", value=2.0)
        with col2:
            x0 = st.number_input("x₀", value=0.0)
            y0 = st.number_input("y₀", value=0.5)
        with col3:
            n = st.number_input("Intervalos (N)", min_value=1, value=10)
            st.write("")
            comparar = st.button("Comparar Métodos", type="primary", use_container_width=True)

    if comparar:
        motor = EcuacionesDiferenciales()
        res, err = motor.ejecutar_comparativa(f_str, x0, y0, xf, n)

        if err:
            st.error(err)
        else:
            fig = go.Figure()
            estilos = {
                "Euler": {"color": "crimson", "dash": "dot"},
                "Heun": {"color": "darkorange", "dash": "dash"},
                "Runge-Kutta 4": {"color": "mediumseagreen", "dash": "solid"}
            }

            # Armamos una tabla para el resumen final
            resumen_data = []

            for metodo, datos in res.items():
                fig.add_trace(go.Scatter(
                    x=datos["x"], y=datos["y"],
                    mode='lines+markers',
                    name=metodo,
                    line=dict(color=estilos[metodo]["color"], dash=estilos[metodo]["dash"]),
                    marker=dict(size=4)
                ))
                
                resumen_data.append({
                    "Método": metodo,
                    "Valor Final y(xf)": round(datos["y"][-1], 6)
                })

            fig.update_layout(
                title="Superposición de Trayectorias",
                xaxis_title="X", yaxis_title="Y",
                hovermode="x unified",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabla comparativa de resultados finales
            st.subheader("Resumen de Valores Finales")
            df_resumen = pd.DataFrame(resumen_data)
            st.table(df_resumen)

            st.info("""
            **Análisis de Convergencia:** Observá cómo, ante un mismo N, Runge-Kutta 4 suele ser el que mejor define la curvatura. 
            Si aumentás N (o achicás el paso h), verás que Euler y Heun comienzan a cerrarse sobre el valor de RK4.
            """)