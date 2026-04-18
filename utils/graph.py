import numpy as np
import plotly.graph_objects as go

def generar_grafico_raiz(f, x_min, x_max, raiz=None, puntos_x=None, intervalo=None):
    if puntos_x is None:
        puntos_x = []

    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = [f(x) for x in x_vals]

    fig = go.Figure()

    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)

    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals, 
        mode='lines', 
        name='f(x)',
        line=dict(color='dodgerblue', width=2)
    ))

    if intervalo:
        a, b = intervalo
        fig.add_vline(x=a, line_dash="dot", line_color="orange", annotation_text="a", annotation_position="top right")
        fig.add_vline(x=b, line_dash="dot", line_color="orange", annotation_text="b", annotation_position="top left")
        
        fig.add_trace(go.Scatter(
            x=[a, b], y=[f(a), f(b)],
            mode='markers',
            name='Límites [a, b]',
            marker=dict(color='orange', size=10, symbol='square')
        ))

    if puntos_x:
        y_puntos = [f(x) for x in puntos_x]
        fig.add_trace(go.Scatter(
            x=puntos_x, y=y_puntos,
            mode='markers',
            name='Punto inicial (x0)',
            marker=dict(color='purple', size=10)
        ))

    if raiz is not None:
        fig.add_trace(go.Scatter(
            x=[raiz], y=[0],
            mode='markers',
            name='Raíz encontrada',
            marker=dict(color='red', size=14, symbol='x', line=dict(color='DarkRed', width=2))
        ))

    fig.update_layout(
        title="Análisis Gráfico de la Función",
        xaxis_title="Eje X",
        yaxis_title="Eje Y (Imagen)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig