import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import numpy as np

from core.raices.biseccion import Biseccion
from core.raices.punto_fijo import PuntoFijo
from core.raices.punto_fijo_aitken import PuntoFijoAitken
from core.raices.newton_raphson import NewtonRaphson

from utils.maths import parsear_funcion, obtener_derivada
from core.common.enums import MetodoRaices

def renderizar_comparativa():
    st.header("🏁 Comparativa de Métodos")
    st.markdown("Pone a competir a los 4 algoritmos simultáneamente para evaluar su velocidad de convergencia.")

    col_in, col_out = st.columns([1, 2])

    with col_in:
        with st.container(border=True):
            st.subheader("Funciones", divider="gray")
            funcion_f_str = st.text_input("Función original f(x) = 0", value="e**-x - x")
            funcion_g_str = st.text_input("Función iterativa g(x) = x", value="e**-x", help="Requerida para Punto Fijo y Aitken")
            
            st.subheader("Parámetros Iniciales", divider="gray")
            x0 = st.number_input("Valor inicial (x0)", value=0.0, format="%.4f", help="Para Punto Fijo, Aitken y Newton")
            
            c1, c2 = st.columns(2)
            with c1:
                a = st.number_input("Límite inferior (a)", value=0.0, format="%.4f", help="Solo para Bisección")
            with c2:
                b = st.number_input("Límite superior (b)", value=1.0, format="%.4f", help="Solo para Bisección")

            c3, c4 = st.columns(2)
            with c3:
                tol = st.number_input("Tolerancia", value=0.001, format="%.6f")
            with c4:
                max_iter = st.number_input("Máx. Iter.", value=50, step=1)

            calcular = st.button("▶ Ejecutar Carrera", use_container_width=True, type="primary")

    with col_out:
        if calcular:
            f = parsear_funcion(funcion_f_str)
            g = parsear_funcion(funcion_g_str)
            derivada_str, df = obtener_derivada(funcion_f_str)
            
            if not f or not g or not df:
                st.error("❌ Error al interpretar las funciones. Revisá la sintaxis.")
                st.stop()
                
            st.info(f"**Derivada calculada automáticamente:** $f'(x) = {derivada_str}$")

            motores = {
                MetodoRaices.BISECCION: Biseccion(tol=tol, max_iter=max_iter),
                MetodoRaices.PUNTO_FIJO: PuntoFijo(tol=tol, max_iter=max_iter),
                MetodoRaices.PUNTO_FIJO_AITKEN: PuntoFijoAitken(tol=tol, max_iter=max_iter),
                MetodoRaices.NEWTON: NewtonRaphson(tol=tol, max_iter=max_iter)
            }

            resultados = []
            detalles_tablas = {}
            cant_decimales = abs(int(math.log10(tol))) if tol > 0 else 4

            with st.spinner("Ejecutando métodos..."):
                for enum_metodo, motor in motores.items():
                    
                    nombre = enum_metodo.value if hasattr(enum_metodo, 'value') else str(enum_metodo)
                    
                    try:
                        if enum_metodo == MetodoRaices.BISECCION:
                            raiz, iteraciones, _, error_msg = motor.ejecutar(f, a, b)
                        elif enum_metodo in [MetodoRaices.PUNTO_FIJO, MetodoRaices.PUNTO_FIJO_AITKEN]:
                            raiz, iteraciones, _, error_msg = motor.ejecutar(g, x0)
                        elif enum_metodo == MetodoRaices.NEWTON:
                            raiz, iteraciones, _, error_msg = motor.ejecutar(f, df, x0, derivada_str) 

                        detalles_tablas[nombre] = {
                            "iteraciones": iteraciones if iteraciones else [],
                            "raiz": raiz,
                            "error": error_msg
                        }

                        if error_msg:
                            estado = f"❌ Falló: {error_msg}"
                            raiz_str, iters_str, err_str = "-", "-", "-"
                        else:
                            estado = "✅ Éxito"
                            pasos_reales = len(iteraciones) - 1 if iteraciones and iteraciones[0].get("Iter") == 0 else len(iteraciones)
                            raiz_str = f"{raiz:.{cant_decimales}f}"
                            iters_str = str(pasos_reales)
                            err_str = iteraciones[-1].get("Error", "-") if iteraciones else "0"

                    except Exception as e:
                        estado = f"💥 Error de ejecución: {e}"
                        raiz_str, iters_str, err_str = "-", "-", "-"
                        detalles_tablas[nombre] = {"iteraciones": [], "raiz": None, "error": str(e)}

                    resultados.append({
                        "Método": nombre,
                        "Estado": estado,
                        "Raíz Aprox.": raiz_str,
                        "Iteraciones": iters_str,
                        "Error Final": err_str
                    })

            tab_resumen, tab_grafico, tab_tablas = st.tabs(["🏆 Resumen", "📈 Gráfico Unificado", "📊 Tablas de Iteración"])
            
            with tab_resumen:
                st.subheader("Resultados de la Simulación", divider="gray")
                st.dataframe(
                    pd.DataFrame(resultados), 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "Método": st.column_config.TextColumn("Algoritmo", width="medium"),
                        "Estado": st.column_config.TextColumn("Resultado", width="large")
                    }
                )

            with tab_grafico:
                st.subheader("Análisis Visual", divider="gray")
                try:
                    fig = go.Figure()

                    x_min = min(a, x0) - 1.0
                    x_max = max(b, x0) + 1.0
                    for d in detalles_tablas.values():
                        if d["raiz"] is not None:
                            x_min = min(x_min, d["raiz"] - 0.5)
                            x_max = max(x_max, d["raiz"] + 0.5)

                    x_vals = np.linspace(x_min, x_max, 300)

                    fig.add_trace(go.Scatter(x=x_vals, y=[f(v) for v in x_vals], name="f(x)", line=dict(color='blue', width=2)))
                    fig.add_trace(go.Scatter(x=x_vals, y=[g(v) for v in x_vals], name="g(x)", line=dict(color='green', dash='dash')))
                    fig.add_trace(go.Scatter(x=x_vals, y=x_vals, name="y = x", line=dict(color='gray', dash='dot')))
                    fig.add_hline(y=0, line_dash="solid", line_color="black", opacity=0.3)

                    simbolos_colores = ['red', 'purple', 'orange', 'cyan']
                    for i, (nombre_metodo, info) in enumerate(detalles_tablas.items()):
                        r = info["raiz"]
                        if r is not None:
                            fig.add_trace(go.Scatter(
                                x=[r], y=[0], mode='markers', name=f"Raíz ({nombre_metodo})",
                                marker=dict(size=12, symbol='x', line=dict(width=2), color=simbolos_colores[i % len(simbolos_colores)])
                            ))

                    fig.update_layout(height=450, margin=dict(l=10, r=10, t=30, b=10), hovermode="x unified")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"No se pudo generar el gráfico unificado. Detalle: {e}")

            with tab_tablas:
                st.subheader("Desglose paso a paso", divider="gray")
                
                metodos_exitosos = [nombre for nombre, data in detalles_tablas.items() if data["iteraciones"]]
                
                if metodos_exitosos:
                    
                    sub_tabs = st.tabs(metodos_exitosos)
                    for i, nombre_metodo in enumerate(metodos_exitosos):
                        with sub_tabs[i]:
                            df_iters = pd.DataFrame(detalles_tablas[nombre_metodo]["iteraciones"])
                            st.dataframe(df_iters, use_container_width=True, hide_index=True)
                else:
                    st.info("Ningún método generó iteraciones válidas.")