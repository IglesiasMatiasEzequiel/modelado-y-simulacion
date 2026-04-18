import sympy as sp

def parsear_funcion(funcion_str):
    x_sym = sp.Symbol("x")
    expr = sp.sympify(funcion_str)
    return sp.lambdify(x_sym, expr, "numpy")


def obtener_derivada(funcion_str):

    x_sym = sp.Symbol("x")
    expr = sp.sympify(funcion_str)

    derivada_expr = sp.diff(expr, x_sym)
    f_prima = sp.lambdify(x_sym, derivada_expr, "numpy")

    return f_prima, str(derivada_expr)

def calcular_aceleracion_aitken(x0, x1, x2):
    denominador = x2 - 2*x1 + x0
    return x2 if denominador == 0 else x0 - ((x1 - x0)**2) / denominador