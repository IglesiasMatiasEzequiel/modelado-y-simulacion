import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sympy as sp

from core.integracion.montecarlo import MonteCarlo

def renderizar_montecarlo():
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
                
            n_puntos = st.number_input("Cantidad de Puntos (N)", min_value=10, max_value=100000, value=1000, step=500, 
                                help="Más puntos = más tiempo de cálculo, pero menor error.")
            
            st.markdown("---")
            calcular = st.button("Tirar Dados (Calcular)", type="primary", use_container_width=True)

    if calcular:
        if a >= b:
            st.error("El límite inferior 'a' debe ser menor que el límite superior 'b'.")
            return

        simulador = MonteCarlo()
        area, iteraciones, log_pasos, h_promedio, x_raw, y_raw, error_msg = simulador.ejecutar(funcion_str, a, b, n_puntos)

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

                        margen = float((b - a) * 0.1)
                        x_context = np.linspace(float(a - margen), float(b + margen), 200)
                        
                        # 1. BLINDAJE CONTRA RAÍCES NEGATIVAS (Genera 'None' si está fuera del dominio)
                        y_context = []
                        for val in x_context:
                            try:
                                y_context.append(float(f_lamb(val)))
                            except (ValueError, TypeError, ZeroDivisionError):
                                y_context.append(None) 

                        fig = go.Figure()

                        # 2. CURVA ORIGINAL
                        fig.add_trace(go.Scatter(
                            x=x_context, y=y_context, mode='lines',
                            line=dict(color='dodgerblue', width=3), name='f(x)'
                        ))

                        # 3. RECTÁNGULO DE ÁREA
                        fig.add_shape(type="rect",
                            x0=a, y0=0, x1=b, y1=float(h_promedio),
                            fillcolor="rgba(255, 165, 0, 0.3)", 
                            line=dict(color="darkorange", width=2, dash="dash"),
                        )
                        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines',
                            line=dict(color="darkorange", width=2, dash="dash"), name='Área (Valor Medio)'
                        ))

                        # 4. PREPARACIÓN DE DARDOS
                        max_plot = int(min(n_puntos, 2000))
                        x_dardos = np.array(x_raw[:max_plot], dtype=float)
                        y_curva_real = np.array(y_raw[:max_plot], dtype=float)
                        
                        # --- CÁLCULO SEGURO DE LA CAJA ---
                        # Filtramos los None para que max() funcione perfecto
                        y_context_validos = [y for y in y_context if y is not None]
                        max_y_curva = max(y_context_validos) if y_context_validos else float(h_promedio)
                        
                        # Usamos max_y_curva, YA NO usamos y_context acá
                        y_max_caja = float(max(max_y_curva, float(h_promedio) * 1.2))
                        if y_max_caja <= 0.0: 
                            y_max_caja = 1.0 

                        y_dardos = np.random.uniform(0.0, y_max_caja, len(x_dardos))

                        hits_x, hits_y = [], []
                        miss_x, miss_y = [], []

                        for i in range(len(x_dardos)):
                            if 0.0 <= y_dardos[i] <= y_curva_real[i]:
                                hits_x.append(x_dardos[i])
                                hits_y.append(y_dardos[i])
                            else:
                                miss_x.append(x_dardos[i])
                                miss_y.append(y_dardos[i])

                        # 5. DIBUJAR DARDOS
                        if hits_x:
                            fig.add_trace(go.Scatter(
                                x=hits_x, y=hits_y, mode='markers',
                                marker=dict(color='mediumseagreen', size=5, opacity=0.8),
                                name='Aciertos (Debajo de f(x))'
                            ))

                        if miss_x:
                            fig.add_trace(go.Scatter(
                                x=miss_x, y=miss_y, mode='markers',
                                marker=dict(color='crimson', size=4, opacity=0.4),
                                name='Fallos (Fuera)'
                            ))

                        fig.update_layout(
                            xaxis_title="X", yaxis_title="Y", height=400,
                            margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified"
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        import traceback
                        st.warning(f"Error al graficar: {e}")
                        st.error(traceback.format_exc())

                    # --- MODAL ANALÍTICO ---
                    with st.popover("🔍 Ver log matemático y puntos", use_container_width=True):
                        st.markdown("### Cálculos Analíticos")
                        for linea in log_pasos:
                            st.markdown(linea)
                            
                        st.divider()
                        st.markdown(f"### Muestra de Datos (Primeros {min(n_puntos, 100)} puntos)")
                        if iteraciones:
                            df_puntos_seguro = pd.DataFrame(iteraciones)
                            st.dataframe(df_puntos_seguro, use_container_width=True, hide_index=True)