from abc import ABC, abstractmethod
import math

class MetodoRaizBase(ABC):
    def __init__(self, tol=0.001, max_iter=50):
        self.tol = tol
        self.max_iter = max_iter
        
        decimales = abs(int(math.log10(self.tol))) if self.tol > 0 else 4
        self.fmt = f"{{:.{decimales}f}}"

    def formatear(self, valor):
        if valor is None or isinstance(valor, str):
            return valor
        try:
            return self.fmt.format(float(valor))
        except (ValueError, TypeError):
            return str(valor)

    @abstractmethod
    def ejecutar(self, *args, **kwargs):
        """
        Firma abstracta. Los métodos hijos (Bisección, Newton, etc.)
        deben implementar su propia lógica.
        
        IMPORTANTE: Deben retornar estrictamente esta tupla de 4 elementos:
        - raiz (float | None): Valor numérico de la raíz.
        - iteraciones (list[dict]): Tabla de pasos.
        - log_pasos (list[str]): Registro de la teoría y fórmulas.
        - error_msg (str | None): Mensaje en caso de falla.
        """
        pass

class MetodoInterpolacionBase(ABC):
    def __init__(self):
        pass

    def formatear(self, valor, decimales=4):
        if valor is None or isinstance(valor, str):
            return valor
        try:
            return f"{float(valor):.{decimales}f}"
        except (ValueError, TypeError):
            return str(valor)

    @abstractmethod
    def ejecutar(self, puntos_x, puntos_y):
        """
        Construye un polinomio interpolante a partir de un conjunto de puntos.
        
        Parámetros:
        puntos_x (list[float]): Coordenadas X de los nodos.
        puntos_y (list[float]): Coordenadas Y de los nodos.
        
        Retorna estrictamente esta tupla de 4 elementos:
        - funcion_P (callable | None): El polinomio resultante evaluable en Python.
        - iteraciones (list[dict]): Tabla con los nodos y sus polinomios base L_i.
        - log_pasos (list[str]): Desarrollo analítico en LaTeX.
        - error_msg (str | None): Mensaje de error si falla (ej: puntos X duplicados).
        """
        pass

class MetodoDerivacionBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ejecutar(self, f, x, h):
        """
        Calcula la derivada numérica de una función en un punto.
        
        Parámetros:
        f : función matemática a evaluar.
        x : punto específico donde se quiere conocer la pendiente.
        h : tamaño del incremento (paso).
        
        Retorna:
        - valor_derivada (float): El resultado numérico final.
        - iteraciones (list[dict]): Tabla con f(x), f(x+h), etc.
        - log_pasos (list[str]): Desarrollo teórico y fórmulas en LaTeX.
        - error_msg (str | None): Mensaje de error si falla.
        """
        pass

    def formatear(self, valor, decimales=6):
        return round(valor, decimales)
    
class MetodoIntegracionBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def ejecutar(self, f, a, b, n):
        """
        Calcula el área bajo la curva (integral definida).
        
        Parámetros:
        f : función a integrar.
        a : límite inferior del intervalo.
        b : límite superior del intervalo.
        n : cantidad de subintervalos o particiones (suele ser par para Simpson).
        
        Retorna:
        - area_total (float): El área calculada.
        - iteraciones (list[dict]): Tabla con los nodos (x_i) y sus imágenes f(x_i).
        - log_pasos (list[str]): Desarrollo teórico (fórmula de Simpson, Trapecio, etc.).
        - error_msg (str | None): Mensaje de error si falla (ej: n impar en Simpson 1/3).
        """
        pass

    def formatear(self, valor, decimales=6):
        return round(valor, decimales)
    
class MetodoEDOBase(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def ejecutar(self, f, t0, y0, h, n_pasos):
        """
        Resuelve un Problema de Valor Inicial (PVI) paso a paso.
        
        Parámetros:
        f : función f(t, y) que representa la derivada dy/dt.
        t0: tiempo inicial.
        y0: estado inicial en t0.
        h : tamaño del paso temporal.
        n_pasos : cantidad de iteraciones/pasos hacia el futuro.
        
        Retorna:
        - t_vals (list[float]): Arreglo con todos los tiempos simulados (Eje X).
        - y_vals (list[float]): Arreglo con los estados calculados (Eje Y).
        - iteraciones (list[dict]): Tabla paso a paso (t_i, y_i, k1, k2, etc.).
        - log_pasos (list[str]): Fórmulas de Euler o RK4 aplicadas.
        - error_msg (str | None): Mensaje de error si la función diverge al infinito.
        """
        pass

    def formatear(self, valor, decimales=6):
        return round(valor, decimales)