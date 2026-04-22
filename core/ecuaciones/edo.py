import sympy as sp
import numpy as np

class EcuacionesDiferenciales:
    def formatear(self, valor):
        return round(float(valor), 6)

    def ejecutar(self, f_str, x0, y0, xf, n, metodo="Euler"):
        x_sym, y_sym = sp.symbols('x y')
        log_pasos = [f"### Resolución EDO: {metodo}"]
        try:
            f_limpia = f_str.lower().replace("y'=", "").replace("dy/dx=", "").replace("sen", "sin").strip()
            f_expr = sp.sympify(f_limpia, locals={'e': sp.E, 'pi': sp.pi})
            f_lamb = sp.lambdify((x_sym, y_sym), f_expr, 'math')

            x0, y0, xf = float(x0), float(y0), float(xf)
            n = int(n)
            h = (xf - x0) / n

            x_vals = [x0]
            y_vals = [y0]
            
            iteraciones = [{"i": 0, "x_i": self.formatear(x0), "y_i": self.formatear(y0)}]
            log_pasos.append(f"**Paso ($h$):** $h = {h:.6f}$")

            for i in range(n):
                xi, yi = x_vals[-1], y_vals[-1]
                xi_sig = x0 + (i + 1) * h 

                if metodo == "Euler":
                    y_sig = yi + h * f_lamb(xi, yi)
                elif metodo == "Heun":
                    k1 = f_lamb(xi, yi)
                    y_pred = yi + h * k1
                    k2 = f_lamb(xi_sig, y_pred)
                    y_sig = yi + (h/2) * (k1 + k2)
                elif metodo == "Runge-Kutta 4":
                    k1 = f_lamb(xi, yi)
                    k2 = f_lamb(xi + h/2, yi + k1 * h/2)
                    k3 = f_lamb(xi + h/2, yi + k2 * h/2)
                    k4 = f_lamb(xi_sig, yi + k3 * h)
                    y_sig = yi + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
                
                x_vals.append(xi_sig)
                y_vals.append(float(y_sig))
                
                iteraciones.append({"i": i + 1, "x_i": self.formatear(xi_sig), "y_i": self.formatear(y_sig)})

            return iteraciones, log_pasos, x_vals, y_vals, None
            
        except Exception as e:
            return [], [], [], [], f"Error en {metodo}: {str(e)}"

    def ejecutar_comparativa(self, f_str, x0, y0, xf, n):
        metodos = ["Euler", "Heun", "Runge-Kutta 4"]
        resultados = {}
        for m in metodos:
            it, log, x_raw, y_raw, err = self.ejecutar(f_str, x0, y0, xf, n, metodo=m)
            if err: return None, err
            
            resultados[m] = {"x": x_raw, "y": y_raw, "iteraciones": it, "log_pasos": log}
            
        return resultados, None