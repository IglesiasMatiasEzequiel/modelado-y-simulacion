import streamlit as st
import pandas as pd
import math

from core.raices.biseccion import Biseccion
from core.common.constants import AYUDA_SINTAXIS_MATEMATICA
from utils.maths import parsear_funcion, escanear_raices
from utils.graph import generar_grafico_raiz


def renderizar_biseccion():
    col_in, col_plot, col_tab = st.columns([1, 2, 1.8]) 
    
    with col_in:
        with st.container(border=True):
            st.subheader("Parámetros", divider="gray")
            
            st.info("Ej: (x+2)*(x+1)*((x-1)**3)*(x-2)")
            funcion_str = st.text_input("Función f(x)", value="(x+2)*(x+1)*((x-1)**3)*(x-2)")
            
            with st.popover("💡 ¿Cómo escribir la función?"):
                st.markdown(AYUDA_SINTAXIS_MATEMATICA)

            col_a, col_b = st.columns(2)
            with col_a:
                a = st.number_input("a", value=-3.0, format="%.4f")
            with col_b:
                b = st.number_input("b", value=2.5, format="%.4f")
                
            col_tol, col_iter = st.columns(2)
            with col_tol:
                tol = st.number_input("Tolerancia", value=0.001, format="%.6f")
            with col_iter:
                max_iter = st.number_input("Máx. Iter.", value=50, step=1)
                
            st.divider()
            
            buscar_multiples = st.checkbox(
                "🔍 Escanear múltiples raíces", 
                value=False, 
                help="Activa la búsqueda inteligente de todas las raíces en el intervalo. Si se desactiva, aplicará el método clásico a todo el intervalo [a, b] buscando solo la primera que encuentre."
            )
                
            calcular = st.button("Ejecutar Simulación", use_container_width=True, type="primary")

    if calcular:
        try:
            f = parsear_funcion(funcion_str)
            if f is None:
                st.error("❌ Error al interpretar la función. Revisa la sintaxis matemática.")
                st.stop()

            simulador = Biseccion(tol=tol, max_iter=max_iter)
            cant_decimales_tolerancia = abs(int(math.log10(tol))) if tol > 0 else 4

            if buscar_multiples:
                sub_intervalos = escanear_raices(f, a, b)
                
                if len(sub_intervalos) == 0:
                    st.error(f"⚠️ No se detectaron cruces del eje X en el intervalo [{a}, {b}].")
                    st.stop()
                    
                with col_plot:
                    with st.container(border=True):
                        st.subheader("Gráfico y Resultados", divider="gray")
                        st.success(f"🔍 ¡Se detectaron {len(sub_intervalos)} zonas con posibles raíces! Procesando...")
                        
                        raices_encontradas = []
                        todas_iteraciones = []
                        
                        for i, (a_sub, b_sub) in enumerate(sub_intervalos):
                            st.markdown(f"#### 📍 Raíz {i+1} (Sub-intervalo [{a_sub:.2f}, {b_sub:.2f}])")
                            c, iteraciones, log_pasos, error_msg = simulador.ejecutar(f, a_sub, b_sub)
                            
                            if error_msg:
                                st.warning(f"No se pudo resolver: {error_msg}")
                            elif iteraciones:
                                raices_encontradas.append(c)
                                
                                for idx in range(len(iteraciones)):
                                    iteraciones[idx] = {"Raíz N°": i + 1, **iteraciones[idx]}
                                todas_iteraciones.extend(iteraciones)
                                
                                pasos_reales = len(iteraciones) - 1 if iteraciones[0]["Iter"] == 0 else len(iteraciones)
                                st.info(f"✅ Convergencia en {pasos_reales} iteraciones. Raíz: **{c:.{cant_decimales_tolerancia}f}**")
                                
                                with st.expander("Ver narración paso a paso"):
                                    for paso in log_pasos:
                                        st.markdown(paso)
                        
                        if raices_encontradas:
                            margen = abs(b - a) * 0.1 if a != b else 1.0
                            fig = generar_grafico_raiz(f, a - margen, b + margen, raiz=raices_encontradas, intervalo=(a, b))
                            st.plotly_chart(fig, use_container_width=True)
                
                if todas_iteraciones:
                    with col_tab:
                        with st.container(border=True):
                            st.subheader("Iteraciones Combinadas", divider="gray")
                            st.dataframe(pd.DataFrame(todas_iteraciones), use_container_width=True, hide_index=True, height=600)

            else:
                c, iteraciones, log_pasos, error_msg = simulador.ejecutar(f, a, b)
                
                if error_msg:
                    with col_plot:
                        with st.container(border=True):
                            st.subheader("Gráfico y Resultados", divider="gray")
                            st.error(error_msg)
                    return
                    
                with col_plot:
                    with st.container(border=True):
                        st.subheader("Gráfico y Resultados", divider="gray")
                        margen = (b - a) * 0.5 
                        fig = generar_grafico_raiz(f, a - margen, b + margen, c, intervalo=(a, b))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        if len(iteraciones) >= max_iter:
                            st.warning(f"Se detuvo por límite de iteraciones ({max_iter}). Raíz aprox: **{c:.{cant_decimales_tolerancia}f}**")
                        else:
                            st.success(f"Convergencia en {len(iteraciones)} iteraciones. Raíz: **{c:.{cant_decimales_tolerancia}f}**")
                        
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
                    st.subheader("Error del Sistema", divider="gray")
                    st.error(f"Error al evaluar la función. Detalle: {e}")