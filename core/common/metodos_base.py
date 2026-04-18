from abc import ABC, abstractmethod
import math

class MetodoNumericoBase(ABC):
    def __init__(self, tol, max_iter):
        self.tol = tol
        self.max_iter = max_iter
        decimales = abs(int(math.log10(tol))) if tol > 0 else 4
        self.fmt = f"{{:.{decimales}f}}"

    def formatear(self, valor):
        return self.fmt.format(valor)

    @abstractmethod
    def ejecutar(self, f, *args, **kwargs):
        pass