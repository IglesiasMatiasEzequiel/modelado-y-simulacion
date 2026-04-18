from core.common.metodos_base import MetodoNumericoBase

class Biseccion(MetodoNumericoBase):
    
    def ejecutar(self, f, a, b):
        log_pasos = [
            "**Análisis Inicial:**",
            "1. Asumiendo que la función es continua en el intervalo.",
            f"2. Evaluando extremos: $f({a}) = {f(a):.4f}$ y $f({b}) = {f(b):.4f}$"
        ]
        
        if f(a) * f(b) > 0:
            log_pasos.append("❌ Error: f(a) y f(b) deben tener signos opuestos.")
            return None, [], log_pasos, "Error: f(a) y f(b) deben tener signos opuestos."
            
        log_pasos.append("3. ¡Signos opuestos confirmados! (Teorema de Bolzano).")
        log_pasos.append("---")
        
        iteraciones = []
        a_actual, b_actual = a, b
        i = 1
        error = abs(b_actual - a_actual)
        error_rel = (error / b_actual) * 100
        c = a_actual
        raiz_exacta = False
        
        while error >= self.tol and i <= self.max_iter:
            c = (a_actual + b_actual) / 2
            f_c = float(f(c))
            
            if i <= 5:
                log_pasos.extend([
                    f"**Iteración {i}:**",
                    f"- Punto medio: c = {c:.4f}",
                    f"- Evaluamos f(c) = {f_c:.4f}"
                ])
            
            iteraciones.append({
                "Iter": i, 
                "a": self.formatear(a_actual), 
                "b": self.formatear(b_actual), 
                "c": self.formatear(c), 
                "f(c)": self.formatear(f_c), 
                "Error": self.formatear(error),
                "Error Rel (%)": self.formatear(error_rel),
            })
            
            if f_c == 0:
                if i <= 5: log_pasos.append("- ¡Raíz exacta encontrada!")
                raiz_exacta = True
                break
            elif f(a_actual) * f_c < 0:
                if i <= 5: log_pasos.append(f"- La raíz está a la izquierda de c. Límite superior: b = {c:.4f}")
                b_actual = c
            else:
                if i <= 5: log_pasos.append(f"- La raíz está a la derecha de c. Límite inferior: a = {c:.4f}")
                a_actual = c
                
            error = abs(b_actual - a_actual)
            error_rel = (error / b_actual) * 100
            i += 1
            
        if i > 5:
            log_pasos.append("*(... Se ocultan las siguientes iteraciones por brevedad ...)*")

        log_pasos.append("---")
        
        if raiz_exacta: log_pasos.append("**Parada:** Raíz exacta.")
        elif error < self.tol: log_pasos.append(f"**Parada:** Error absoluto menor a la tolerancia ({self.tol}).")
        else: log_pasos.append(f"**Parada:** Límite máximo de iteraciones ({self.max_iter}).")
            
        return c, iteraciones, log_pasos, None