from core.common.metodos_base import MetodoRaizBase

from utils.maths import calcular_aceleracion_aitken

class PuntoFijoAitken(MetodoRaizBase):
    
    def ejecutar(self, g, x0):
        log_pasos = [
            "**Análisis Inicial:**",
            f"1. Valor inicial (semilla): $x_0 = {x0}$",
            "2. Comenzamos la iteración aplicando $x_{i+1} = g(x_i)$.",
            "---"
        ]
        
        iteraciones = []
        i = 1
        error = float('inf')
        
        while error >= self.tol and i <= self.max_iter:
            try:
                x1 = float(g(x0))
                x2 = float(g(x1))
                xAst = calcular_aceleracion_aitken(x0, x1, x2)

                error = abs(xAst - x2)
                
                if i <= 5:
                    log_pasos.extend([
                        f"**Iteración {i}:**",
                        f"- Calculamos $g({x0:.4f}) = {x1:.4f}$",
                        f"- Calculamos $g({x1:.4f}) = {x2:.4f}$",
                        f"- Calculamos $g({x2:.4f}) = {xAst:.4f}$",
                        f"- Nuevo valor (acelerado) para la próxima vuelta: $x_{{{i}}} = {xAst:.4f}$",
                        f"- Error: $|{xAst:.4f} - {x2:.4f}| = {error:.4f}$"
                    ])
                
                iteraciones.append({
                    "Iter": i, 
                    "x0": self.formatear(x0), 
                    "x1 = g(x0)": self.formatear(x1), 
                    "x2 = g(x1)": self.formatear(x2),
                    "x*": self.formatear(xAst), 
                    "Error": self.formatear(error)
                })
                
                x0 = xAst
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
            
        return xAst, iteraciones, log_pasos, None
