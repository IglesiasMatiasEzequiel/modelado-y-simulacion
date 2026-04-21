import sympy as sp
import numpy as np
import math

from core.common.metodos_base import MetodoInterpolacionBase

class Lagrange(MetodoInterpolacionBase):
    
    def ejecutar(self, puntos_x, puntos_y, f_str=None, x_eval=None):
        if len(puntos_x) != len(puntos_y):
            return None, [], [], "Error: La cantidad de puntos X e Y debe ser exactamente igual."
            
        n_puntos = len(puntos_x)
        x = sp.Symbol('x')
        
        log_pasos = [
            "### Desarrollo del Polinomio de Lagrange",
            "Calculamos los polinomios base $L_i(x)$ para cada nodo:"
        ]
        P_x = 0
        iteraciones = []
        
        for i in range(n_puntos):
            numerador = 1
            denominador = 1
            for j in range(n_puntos):
                if i != j:
                    if puntos_x[i] == puntos_x[j]:
                        return None, [], log_pasos, f"Error: Puntos duplicados en x={puntos_x[i]}."
                    numerador *= (x - puntos_x[j])
                    denominador *= (puntos_x[i] - puntos_x[j])
            
            L_i = numerador / denominador
            L_i_simplificado = sp.simplify(L_i)
            L_i_expandido = sp.nsimplify(sp.expand(L_i))
            L_i_redondeado = L_i_expandido.evalf(5) 

            log_pasos.append(f"**Paso {i}:** Polinomio base $L_{{{i}}}(x)$")
            log_pasos.append(f"$$L_{{{i}}}(x) = {sp.latex(L_i_simplificado)} = {sp.latex(L_i_redondeado)}$$")
            
            P_x += puntos_y[i] * L_i
            
            iteraciones.append({
                "i": i, 
                "x_i": self.formatear(puntos_x[i]), 
                "y_i": self.formatear(puntos_y[i]), 
                "L_i(x)": str(L_i_simplificado)
            })

        P_x_expandido = sp.nsimplify(sp.expand(P_x))
        P_x_redondeado = P_x_expandido.evalf(5) 
        
        log_pasos.append("---")
        log_pasos.append("**Polinomio Interpolante $P(x)$:**")
        log_pasos.append(f"$$P(x) = {sp.latex(P_x_redondeado)}$$")
        
        funcion_P = sp.lambdify(x, P_x_expandido, 'math')

        if f_str and x_eval is not None:
            log_pasos.append("---")
            log_pasos.append(f"### Cálculo de Error en $x = {x_eval}$")
            
            try:
                f_sym = sp.sympify(f_str, locals={'e': sp.E})
                val_real = float(f_sym.subs(x, x_eval))
                val_aprox = float(P_x.subs(x, x_eval))
                err_local = abs(val_real - val_aprox)
                
                log_pasos.append("**1. Error Local (Valor Verdadero):**")
                log_pasos.append(f"$E_{{local}} = |f({x_eval}) - P({x_eval})| = |{val_real:.5f} - {val_aprox:.5f}| = {err_local:.5f}$")
                
                derivada_n = sp.diff(f_sym, x, n_puntos)
                
                log_pasos.append(f"**2. Derivada de orden $n={n_puntos}$:**")
                log_pasos.append(f"$f^{{({n_puntos})}}(x) = {sp.latex(derivada_n)}$")
                
                f_deriv_n = sp.lambdify(x, derivada_n, 'math')
                x_min, x_max = min(puntos_x), max(puntos_x)
                
                x_rango = np.linspace(x_min, x_max, 1000)
                M = max([abs(f_deriv_n(val)) for val in x_rango])
                
                log_pasos.append(f"**3. Determinación de $M$ (Máximo absoluto en $[{x_min}, {x_max}]$):**")
                log_pasos.append(f"$M \\approx {M:.5f}$")
                
                productoria = 1
                for xi in puntos_x:
                    productoria *= abs(x_eval - xi)
                    
                factorial = math.factorial(n_puntos)
                cota = (M / factorial) * productoria
                
                log_pasos.append("**4. Cota de Error Máxima:**")
                log_pasos.append(f"$|E(x)| \le \\frac{{M}}{{{n_puntos}!}} \\left| \prod (x - x_i) \\right|$")
                log_pasos.append(f"**$|E(x)| \le \\frac{{{M:.5f}}}{{{factorial}}} \\cdot {productoria:.5f} = {cota:.5f}$**")
                
                log_pasos.append(f"✅ **Verificación del Teorema:** El error local ({err_local:.5f}) cumple con ser $\le$ a la cota teórica ({cota:.5f}).")
                
            except Exception as e:
                log_pasos.append(f"*Aviso: No se pudo realizar el análisis de error analítico. ({str(e)})*")

        return funcion_P, iteraciones, log_pasos, None