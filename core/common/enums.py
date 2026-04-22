from enum import Enum

class Categoria(str, Enum):
    RAICES = "Búsqueda de Raíces"
    INTERPOLACION = "Interpolación y Aproximación"
    DERIVACION = "Derivación"
    INTEGRACION = "Integración"
    ECUACIONES = "Ecuaciones"

class MetodoRaices(str, Enum):
    BISECCION = "Bisección"
    PUNTO_FIJO = "Punto Fijo"
    PUNTO_FIJO_AITKEN = "Punto Fijo Acelerado c/ Aitken"
    NEWTON = "Newton-Raphson"
    COMPARATIVA = "Comparativa de Métodos"

class MetodoInterpolacion(str, Enum):
    LAGRANGE = "Interpolación de Lagrange"

class MetodoDerivacion(str, Enum):
    DIFERENCIAS_FINITAS = "Diferencias Finitas"

class MetodoIntegracion(str, Enum):
    NEWTON_COTES = "Newton Cotes"
    MONTECARLO = "Montecarlo"
    MONTECARLO_DOBLE = "Montecarlo (Integrales dobles)"

class MetodoEcuaciones(str, Enum):
    EDO = "Ecuaciones Diferenciales Ordinarias"
    EDO_COMPARATIVA = "Ecuaciones Diferenciales Ordinarias (Comparativa)"