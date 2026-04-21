from core.common.metodos_base import MetodoRaizBase

class PuntoFijo(MetodoRaizBase):
    
    def ejecutar(self, g, x0):
        log_pasos = [
            "**Análisis Inicial:**",
            f"1. Valor inicial (semilla): $x_0 = {x0}$",
            "2. Comenzamos la iteración aplicando $x_{i+1} = g(x_i)$.",
            "---"
        ]
        
        iteraciones = []
        x_actual = x0
        i = 1
        error = float('inf')
        
        while error >= self.tol and i <= self.max_iter:
            try:
                x_nuevo = float(g(x_actual))
                
                error = abs(x_nuevo - x_actual)
                
                if i <= 5:
                    log_pasos.extend([
                        f"**Iteración {i}:**",
                        f"- Calculamos $g({x_actual:.4f}) = {x_nuevo:.4f}$",
                        f"- Nuevo valor para la próxima vuelta: $x_{{{i}}} = {x_nuevo:.4f}$",
                        f"- Error: $|{x_nuevo:.4f} - {x_actual:.4f}| = {error:.4f}$"
                    ])
                
                iteraciones.append({
                    "Iter": i, 
                    "x_i": self.formatear(x_actual), 
                    "g(x_i)": self.formatear(x_nuevo), 
                    "Error": self.formatear(error)
                })
                
                x_actual = x_nuevo
                i += 1
                
            except OverflowError:
                log_pasos.append("❌ **Error crítico:** Los valores tienden al infinito (Divergencia matemática).")
                return None, iteraciones, log_pasos, "La función diverge rápidamente. Intentá despejar g(x) de otra forma o elegí un x0 más cercano a la raíz."
            
        if i > 5:
            log_pasos.append("*(... Se ocultan las siguientes iteraciones ...)*")
        log_pasos.append("---")
        
        if error < self.tol:
            log_pasos.append(f"**Parada:** Convergencia lograda. Error absoluto menor a la tolerancia ({self.tol}).")
        else:
            log_pasos.append(f"**Parada:** Límite máximo de iteraciones alcanzado ({self.max_iter}). Posible divergencia lenta.")
            
        return x_actual, iteraciones, log_pasos, None