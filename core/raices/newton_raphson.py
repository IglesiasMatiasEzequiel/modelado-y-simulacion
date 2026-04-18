from core.common.metodos_base import MetodoNumericoBase

class NewtonRaphson(MetodoNumericoBase):
    
    def ejecutar(self, f, f_prima, x0, derivada_str):
        log_pasos = [
            "**Análisis Inicial:**",
            f"1. Valor inicial (semilla): $x_0 = {x0}$",
            f"2. Función derivada obtenida: $f'(x) = {derivada_str}$",
            "3. Aplicaremos la fórmula iterativa: $x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)}$",
            "---"
        ]
        
        iteraciones = []
        x_actual = x0
        i = 1
        error = float('inf')
        raiz_exacta = False
        
        while error >= self.tol and i <= self.max_iter:
            try:
                f_x = float(f(x_actual))
                f_p_x = float(f_prima(x_actual))
                
                if f_p_x == 0:
                    log_pasos.append(f"❌ **Error:** La derivada es cero en $x = {x_actual:.4f}$. División por cero inminente.")
                    return None, iteraciones, log_pasos, f"Falla del método: La derivada en x={x_actual:.4f} es cero (tangente horizontal). Elegí un x0 distinto."
                
                x_nuevo = x_actual - (f_x / f_p_x)
                
                error = abs(x_nuevo - x_actual)
                
                if i <= 5:
                    log_pasos.extend([
                        f"**Iteración {i}:**",
                        f"- Evaluamos $f({x_actual:.4f}) = {f_x:.4f}$",
                        f"- Evaluamos $f'({x_actual:.4f}) = {f_p_x:.4f}$",
                        f"- Calculamos $x_{{{i}}} = {x_actual:.4f} - \\frac{{{f_x:.4f}}}{{{f_p_x:.4f}}} = {x_nuevo:.4f}$",
                        f"- Error: $|{x_nuevo:.4f} - {x_actual:.4f}| = {error:.4f}$"
                    ])
                
                iteraciones.append({
                    "Iter": i, 
                    "x_i": self.formatear(x_actual), 
                    "f(x_i)": self.formatear(f_x), 
                    "f'(x_i)": self.formatear(f_p_x), 
                    "x_i+1": self.formatear(x_nuevo), 
                    "Error": self.formatear(error)
                })
                
                if f_x == 0:
                    if i <= 5: log_pasos.append("- ¡Raíz exacta encontrada (f(x) = 0)!")
                    raiz_exacta = True
                    x_actual = x_nuevo
                    break
                    
                x_actual = x_nuevo
                i += 1
                
            except OverflowError:
                log_pasos.append("❌ **Error crítico:** Los valores tienden al infinito (Divergencia matemática).")
                return None, iteraciones, log_pasos, "La función diverge rápidamente. Probá con un x0 más cercano a la raíz."
        
        if i > 5:
            log_pasos.append("*(... Se ocultan las siguientes iteraciones ...)*")
        log_pasos.append("---")
        
        if raiz_exacta:
            log_pasos.append("**Parada:** Raíz exacta.")
        elif error < self.tol:
            log_pasos.append(f"**Parada:** Convergencia lograda. Error absoluto menor a la tolerancia ({self.tol}).")
        else:
            log_pasos.append(f"**Parada:** Límite máximo de iteraciones alcanzado ({self.max_iter}).")
            
        return x_actual, iteraciones, log_pasos, None