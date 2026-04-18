from enum import Enum

class Categoria(str, Enum):
    RAICES = "Búsqueda de Raíces"
    INTERPOLACION = "Interpolación y Aproximación"

class MetodoRaices(str, Enum):
    BISECCION = "Bisección"
    PUNTO_FIJO = "Punto Fijo"
    PUNTO_FIJO_AITKEN = "Punto Fijo Acelerado c/ Aitken"
    NEWTON = "Newton-Raphson"

class MetodoInterpolacion(str, Enum):
    LAGRANGE = "Interpolación de Lagrange"