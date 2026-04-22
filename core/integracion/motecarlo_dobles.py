import sympy as sp
import numpy as np
import pandas as pd

class MonteCarloDoble:
    def formatear(self, valor):
        return round(float(valor), 6)

    def ejecutar(self, f_str, ax, bx, ay, by, n_puntos):
        log_pasos = [
            f"### Integración Doble: Monte Carlo",
            f"**Datos:** $x \\in [{ax}, {bx}]$, $y \\in [{ay}, {by}]$, Muestras $N = {n_puntos}$"
        ]

        x_sym, y_sym = sp.symbols('x y')
        try:
            # 1. Preparación y Blindaje
            f_limpia = f_str.lower().replace("f(x,y)=", "").replace("z=", "").replace("sen", "sin").replace("^", "**").strip()
            f_expr = sp.sympify(f_limpia, locals={'e': sp.E, 'pi': sp.pi})
            f_lamb = sp.lambdify((x_sym, y_sym), f_expr, 'math')

            # 2. Generamos puntos aleatorios en el piso (Base XY)
            x_raw = np.random.uniform(ax, bx, n_puntos)
            y_raw = np.random.uniform(ay, by, n_puntos)
            
            # 3. Evaluamos la altura (Z) en cada punto
            z_raw = []
            for i in range(n_puntos):
                z_raw.append(float(f_lamb(x_raw[i], y_raw[i])))
            z_raw = np.array(z_raw)

            # 4. Cálculos Estadísticos
            promedio_z = np.mean(z_raw)
            area_base = float((bx - ax) * (by - ay))
            volumen_estimado = area_base * promedio_z

            varianza_f = np.var(z_raw, ddof=1)
            desviacion_f = np.std(z_raw, ddof=1)
            
            # Fórmulas ajustadas a integración doble
            varianza_estimador = ((area_base**2) / n_puntos) * varianza_f
            error_estandar = (area_base * desviacion_f) / np.sqrt(n_puntos)

            # 5. Desarrollo Analítico
            log_pasos.append("---")
            log_pasos.append("**1. Área de la Base (Dominio Integración):**")
            log_pasos.append(f"$$A = (b_x - a_x) \\cdot (b_y - a_y) = ({bx} - {ax}) \\cdot ({by} - {ay}) = {area_base:.4f}$$")

            log_pasos.append("---")
            log_pasos.append("**2. Esperanza del Estimador (Volumen Estimado):**")
            log_pasos.append(f"$$V \\approx A \\cdot \\bar{{z}} = {area_base:.4f} \\cdot {promedio_z:.6f} = {volumen_estimado:.6f}$$")

            log_pasos.append("---")
            log_pasos.append("**3. Análisis de Precisión:**")
            log_pasos.append(f"Varianza de las alturas evaluadas: $Var[f(X,Y)] \\approx {varianza_f:.6f}$")
            log_pasos.append(f"Error Estándar del método: $\\sigma_{{\\hat{{V}}}} = \\frac{{A \\cdot \\sigma_f}}{{\\sqrt{{N}}}} = {error_estandar:.6f}$")

            # 6. Tabla de Iteraciones (Primeros 100 puntos)
            iteraciones = []
            for i in range(min(n_puntos, 100)):
                iteraciones.append({
                    "Muestra": i + 1,
                    "x_i": self.formatear(x_raw[i]),
                    "y_i": self.formatear(y_raw[i]),
                    "Altura z_i": self.formatear(z_raw[i])
                })

            return volumen_estimado, iteraciones, log_pasos, x_raw, y_raw, z_raw, f_lamb, None

        except Exception as e:
            return None, [], [], [], [], [], None, f"Error en el motor 3D: {str(e)}"