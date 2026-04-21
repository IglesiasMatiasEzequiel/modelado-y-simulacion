import numpy as np
import sympy as sp

def parsear_funcion(funcion_str):
    x_sym = sp.Symbol("x")
    expr = sp.sympify(funcion_str)
    return sp.lambdify(x_sym, expr, "numpy")


def obtener_derivada(funcion_str):
    try:
        x = sp.Symbol('x')
        diccionario_local = {'e': sp.E}
        expr = sp.sympify(funcion_str, locals=diccionario_local)
        
        derivada_expr = sp.diff(expr, x)
        df = sp.lambdify(x, derivada_expr, 'math')
        
        return str(derivada_expr), df
        
    except Exception:
        return None, None

def calcular_aceleracion_aitken(x0, x1, x2):
    denominador = x2 - 2*x1 + x0
    return x2 if denominador == 0 else x0 - ((x1 - x0)**2) / denominador

def escanear_raices(f, a, b, particiones=100):
    intervalos_con_raices = []
    x_vals = np.linspace(a, b, particiones)
    
    for i in range(len(x_vals) - 1):
        x_izq = x_vals[i]
        x_der = x_vals[i+1]
        
        f_izq, f_der = float(f(x_izq)), float(f(x_der))
        
        if f_izq * f_der < 0:
            intervalos_con_raices.append((x_izq, x_der))
        elif f_izq == 0:
            intervalos_con_raices.append((x_izq, x_izq))
            
    return intervalos_con_raices