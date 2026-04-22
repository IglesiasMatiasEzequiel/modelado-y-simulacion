import streamlit as st
import pandas as pd
import math

from core.raices.newton_raphson import NewtonRaphson
from core.common.constants import AYUDA_SINTAXIS_MATEMATICA
from utils.maths import parsear_funcion, obtener_derivada
from utils.graph import generar_grafico_raiz

def renderizar_newton_raphson():
    col_in, col_plot, col_tab = st.columns([1, 2, 1.8]) 
    
    with col_in:
        with st.container(border=True):
            st.subheader("Parámetros", divider="gray")
            
            st.info("Ej: x**3 - 2*x - 5")
            funcion_str = st.text_input("Función f(x)", value="x**3 - 2*x - 5")
            
            with st.popover("💡 ¿Cómo escribir la función?"):
                st.markdown(AYUDA_SINTAXIS_MATEMATICA)

            x0 = st.number_input("Valor inicial (x0)", value=2.0, format="%.6f")
                
            col_tol, col_iter = st.columns(2)
            with col_tol:
                tol = st.number_input("Tolerancia", value=0.000001, format="%.6f")
            with col_iter:
                max_iter = st.number_input("Máx. Iter.", value=50, step=1)
                
            calcular = st.button("Ejecutar Simulación", use_container_width=True, type="primary")

    if calcular:
        try:
            f = parsear_funcion(funcion_str)
            
            derivada_str, f_prima = obtener_derivada(funcion_str)
            
            simulador = NewtonRaphson(tol=tol, max_iter=int(max_iter))
            raiz, iteraciones, log_pasos, error_msg = simulador.ejecutar(f, f_prima, x0, derivada_str)
            
            if error_msg:
                with col_plot:
                    with st.container(border=True):
                        st.subheader("Gráfico", divider="gray")
                        st.error(error_msg)
                return
                
            cant_decimales_tolerancia = abs(int(math.log10(tol))) if tol > 0 else 4

            with col_plot:
                with st.container(border=True):
                    st.subheader("Gráfico y Resultados", divider="gray")
                    
                    st.caption(f"**Derivada calculada analíticamente:** $f'(x) = {derivada_str}$")
                    
                    margen = max(2.0, abs(x0 - raiz) * 2 if raiz else 2.0)
                    
                    fig = generar_grafico_raiz(f, x0 - margen, x0 + margen, raiz, puntos_x=[x0])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if len(iteraciones) >= max_iter:
                        st.warning(f"Se detuvo por límite de iteraciones ({max_iter}). Raíz aprox: **{raiz:.{cant_decimales_tolerancia}f}**")
                    else:
                        st.success(f"Convergencia ultra rápida en {len(iteraciones)} iteraciones. Raíz: **{raiz:.{cant_decimales_tolerancia}f}**")
                    
                    with st.popover("🔍 Ver narración paso a paso del algoritmo", use_container_width=True):
                        st.markdown("### Historial de ejecución")
                        for linea in log_pasos:
                            st.markdown(linea)
            
            with col_tab:
                with st.container(border=True):
                    st.subheader("Iteraciones", divider="gray")
                    st.dataframe(pd.DataFrame(iteraciones), use_container_width=True, hide_index=True, height=450)
                
        except Exception as e:
            with col_plot:
                with st.container(border=True):
                    st.subheader("Gráfico", divider="gray")
                    st.error(f"Error al evaluar la función o su derivada. Detalle: {e}")