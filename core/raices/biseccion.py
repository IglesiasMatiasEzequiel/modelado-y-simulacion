from core.common.metodos_base import MetodoRaizBase

class Biseccion(MetodoRaizBase):
    
    def calcular_errores(self, a, b):
        error = abs(b - a)
        error_rel = (error / b) * 100 if b != 0 else 0.0
        return error, error_rel

    def ejecutar(self, f, a, b):

        f_a = float(f(a))
        f_b = float(f(b))
        
        log_pasos = [
            "**Análisis Inicial:**",
            "1. Asumiendo que la función es continua en el intervalo.",
            f"2. Evaluando extremos: $f({a}) = {f_a:.4f}$ y $f({b}) = {f_b:.4f}$"
        ]
        
        if f_a == 0:
            log_pasos.append(f"3. ¡Raíz exacta encontrada en el límite inferior ($x = {a}$)! No es necesario iterar.")
            iteraciones = [{"Iter": 0, "a": self.formatear(a), "b": self.formatear(b), "c": self.formatear(a), "f(c)": self.formatear(0), "Error": self.formatear(0), "Error Rel (%)": self.formatear(0)}]
            return a, iteraciones, log_pasos, None
            
        if f_b == 0:
            log_pasos.append(f"3. ¡Raíz exacta encontrada en el límite superior ($x = {b}$)! No es necesario iterar.")
            iteraciones = [{"Iter": 0, "a": self.formatear(a), "b": self.formatear(b), "c": self.formatear(b), "f(c)": self.formatear(0), "Error": self.formatear(0), "Error Rel (%)": self.formatear(0)}]
            return b, iteraciones, log_pasos, None
        
        if f_a * f_b > 0:
            log_pasos.append("❌ Error: f(a) y f(b) deben tener signos opuestos.")
            return None, [], log_pasos, "Error: f(a) y f(b) deben tener signos opuestos."
            
        log_pasos.append("3. ¡Signos opuestos confirmados! (Teorema de Bolzano).")
        log_pasos.append("---")
        
        
        iteraciones = []
        a_actual, b_actual = a, b
        c = a_actual
        i = 1

        error, error_rel = self.calcular_errores(a_actual, b_actual)

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
            elif float(f(a_actual)) * f_c < 0:
                if i <= 5: log_pasos.append(f"- La raíz está a la izquierda de c. Límite superior: b = {c:.4f}")
                b_actual = c
            else:
                if i <= 5: log_pasos.append(f"- La raíz está a la derecha de c. Límite inferior: a = {c:.4f}")
                a_actual = c

            error, error_rel = self.calcular_errores(a_actual, b_actual)

            i += 1
            
        if i > 5:
            log_pasos.append("*(... Se ocultan las siguientes iteraciones por brevedad ...)*")

        log_pasos.append("---")
        
        if raiz_exacta: log_pasos.append("**Parada:** Raíz exacta.")
        elif error < self.tol: log_pasos.append(f"**Parada:** Error absoluto menor a la tolerancia ({self.tol}).")
        else: log_pasos.append(f"**Parada:** Límite máximo de iteraciones ({self.max_iter}).")
            
        return c, iteraciones, log_pasos, None