import streamlit as st
import pandas as pd
import sympy as sp
import math

from core.raices.punto_fijo import PuntoFijo
from core.common.constants import AYUDA_SINTAXIS_MATEMATICA
from utils.maths import parsear_funcion
from utils.graph import generar_grafico_raiz

def renderizar_punto_fijo():
    col_in, col_plot, col_tab = st.columns([1, 2, 1.8]) 
    
    with col_in:
        with st.container(border=True):
            st.subheader("Parámetros", divider="gray")
            
            st.info("Ej: exp(-x)")
            funcion_str = st.text_input("Función g(x) despejada", value="exp(-x)")
            
            with st.popover("💡 ¿Cómo escribir la función?"):
                st.markdown(AYUDA_SINTAXIS_MATEMATICA)

            x0 = st.number_input("Valor inicial (x0)", value=0.0, format="%.6f")
                
            col_tol, col_iter = st.columns(2)
            with col_tol:
                tol = st.number_input("Tolerancia", value=0.000001, format="%.6f")
            with col_iter:
                max_iter = st.number_input("Máx. Iter.", value=50, step=1)
                
            calcular = st.button("Ejecutar Simulación", use_container_width=True, type="primary")

    if calcular:
        try:
            g = parsear_funcion(funcion_str)
            
            x_sym = sp.Symbol('x')
            expr_g = sp.sympify(funcion_str)
            expr_f = x_sym - expr_g
            f = sp.lambdify(x_sym, expr_f, 'numpy')
            
            simulador = PuntoFijo(tol=tol, max_iter=int(max_iter))
            raiz, iteraciones, log_pasos, error_msg = simulador.ejecutar(g, x0)
            
            if error_msg:
                with col_plot:
                    with st.container(border=True):
                        st.subheader("Gráfico", divider="gray")
                        st.error(error_msg)
                return
                
            cant_decimales_tolerancia = abs(int(math.log10(tol))) if tol > 0 else 4

            with col_plot:
                with st.container(border=True):
                    st.subheader("Gráfico f(x) = x - g(x)", divider="gray")
                    
                    margen = max(2.0, abs(x0 - raiz) * 2 if raiz else 2.0)
                    
                    fig = generar_grafico_raiz(f, x0 - margen, x0 + margen, raiz, puntos_x=[x0])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    if len(iteraciones) >= max_iter:
                        st.warning(f"Se detuvo por límite de iteraciones ({max_iter}). Raíz aprox: **{raiz:.{cant_decimales_tolerancia}f}**")
                    else:
                        st.success(f"Convergencia en {len(iteraciones)} iteraciones. Raíz: **{raiz:.{cant_decimales_tolerancia}f}**")
                    
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
                    st.error(f"Error al evaluar la función. Detalle: {e}")