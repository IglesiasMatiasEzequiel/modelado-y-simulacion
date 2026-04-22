import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.ecuaciones.edo import EcuacionesDiferenciales

def renderizar_comparativa_edo():
    st.subheader("Comparativa de Métodos EDO", divider="green")
    
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_str = st.text_input("dy/dx = f(x, y)", value="y - x**2 + 1", key="comp_f")
            xf = st.number_input("x Final", value=2.0, key="comp_xf")
        with c2:
            x0 = st.number_input("x₀", value=0.0, key="comp_x0")
            y0 = st.number_input("y₀", value=0.5, key="comp_y0")
        with c3:
            n = st.number_input("Intervalos (N)", min_value=1, value=10, key="comp_n")
            st.write("")
            btn = st.button("Ejecutar Comparativa", type="primary", use_container_width=True)

    if btn:
        motor = EcuacionesDiferenciales()
        res, err = motor.ejecutar_comparativa(f_str, x0, y0, xf, n)

        if err:
            st.error(err)
        else:
            fig = go.Figure()
            estilos = {
                "Euler": "crimson", 
                "Heun": "darkorange", 
                "Runge-Kutta 4": "mediumseagreen"
            }

            resumen = []
            for met, data in res.items():
                fig.add_trace(go.Scatter(
                    x=data["x"], y=data["y"], name=met,
                    mode='lines+markers', line=dict(color=estilos[met]),
                    marker=dict(size=5)
                ))
                resumen.append({"Método": met, "Valor Final y(xf)": round(data["y"][-1], 6)})

            fig.update_layout(
                xaxis_title="X", yaxis_title="Y", height=450,
                margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Resumen de Valores Finales")
            st.table(pd.DataFrame(resumen))

            with st.popover("🔍 Ver Tablas de Pasos Completas", use_container_width=True):
                nombres_metodos = ["Euler", "Heun", "Runge-Kutta 4"]
                tabs = st.tabs(nombres_metodos)
                
                for idx, metodo in enumerate(nombres_metodos):
                    with tabs[idx]:
                        df_iters = pd.DataFrame(res[metodo]["iteraciones"])
                        st.dataframe(df_iters, use_container_width=True, hide_index=True)