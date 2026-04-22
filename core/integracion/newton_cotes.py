import sympy as sp
import numpy as np
from core.common.metodos_base import MetodoIntegracionBase

class NewtonCotes(MetodoIntegracionBase):
    
    def ejecutar(self, f_str, a, b, n, regla="Trapecio"):
        
        log_pasos = [
            f"### Integración Numérica: Regla de {regla}",
            f"**Datos iniciales:** Límite inferior $a = {a}$, Límite superior $b = {b}$, Subintervalos $n = {n}$"
        ]

        if regla == "Simpson 1/3" and n % 2 != 0:
            return None, [], log_pasos, "Error: Para usar la regla de Simpson 1/3, la cantidad de subintervalos 'n' debe ser un número PAR."
            
        if regla == "Simpson 3/8" and n % 3 != 0:
            return None, [], log_pasos, "Error: Para usar la regla de Simpson 3/8, la cantidad de subintervalos 'n' debe ser MÚLTIPLO DE 3 (ej: 3, 6, 9)."

        x = sp.Symbol('x')
        try:
            f_str_limpio = f_str.lower().replace("f(x)=", "").replace("y=", "").replace("sen", "sin").strip()
            f_sym = sp.sympify(f_str_limpio, locals={'e': sp.E, 'pi': sp.pi})

            h = (b - a) / n

            log_pasos.append(f"**1. Cálculo del paso ($h$):**")
            log_pasos.append(f"$$h = \\frac{{b - a}}{{n}} = \\frac{{{b} - {a}}}{{{n}}} = {h:.6f}$$")

            nodos_x = [a + i * h for i in range(n + 1)]
            nodos_y = [float(f_sym.subs(x, xi).evalf()) for xi in nodos_x]

            log_pasos.append("---")
            log_pasos.append("**2. Evaluación de la función en los nodos:**")

            iteraciones = []
            area_total = 0

            if regla == "Trapecio":
                suma_intermedia = sum(nodos_y[1:-1])
                area_total = (h / 2) * (nodos_y[0] + 2 * suma_intermedia + nodos_y[-1])

                log_pasos.append(f"Fórmula: $\\text{{Área}} \\approx \\frac{{h}}{{2}} \\left[ f(x_0) + 2 \\sum_{{i=1}}^{{n-1}} f(x_i) + f(x_n) \\right]$")
                log_pasos.append(f"$$Área \\approx \\frac{{{h:.6f}}}{{2}} \\left[ {nodos_y[0]:.6f} + 2({suma_intermedia:.6f}) + {nodos_y[-1]:.6f} \\right] = {area_total:.6f}$$")

                for i in range(n + 1):
                    coef = 1 if i == 0 or i == n else 2
                    iteraciones.append({
                        "i": i, "x_i": self.formatear(nodos_x[i]), "f(x_i)": self.formatear(nodos_y[i]), "Coeficiente": coef
                    })

            elif regla == "Simpson 1/3":
                suma_impares = sum(nodos_y[1:-1:2])
                suma_pares = sum(nodos_y[2:-2:2])
                area_total = (h / 3) * (nodos_y[0] + 4 * suma_impares + 2 * suma_pares + nodos_y[-1])

                log_pasos.append(f"Fórmula: $\\text{{Área}} \\approx \\frac{{h}}{{3}} \\left[ f(x_0) + 4 \\sum f(x_{{impares}}) + 2 \\sum f(x_{{pares}}) + f(x_n) \\right]$")
                log_pasos.append(f"$$Área \\approx \\frac{{{h:.6f}}}{{3}} \\left[ {nodos_y[0]:.6f} + 4({suma_impares:.6f}) + 2({suma_pares:.6f}) + {nodos_y[-1]:.6f} \\right] = {area_total:.6f}$$")

                for i in range(n + 1):
                    if i == 0 or i == n: coef = 1
                    elif i % 2 != 0:     coef = 4
                    else:                coef = 2
                    iteraciones.append({
                        "i": i, "x_i": self.formatear(nodos_x[i]), "f(x_i)": self.formatear(nodos_y[i]), "Coeficiente": coef
                    })
                    
            elif regla == "Simpson 3/8":

                suma_mult_3 = sum([nodos_y[i] for i in range(3, n, 3)])
                suma_resto = sum([nodos_y[i] for i in range(1, n) if i % 3 != 0])
                
                area_total = (3 * h / 8) * (nodos_y[0] + 3 * suma_resto + 2 * suma_mult_3 + nodos_y[-1])

                log_pasos.append(f"Fórmula: $\\text{{Área}} \\approx \\frac{{3h}}{{8}} \\left[ f(x_0) + 3 \\sum f(x_{{resto}}) + 2 \\sum f(x_{{múltiplos\\;de\\;3}}) + f(x_n) \\right]$")
                log_pasos.append(f"$$Área \\approx \\frac{{3({h:.6f})}}{{8}} \\left[ {nodos_y[0]:.6f} + 3({suma_resto:.6f}) + 2({suma_mult_3:.6f}) + {nodos_y[-1]:.6f} \\right] = {area_total:.6f}$$")

                for i in range(n + 1):
                    if i == 0 or i == n: coef = 1
                    elif i % 3 == 0:     coef = 2
                    else:                coef = 3
                    iteraciones.append({
                        "i": i, "x_i": self.formatear(nodos_x[i]), "f(x_i)": self.formatear(nodos_y[i]), "Coeficiente": coef
                    })

            log_pasos.append("---")
            log_pasos.append("**3. Análisis de Error Local:**")
            
            try:
                integral_real = sp.integrate(f_sym, (x, a, b))
                val_real = float(integral_real.evalf())
                err_abs = abs(val_real - area_total)
                
                log_pasos.append(f"Integral exacta analítica: $\\int_{{{a}}}^{{{b}}} f(x) dx = {val_real:.6f}$")
                log_pasos.append(f"Error Verdadero: $|{val_real:.6f} - {area_total:.6f}| = {err_abs:.6f}$")
            except Exception:
                log_pasos.append("*Aviso: No se pudo calcular la primitiva analítica para obtener el error exacto.*")

            log_pasos.append("---")
            log_pasos.append("**4. Cota de Error de Truncamiento Teórico ($E_T$):**")

            try:
                if regla == "Trapecio":
                    orden_deriv = 2
                    coef_str = "-\\frac{b-a}{12} h^2"
                    coef_num = -((b - a) / 12) * (h ** 2)
                elif regla == "Simpson 1/3":
                    orden_deriv = 4
                    coef_str = "-\\frac{b-a}{180} h^4"
                    coef_num = -((b - a) / 180) * (h ** 4)
                elif regla == "Simpson 3/8":
                    orden_deriv = 4
                    coef_str = "-\\frac{b-a}{80} h^4"
                    coef_num = -((b - a) / 80) * (h ** 4)

                derivada_sym = sp.diff(f_sym, x, orden_deriv)
                log_pasos.append(f"**Paso A:** Derivada de orden $n={orden_deriv}$")
                log_pasos.append(f"$f^{{({orden_deriv})}}(x) = {sp.latex(derivada_sym)}$")

                f_deriv_lamb = sp.lambdify(x, derivada_sym, 'math')
                x_rango = np.linspace(a, b, 1000)
                M = max([abs(f_deriv_lamb(val)) for val in x_rango])
                
                log_pasos.append(f"**Paso B:** Encontrar el máximo absoluto $M$ en el intervalo $[{a}, {b}]$")
                log_pasos.append(f"$\\max |f^{{({orden_deriv})}}(x)| = M \\approx {M:.6f}$")

                cota_error = abs(coef_num * M)
                log_pasos.append(f"**Paso C:** Calcular la Cota de Error")
                log_pasos.append(f"$|E_T| \\le \\left| {coef_str} \\right| \\cdot M$")
                log_pasos.append(f"$|E_T| \\le \\left| {coef_num:.6f} \\right| \\cdot {M:.6f} = {cota_error:.6f}$")

                if err_abs is not None:
                    if err_abs <= cota_error:
                        log_pasos.append(f"✅ **Verificación del Teorema:** El Error Verdadero ({err_abs:.6f}) cumple con ser $\\le$ a la Cota de Truncamiento.")
                    else:
                        log_pasos.append(f"⚠️ **Aviso:** El error superó la cota. Esto puede deberse a errores de redondeo de punto flotante de la computadora.")

            except Exception as e:
                log_pasos.append(f"*Aviso: No se pudo realizar el cálculo analítico de la cota teórica. ({str(e)})*")

            return area_total, iteraciones, log_pasos, None

        except Exception as e:
            return None, [], [], f"Error al procesar la integración: {str(e)}"