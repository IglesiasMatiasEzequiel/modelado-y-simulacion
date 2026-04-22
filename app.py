import streamlit as st
from ui.raices.vistas_biseccion import renderizar_biseccion
from ui.raices.vistas_punto_fijo import renderizar_punto_fijo
from ui.raices.vistas_punto_fijo_aitken import renderizar_punto_fijo_aitaken
from ui.raices.vistas_newton_raphson import renderizar_newton_raphson
from ui.raices.vistas_comparativa import renderizar_comparativa
from ui.interpolacion.vistas_lagrange import renderizar_lagrange
from ui.derivacion.vistas_diferencias_finitas import renderizar_diferencias_finitas
from ui.integracion.vistas_newton_cotes import renderizar_newton_cotes
from ui.integracion.vistas_montecarlo import renderizar_montecarlo
from ui.integracion.vistas_montecarlo_dobles import renderizar_montecarlo_doble
from ui.ecuaciones.vistas_edo import renderizar_edo
from ui.ecuaciones.vistas_edo_comparativa import renderizar_comparativa_edo

from core.common.enums import Categoria, MetodoRaices, MetodoInterpolacion, MetodoDerivacion, MetodoIntegracion, MetodoEcuaciones
from core.common.constants import INFO_METODOS

st.set_page_config(page_title="Simulador de Métodos Numéricos", layout="wide")

st.markdown(
    """
    <style>
    
    [data-testid="stNumberInputStepUp"] {
        display: none;
    }
    
    [data-testid="stNumberInputStepDown"] {
        display: none;
    }
    
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Modelado y Simulación - Métodos Numéricos")

with st.container(border=True):
    col_cat, col_met = st.columns(2)
    
    with col_cat:
        opciones_categorias = [c.value for c in Categoria]
        categoria_seleccionada = st.radio("Categoría de Problema", opciones_categorias, horizontal=True)
        
    opciones_metodos = []

    with col_met:
        if categoria_seleccionada == Categoria.RAICES:
            opciones_metodos = [m.value for m in MetodoRaices]
        elif categoria_seleccionada == Categoria.INTERPOLACION:
            opciones_metodos = [m.value for m in MetodoInterpolacion]
        elif categoria_seleccionada == Categoria.DERIVACION:
            opciones_metodos = [m.value for m in MetodoDerivacion]
        elif categoria_seleccionada == Categoria.INTEGRACION:
            opciones_metodos = [m.value for m in MetodoIntegracion]
        elif categoria_seleccionada == Categoria.ECUACIONES:
            opciones_metodos = [m.value for m in MetodoEcuaciones]
            
        metodo_seleccionado = st.selectbox("Seleccione el método", opciones_metodos, label_visibility="collapsed")
        
        with st.popover(f"ℹ️ Información sobre {metodo_seleccionado}", use_container_width=True):
            descripcion = INFO_METODOS.get(metodo_seleccionado, "No hay información disponible para este método.")
            st.markdown(descripcion)

st.write("")

if categoria_seleccionada == Categoria.RAICES:
    if metodo_seleccionado == MetodoRaices.BISECCION: renderizar_biseccion()
    elif metodo_seleccionado == MetodoRaices.PUNTO_FIJO: renderizar_punto_fijo()
    elif metodo_seleccionado == MetodoRaices.PUNTO_FIJO_AITKEN: renderizar_punto_fijo_aitaken()
    elif metodo_seleccionado == MetodoRaices.NEWTON: renderizar_newton_raphson()
    elif metodo_seleccionado == MetodoRaices.COMPARATIVA: renderizar_comparativa()
elif categoria_seleccionada == Categoria.INTERPOLACION:
    if metodo_seleccionado == MetodoInterpolacion.LAGRANGE: renderizar_lagrange()
elif categoria_seleccionada == Categoria.DERIVACION:
    if metodo_seleccionado == MetodoDerivacion.DIFERENCIAS_FINITAS: renderizar_diferencias_finitas()
elif categoria_seleccionada == Categoria.INTEGRACION:
    if metodo_seleccionado == MetodoIntegracion.NEWTON_COTES : renderizar_newton_cotes()
    elif metodo_seleccionado == MetodoIntegracion.MONTECARLO : renderizar_montecarlo()
    elif metodo_seleccionado == MetodoIntegracion.MONTECARLO_DOBLE : renderizar_montecarlo_doble()
elif categoria_seleccionada == Categoria.ECUACIONES:
    if metodo_seleccionado == MetodoEcuaciones.EDO : renderizar_edo()
    elif metodo_seleccionado == MetodoEcuaciones.EDO_COMPARATIVA : renderizar_comparativa_edo()

