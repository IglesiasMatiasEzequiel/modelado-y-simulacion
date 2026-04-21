import sympy as sp
from core.common.metodos_base import MetodoDerivacionBase

class DiferenciasFinitas(MetodoDerivacionBase):
    
    def ejecutar(self, f_str, x_eval, h):
        x = sp.Symbol('x')
        
        log_pasos = [
            f"### Derivación Numérica por Diferencias Finitas",
            f"**Datos iniciales:** $x_0 = {x_eval}$, $h = {h}$"
        ]
        
        try:
            f_str_limpio = f_str.lower().replace("f(x)=", "").replace("f(x) =", "").replace("y=", "").replace("y =", "").replace("sen", "sin").strip()
            f_sym = sp.sympify(f_str_limpio, locals={'e': sp.E, 'pi': sp.pi})
            
            x_adelante = x_eval + h
            x_atras = x_eval - h
            
            fx = float(f_sym.subs(x, x_eval).evalf()) #Sustituye x por x_eval y luego evalúa la fórmula como float
            fx_adelante = float(f_sym.subs(x, x_adelante).evalf())
            fx_atras = float(f_sym.subs(x, x_atras).evalf())
            
            log_pasos.append("---")
            log_pasos.append("**1. Evaluación de la función en los nodos:**")
            log_pasos.append(f"* $f(x_0) = f({x_eval}) = {fx:.6f}$")
            log_pasos.append(f"* $f(x_0 + h) = f({x_adelante}) = {fx_adelante:.6f}$")
            log_pasos.append(f"* $f(x_0 - h) = f({x_atras}) = {fx_atras:.6f}$")
            
            #Aproximar derivada Progesiva (Adelante)
            deriv_adelante = (fx_adelante - fx) / h 

            #Aproximar derivada Progesiva (Atrás)
            deriv_atras = (fx - fx_atras) / h 

            #Aproximar derivada Progesiva (Central)
            deriv_central = (fx_adelante - fx_atras) / (2 * h) 
            
            log_pasos.append("---")
            log_pasos.append("**2. Aplicación de Fórmulas:**")
            
            log_pasos.append("**Hacia Adelante (Progresiva):**")
            log_pasos.append(f"$$f'(x) \\approx \\frac{{f(x_0 + h) - f(x_0)}}{{h}} = \\frac{{{fx_adelante:.6f} - {fx:.6f}}}{{{h}}} = {deriv_adelante:.6f}$$")
            
            log_pasos.append("**Hacia Atrás (Regresiva):**")
            log_pasos.append(f"$$f'(x) \\approx \\frac{{f(x_0) - f(x_0 - h)}}{{h}} = \\frac{{{fx:.6f} - {fx_atras:.6f}}}{{{h}}} = {deriv_atras:.6f}$$")
            
            log_pasos.append("**Central:**")
            log_pasos.append(f"$$f'(x) \\approx \\frac{{f(x_0 + h) - f(x_0 - h)}}{{2h}} = \\frac{{{fx_adelante:.6f} - {fx_atras:.6f}}}{{{2*h}}} = {deriv_central:.6f}$$")
            
            derivada_analitica = sp.diff(f_sym, x)
            val_real = float(derivada_analitica.subs(x, x_eval).evalf())
            
            err_adelante = abs(val_real - deriv_adelante)
            err_atras = abs(val_real - deriv_atras)
            err_central = abs(val_real - deriv_central)
            
            log_pasos.append("---")
            log_pasos.append("**3. Análisis de Error:**")
            log_pasos.append(f"Derivada analítica real: $f'(x) = {sp.latex(derivada_analitica)}$")
            log_pasos.append(f"Valor real en $x_0$: $f'({x_eval}) = {val_real:.6f}$")
            
            iteraciones = [
                {"Método": "Adelante", "Resultado": self.formatear(deriv_adelante), "Error Verdadero": self.formatear(err_adelante)},
                {"Método": "Atrás", "Resultado": self.formatear(deriv_atras), "Error Verdadero": self.formatear(err_atras)},
                {"Método": "Central", "Resultado": self.formatear(deriv_central), "Error Verdadero": self.formatear(err_central)}
            ]
            
            return deriv_central, iteraciones, log_pasos, None
            
        except Exception as e:
            return None, [], [], f"Error al procesar la función: {str(e)}"