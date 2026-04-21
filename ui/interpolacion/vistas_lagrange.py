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
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )
            
            st.subheader("Análisis de Error (Opcional)", divider="gray")
            
            with st.expander("📚 ¿Qué tipos de error calculamos?"):
                st.markdown("""
                **1. Error Local (Verdadero):**
                Mide la diferencia exacta entre el valor real de la función $f(x)$ y la aproximación de nuestro polinomio $P(x)$. Solo se puede calcular si conocemos la función original.
                
                **2. Cota de Error (Teórica):**
                Nos da el 'peor escenario posible'. Basado en el Teorema de Interpolación, usa la derivada máxima para garantizar que el error verdadero **nunca** superará este límite.
                """)
                
            funcion_str = st.text_input("Función original f(x)", value="", help="Ej: sin(x), e**x. Dejar vacío si no se conoce.")
            punto_eval = st.number_input("Punto a evaluar (x)", value=2.0000, format="%.6f")
            
            calcular = st.button("Calcular Polinomio", use_container_width=True, type="primary")

    if calcular:
        df_limpio = df_editado.dropna()
        
        if len(df_limpio) < 2:
            st.error("Se necesitan al menos 2 puntos para trazar una interpolación.")
            return
            
        if df_limpio["X"].duplicated().any():
            st.error("Los valores de X deben ser únicos.")
            return
            
        x_list = df_limpio["X"].tolist()
        y_list = df_limpio["Y"].tolist()
        
        try:
            simulador = Lagrange()
            
            if funcion_str.strip() != "":
                f_interp, iteraciones, log_pasos, error_msg = simulador.ejecutar(x_list, y_list, f_str=funcion_str, x_eval=punto_eval)
            else:
                f_interp, iteraciones, log_pasos, error_msg = simulador.ejecutar(x_list, y_list)
            
            if error_msg:
                st.error(error_msg)
            else:
                with col_plot:
                    with st.container(border=True):
                        st.subheader("Resultado de Interpolación", divider="gray")
                        st.success("¡Polinomio encontrado exitosamente!")

                        formula_final = ""
                        for linea in log_pasos:
                            if linea.startswith("$$P(x) ="):
                                formula_final = linea

                        st.markdown("**Polinomio simplificado:**")
                        st.markdown(formula_final)
                        
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
                            hovermode="x unified",
                            margin=dict(l=0, r=0, t=40, b=0),
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        with st.popover("🔍 Ver desarrollo matemático paso a paso", use_container_width=True):
                            st.markdown("### Resumen de Polinomios Base")
                            if iteraciones:
                                df_iters = pd.DataFrame(iteraciones)
                                st.dataframe(df_iters, use_container_width=True, hide_index=True)
                            
                            st.divider()
                            st.markdown("### Cálculos Analíticos")
                            for linea in log_pasos:
                                st.markdown(linea)
                            
        except Exception as e:
            with col_plot:
                st.error(f"Error al calcular la interpolación. Detalle: {e}")