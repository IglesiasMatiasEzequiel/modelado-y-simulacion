import sympy as sp

class Lagrange:
    
    def ejecutar(self, x_list, y_list):
        log_pasos = [
            "**Planteo del Problema:**",
            f"Tenemos $n = {len(x_list)}$ puntos de datos.",
            "Vamos a construir un polinomio de grado máximo $n-1$ usando la fórmula:",
            "$P(x) = \sum_{i=0}^{n-1} y_i \cdot L_i(x)$",
            "---"
        ]
        
        n = len(x_list)
        x_sym = sp.Symbol('x')
        
        
        P_x = 0 
        
        for i in range(n):
            
            numerador = 1
            denominador = 1
            log_terminos = []
            
            for j in range(n):
                if i != j:
                    numerador *= (x_sym - x_list[j])
                    denominador *= (x_list[i] - x_list[j])
                    
                    if n <= 6:
                        log_terminos.append(f"\\frac{{(x - {x_list[j]:.2f})}}{{{x_list[i]:.2f} - {x_list[j]:.2f}}}")
            
            L_i = numerador / denominador
            
            termino_completo = y_list[i] * L_i
            P_x += termino_completo
            
            if n <= 6:
                str_L = " \\cdot ".join(log_terminos)
                log_pasos.extend([
                    f"**Término para el punto $i={i}$ $(x={x_list[i]:.2f}, y={y_list[i]:.2f})$:**",
                    f"$L_{i}(x) = {str_L}$",
                    f"$T_{i}(x) = {y_list[i]:.2f} \cdot L_{i}(x)$"
                ])
        
        P_simplificado = sp.expand(P_x)
        
        log_pasos.extend([
            "---",
            "**Polinomio Final (sin simplificar):**",
            "La suma de todos los $T_i(x)$ anteriores.",
            "**Polinomio Simplificado (expandido algebraicamente):**",
            f"$P(x) = {sp.latex(P_simplificado)}$"
        ])
        
        f_evaluable = sp.lambdify(x_sym, P_simplificado, 'numpy')
        
        return f_evaluable, str(P_simplificado), log_pasos