import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sympy as sp

from core.integracion.newton_cotes import NewtonCotes

def renderizar_newton_cotes():
    col_in, col_plot = st.columns([1, 2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("Configuración", divider="gray")
            
            funcion_str = st.text_input("Función f(x)", value="sin(x) + 2")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("Límite inferior (a)", value=0.0, step=0.5)
            with c2:
                b = st.number_input("Límite superior (b)", value=4.0, step=0.5)
                
            n = st.number_input("Subintervalos (n)", min_value=1, value=4, step=1, 
                                help="Cantidad de 'pedacitos' en los que se divide el área.")
            
            regla = st.selectbox("Método de Integración", ["Trapecio", "Simpson 1/3", "Simpson 3/8"])
            
            if regla == "Simpson 1/3" and n % 2 != 0:
                st.warning("⚠️ Atención: Para Simpson 1/3 el valor de 'n' debe ser un número par.")
            elif regla == "Simpson 3/8" and n % 3 != 0:
                st.warning("⚠️ Atención: Para Simpson 3/8 el valor de 'n' debe ser múltiplo de 3 (3, 6, 9...).")

            st.markdown("---")
            calcular = st.button("Calcular Área", type="primary", use_container_width=True)

    if calcular:
        if a >= b:
            st.error("El límite inferior 'a' debe ser estrictamente menor que el límite superior 'b'.")
            return

        # Llamamos al motor matemático
        simulador = NewtonCotes()
        area, iteraciones, log_pasos, error_msg = simulador.ejecutar(funcion_str, a, b, n, regla)

        if error_msg:
            with col_plot:
                st.error(error_msg)
        else:
            with col_plot:
                with st.container(border=True):
                    st.subheader("Resultado de Integración", divider="gray")
                    
                    st.success(f"**Área aproximada:** {area:.6f}")

                    try:
                        x_sym = sp.Symbol('x')

                        f_limpia = funcion_str.lower().replace("f(x)=", "").replace("sen", "sin").strip()
                        f_sym = sp.sympify(f_limpia, locals={'e': sp.E, 'pi': sp.pi})
                        f_lamb = sp.lambdify(x_sym, f_sym, 'math')

                        margen = (b - a) * 0.1
                        x_context = np.linspace(a - margen, b + margen, 200)
                        y_context = [f_lamb(val) for val in x_context]

                        fig = go.Figure()

                        fig.add_trace(go.Scatter(
                            x=x_context, y=y_context, mode='lines',
                            line=dict(color='dodgerblue', width=3), name='f(x)'
                        ))

                        x_nodos = np.linspace(a, b, n + 1)
                        y_nodos = [f_lamb(val) for val in x_nodos]

                        if regla == "Trapecio":
                            fig.add_trace(go.Scatter(
                                x=x_nodos, y=y_nodos, fill='tozeroy', mode='lines',
                                fillcolor='rgba(255, 99, 71, 0.3)', line=dict(color='tomato', width=2),
                                name='Aproximación (Trapecios)'
                            ))
                        else:
                            x_fill = np.linspace(a, b, 200)
                            y_fill = [f_lamb(val) for val in x_fill]
                            fig.add_trace(go.Scatter(
                                x=x_fill, y=y_fill, fill='tozeroy', mode='lines',
                                fillcolor='rgba(50, 205, 50, 0.3)', line=dict(width=0), # Verde tenue
                                name='Aproximación (Simpson)'
                            ))

                        for xn, yn in zip(x_nodos, y_nodos):
                            fig.add_trace(go.Scatter(
                                x=[xn, xn], y=[0, yn], mode='lines',
                                line=dict(color='gray', width=1, dash='dot'), showlegend=False
                            ))

                        fig.add_trace(go.Scatter(
                            x=x_nodos, y=y_nodos, mode='markers',
                            marker=dict(color='crimson', size=8, symbol='square'), name='Nodos ($x_i$)'
                        ))

                        fig.update_layout(
                            xaxis_title="X", yaxis_title="Y", height=400,
                            margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        st.warning(f"Se calculó el área, pero hubo un error al graficar: {e}")

                    with st.popover("🔍 Ver desarrollo matemático y tabla de coeficientes", use_container_width=True):
                        st.markdown("### Tabla de Nodos")
                        st.info("Fijate en la columna 'Coeficiente' para ver por qué número se multiplicó cada punto de la curva.")
                        if iteraciones:
                            df_iters = pd.DataFrame(iteraciones)
                            st.dataframe(df_iters, use_container_width=True, hide_index=True)
                        
                        st.divider()
                        st.markdown("### Cálculos Analíticos y Error Verdadero")
                        for linea in log_pasos:
                            st.markdown(linea)