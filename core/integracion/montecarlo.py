import sympy as sp
import numpy as np
from core.common.metodos_base import MetodoIntegracionBase

class MonteCarlo(MetodoIntegracionBase):
    
    def ejecutar(self, f_str, a, b, n_puntos):
       
        log_pasos = [
            f"### Integración Probabilística: Monte Carlo",
            f"**Datos:** Límite inferior $a = {a}$, Límite superior $b = {b}$, Muestras $N = {n_puntos}$"
        ]

        x = sp.Symbol('x')
        try:
            # 1. Preparación y Muestreo
            f_str_limpio = f_str.lower().replace("f(x)=", "").replace("y=", "").replace("sen", "sin").strip()
            f_sym = sp.sympify(f_str_limpio, locals={'e': sp.E, 'pi': sp.pi})
            f_lamb = sp.lambdify(x, f_sym, 'math')

            # Generamos los números aleatorios uniformes en [a, b]
            x_raw = np.random.uniform(a, b, n_puntos)
            y_raw = np.array([float(f_lamb(val)) for val in x_raw])
            
            # 2. Cálculos Estadísticos del Estimador
            promedio_y = np.mean(y_raw)
            base = float(b - a)
            area_estimada = base * promedio_y

            # Varianza de la función f(X)
            varianza_f = np.var(y_raw, ddof=1)
            desviacion_f = np.std(y_raw, ddof=1)
            
            # Varianza del Estimador: Var[I_hat] = ((b-a)^2 / N) * Var[f(X)]
            varianza_estimador = ((base**2) / n_puntos) * varianza_f
            
            # Error Estándar (Desviación del estimador): sigma_I_hat = (b-a)*sigma_f / sqrt(N)
            error_estandar = (base * desviacion_f) / np.sqrt(n_puntos)
            
            # Intervalo de Confianza al 95% (Z = 1.96)
            intervalo_min = area_estimada - (1.96 * error_estandar)
            intervalo_max = area_estimada + (1.96 * error_estandar)

            # --- LOG DE PASOS CON FÓRMULAS DE PROBABILIDAD ---
            log_pasos.append("---")
            log_pasos.append("**1. Esperanza del Estimador ($E[\\hat{I}]$):**")
            log_pasos.append("El estimador del valor medio es insesgado:")
            log_pasos.append(f"$$E[\\hat{{I}}] = I = \\int_{a}^{b} f(x) dx \\approx {area_estimada:.6f}$$")

            log_pasos.append("---")
            log_pasos.append("**2. Análisis de Varianza:**")
            log_pasos.append("Estimación de la varianza de la función $Var[f(X)]$:")
            log_pasos.append(f"$$Var[f(X)] = \\int_{a}^{b} \\frac{1}{b-a} f^2(x) dx - I^2 \\approx {varianza_f:.6f}$$")
            
            log_pasos.append("Varianza del estimador de la integral:")
            log_pasos.append(f"$$Var[\\hat{{I}}] = \\frac{{(b-a)^2}}{{N}} Var[f(X)] = \\frac{{({base})^2}}{{{n_puntos}}} ({varianza_f:.6f}) = {varianza_estimador:.6f}$$")

            log_pasos.append("---")
            log_pasos.append("**3. Desviación y Error Estándar:**")
            log_pasos.append("La desviación estándar del estimador es la medida de precisión del método:")
            log_pasos.append(f"$$\\sigma_{{\\hat{{I}}}} = \\sqrt{{Var[\\hat{{I}}]}} = \\frac{{(b-a) \\sigma_f}}{{\\sqrt{{N}}}} = \\frac{{({base}) \\cdot {desviacion_f:.6f}}}{{\\sqrt{{{n_puntos}}}}} = {error_estandar:.6f}$$")
            
            log_pasos.append(f"**Intervalo de Confianza (95%):** $[{intervalo_min:.5f}, {intervalo_max:.5f}]$")

            # Preparación de datos para la vista
            iteraciones = []
            for i in range(min(n_puntos, 100)):
                iteraciones.append({
                    "Muestra": i + 1,
                    "x_i": self.formatear(x_raw[i]),
                    "f(x_i)": self.formatear(y_raw[i])
                })

            # Error analítico si SymPy puede resolver la integral
            try:
                integral_real = sp.integrate(f_sym, (x, a, b))
                val_real = float(integral_real.evalf())
                err_abs = abs(val_real - area_estimada)
                log_pasos.append("---")
                log_pasos.append(f"**4. Error Verdadero:** $|{val_real:.6f} - {area_estimada:.6f}| = {err_abs:.6f}$")
            except:
                pass

            return area_estimada, iteraciones, log_pasos, promedio_y, x_raw, y_raw, None

        except Exception as e:
            return None, [], [], 0, [], [], f"Error en el motor Monte Carlo: {str(e)}"