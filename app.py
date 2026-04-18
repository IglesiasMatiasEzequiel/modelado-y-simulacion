import streamlit as st
from ui.raices.vistas_biseccion import renderizar_biseccion
from ui.raices.vistas_punto_fijo import renderizar_punto_fijo
from ui.raices.vistas_punto_fijo_aitken import renderizar_punto_fijo_aitaken
from ui.raices.vistas_newton_raphson import renderizar_newton_raphson
from ui.interpolacion.vistas_lagrange import renderizar_lagrange

from core.common.enums import Categoria, MetodoRaices, MetodoInterpolacion

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
        
    with col_met:
        if categoria_seleccionada == Categoria.RAICES:
            opciones_metodos = [m.value for m in MetodoRaices]
            metodo_seleccionado = st.selectbox("Seleccione el método", opciones_metodos, label_visibility="collapsed")
        else:
            opciones_metodos = [m.value for m in MetodoInterpolacion]
            metodo_seleccionado = st.selectbox("Seleccione el método", opciones_metodos, label_visibility="collapsed")

st.write("")

if categoria_seleccionada == Categoria.RAICES:
    if metodo_seleccionado == MetodoRaices.BISECCION: renderizar_biseccion()
    elif metodo_seleccionado == MetodoRaices.PUNTO_FIJO: renderizar_punto_fijo()
    elif metodo_seleccionado == MetodoRaices.PUNTO_FIJO_AITKEN: renderizar_punto_fijo_aitaken()
    elif metodo_seleccionado == MetodoRaices.NEWTON: renderizar_newton_raphson()
elif categoria_seleccionada == Categoria.INTERPOLACION:
    if metodo_seleccionado == MetodoInterpolacion.LAGRANGE: renderizar_lagrange()

