import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sympy as sp

from core.derivacion.diferencias_finitas import DiferenciasFinitas

def renderizar_diferencias_finitas():
    col_in, col_plot = st.columns([1, 2])
    
    with col_in:
        with st.container(border=True):
            st.subheader("Configuración", divider="gray")
            st.info("Al mover el deslizador, el cálculo se actualiza automáticamente.")
            
            funcion_str = st.text_input("Función f(x)", value="sin(x)")
            x_eval = st.number_input("Punto de evaluación (x₀)", value=1.0, step=0.1)
            
            st.markdown("---")
            st.markdown("### Tamaño del Paso (h)")
            
            h = st.slider("Mové este control para ajustar la precisión", 
                          min_value=0.05, max_value=2.0, value=0.8, step=0.05)
            
            st.markdown("---")
            metodo_vis = st.radio("Método a visualizar en el gráfico:", 
                                  ["Central", "Hacia Adelante", "Hacia Atrás"])

    try:
        simulador = DiferenciasFinitas()
        deriv_central, iteraciones, log_pasos, error_msg = simulador.ejecutar(funcion_str, x_eval, h)
        
        if error_msg:
            with col_plot:
                st.error(error_msg)
        else:
            with col_plot:
                with st.container(border=True):
                    st.subheader("Visualización Dinámica", divider="gray")
                    
                    x_sym = sp.Symbol('x')
                    f_str_limpio = funcion_str.lower().replace("f(x)=", "").replace("sen", "sin").strip()
                    f_sym = sp.sympify(f_str_limpio, locals={'e': sp.E, 'pi': sp.pi})
                    f_lamb = sp.lambdify(x_sym, f_sym, 'math')
                    
                    deriv_analitica = sp.diff(f_sym, x_sym)
                    deriv_lamb = sp.lambdify(x_sym, deriv_analitica, 'math')
                    y_eval = f_lamb(x_eval)
                    m_real = deriv_lamb(x_eval)
                    
                    x_range = np.linspace(x_eval - 3, x_eval + 3, 200)
                    y_range = [f_lamb(val) for val in x_range]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', 
                                             line=dict(color='dodgerblue', width=3), name='f(x)'))
                    
                    y_tangente = [m_real * (val - x_eval) + y_eval for val in x_range]
                    fig.add_trace(go.Scatter(x=x_range, y=y_tangente, mode='lines', 
                                             line=dict(color='mediumseagreen', width=2, dash='dash'), 
                                             name='Derivada Real (Tangente)'))
                    
                    if metodo_vis == "Hacia Adelante":
                        x_nodos = [x_eval, x_eval + h]
                    elif metodo_vis == "Hacia Atrás":
                        x_nodos = [x_eval - h, x_eval]
                    else:
                        x_nodos = [x_eval - h, x_eval + h]
                        
                    y_nodos = [f_lamb(val) for val in x_nodos]
                    m_num = (y_nodos[1] - y_nodos[0]) / (x_nodos[1] - x_nodos[0])
                    
                    y_secante = [m_num * (val - x_eval) + y_eval for val in x_range]
                    fig.add_trace(go.Scatter(x=x_range, y=y_secante, mode='lines', 
                                             line=dict(color='crimson', width=2), 
                                             name=f'Aprox. {metodo_vis}'))
                    
                    fig.add_trace(go.Scatter(x=x_nodos, y=y_nodos, mode='markers', 
                                             marker=dict(color='crimson', size=10, symbol='diamond'), 
                                             name='Nodos Usados (x±h)'))
                    
                    fig.add_trace(go.Scatter(x=[x_eval], y=[y_eval], mode='markers', 
                                             marker=dict(color='black', size=12), name='Punto x₀'))
                    
                    y_min, y_max = min(y_nodos) - 2, max(y_nodos) + 2
                    fig.update_layout(xaxis_title="X", yaxis_title="Y", height=400,
                                      yaxis=dict(range=[y_min, y_max]),
                                      margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("### Cuadro Comparativo de Errores")
                    if iteraciones:
                        df_iters = pd.DataFrame(iteraciones)

                        st.dataframe(df_iters.style.highlight_min(subset=['Error Verdadero'], color='lightgreen'), 
                                     use_container_width=True, hide_index=True)
                    
                    with st.popover("🔍 Ver cálculo analítico paso a paso", use_container_width=True):
                        for linea in log_pasos:
                            st.markdown(linea)

    except Exception as e:
         st.error(f"Ocurrió un error en la vista: {e}")