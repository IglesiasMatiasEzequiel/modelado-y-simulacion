AYUDA_SINTAXIS_MATEMATICA = """
**Operadores básicos:**
* **Multiplicación:** `*` *(Obligatorio: usar `2*x`, no `2x`)*
* **Potencia:** `**` *(Ejemplo: x² se escribe `x**2`)*
* **División:** `/`

**Raíces:**
* **Raíz cuadrada:** `sqrt(x)`
* **Raíz N-ésima:** `x**(1/3)` *(Ejemplo para raíz cúbica)*

**Funciones especiales:**
* **Exponencial (e^x):** `exp(x)` *(No usar `e**x`)*
* **Logaritmo natural (ln):** `log(x)`
* **Logaritmo base 10:** `log(x, 10)`
* **Trigonometría:** `sin(x)`, `cos(x)`, `tan(x)`

**Constantes:**
* **Pi (π):** `pi`
* **Euler (e):** `E`
"""

INFO_METODOS = {
    "Bisección": """
    ### Método de Bisección
    **El Concepto:**
    Es el método más seguro pero más lento. Imagina que tienes una función que pasa de negativo a positivo (o viceversa); lógicamente, en algún punto tuvo que cruzar el cero. El método corta ese intervalo a la mitad una y otra vez hasta acorralar a la raíz.
    
    **Pasos del Algoritmo:**
    1. Elegir un intervalo $[a, b]$ donde la función cambie de signo ($f(a) \cdot f(b) < 0$).
    2. Calcular el punto medio del intervalo: $c = \\frac{a+b}{2}$.
    3. Evaluar la función en ese punto: $f(c)$. Si da $0$, encontraste la raíz exacta.
    4. Si $f(a)$ y $f(c)$ tienen signos opuestos, la raíz está en la primera mitad. El nuevo límite superior será $b = c$.
    5. Si tienen el mismo signo, la raíz está en la segunda mitad. El nuevo límite inferior será $a = c$.
    
    **Condiciones:** La función debe ser continua. Nunca falla si se elige bien el intervalo inicial (Teorema de Bolzano).
    """,
    
    "Punto Fijo": """
    ### Método del Punto Fijo
    **El Concepto:**
    En lugar de buscar dónde $f(x) = 0$, reescribimos la ecuación original despejando una "$x$" para que quede de la forma $x = g(x)$. El objetivo es encontrar un valor que, al meterlo en $g(x)$, te devuelva exactamente ese mismo valor.
    
    **Pasos del Algoritmo:**
    1. Despejar $x$ de la función original para obtener $g(x)$.
    2. Elegir un valor inicial al azar ($x_0$), preferentemente cerca de donde crees que está la raíz.
    3. Evaluar ese valor en la función: $x_1 = g(x_0)$.
    4. Agarrar el resultado y volver a meterlo en la función: $x_2 = g(x_1)$.
    5. Repetir la iteración $x_{i+1} = g(x_i)$ hasta que el valor nuevo sea casi idéntico al anterior.
    
    **Condiciones (Teorema de Banach):** Para que los números no se disparen al infinito (divergencia), la derivada de tu función despejada debe ser menor a 1 en valor absoluto ($|g'(x)| < 1$) cerca de la raíz.
    """,
    
    "Punto Fijo Acelerado c/ Aitken": """
    ### Aceleración de Aitken ($\Delta^2$)
    **El Concepto:**
    A veces, el Método de Punto Fijo avanza a pasos de tortuga. Aitken es un "atajo" matemático. Al ver cómo se comportan los primeros 3 puntos generados, Aitken adivina hacia dónde se está dirigiendo la secuencia y "salta" directamente hacia ese límite.
    
    **Pasos del Algoritmo:**
    1. Hacer dos iteraciones normales de Punto Fijo: $x_1 = g(x_0)$ y $x_2 = g(x_1)$.
    2. Usar esos tres valores consecutivos ($x_0, x_1, x_2$) en la fórmula de aceleración:
       $$x^* = x_0 - \\frac{(x_1 - x_0)^2}{x_2 - 2x_1 + x_0}$$
    3. Ese nuevo valor $x^*$ está mucho más cerca de la raíz. 
    4. Si el error no es lo suficientemente pequeño, tomar $x^*$ como el nuevo inicio ($x_0$) y volver al paso 1.
    
    **Condiciones:** El denominador de la fórmula no debe ser cero. Solo funciona si la sucesión original de Punto Fijo ya iba a converger eventualmente.
    """,
    
    "Newton-Raphson": """
    ### Método de Newton-Raphson
    **El Concepto:**
    Es el "Fórmula 1" de los métodos numéricos. En lugar de encerrar la raíz, se para en un punto de la curva, dibuja una línea recta tangente, y se fija dónde esa recta choca contra el eje X. Ese choque será el nuevo punto para la siguiente iteración.
    
    **Pasos del Algoritmo:**
    1. Elegir un valor inicial $x_0$.
    2. Calcular la derivada de la función $f'(x)$.
    3. Aplicar la fórmula iterativa que resta el valor actual menos la pendiente:
       $$x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)}$$
    4. Repetir hasta que la diferencia entre $x_{i+1}$ y $x_i$ sea casi nula.
    
    **Condiciones:** Su mayor debilidad es que si la curva se vuelve plana en el punto que estás evaluando (es decir, la derivada $f'(x)$ es igual a $0$), el método explota por división por cero. Además, requiere conocer la derivada analítica previamente.
    """,
    
    "Interpolación de Lagrange": """
    ### Polinomio Interpolante de Lagrange
    **El Concepto:**
    A diferencia de los métodos anteriores que buscan raíces ($y=0$), Lagrange busca construir una fórmula. Si tenés un puñado de puntos dispersos (datos de un experimento, por ejemplo), Lagrange fabrica una única curva polinómica que pasa exactamente por todos y cada uno de esos puntos.
    
    **Pasos del Algoritmo:**
    1. Para cada punto de tus datos, se construye un término $L_i(x)$. Este término está diseñado como un interruptor: vale $1$ en su propia coordenada X, y $0$ en las demás.
       $$L_i(x) = \\prod_{j \\neq i} \\frac{x - x_j}{x_i - x_j}$$
    2. Se multiplica cada "interruptor" $L_i(x)$ por la altura real del punto ($y_i$).
    3. Se suman todos los términos generados.
       $$P(x) = \\sum_{i=0}^{n-1} y_i \cdot L_i(x)$$
    
    **Condiciones:** Genera un único polinomio de grado $n-1$ (donde $n$ es la cantidad de puntos). Si hay muchos puntos, el polinomio resultante oscila de forma violenta en los bordes (Fenómeno de Runge).
    """,

   "Comparativa de Métodos": """
    ### Análisis Comparativo Multimétodo
    **El Concepto:**
    Esta herramienta ejecuta simultáneamente los 4 métodos de búsqueda de raíces vistos en la cátedra bajo las mismas condiciones iniciales. 
    
    **¿Para qué sirve?**
    Permite visualizar empíricamente los órdenes de convergencia:
    * **Bisección:** Lenta (lineal) pero segura.
    * **Punto Fijo:** Depende fuertemente de la función $g(x)$ elegida.
    * **Aitken:** Acelera la convergencia lineal del Punto Fijo.
    * **Newton-Raphson:** Extremadamente rápida (cuadrática), pero riesgosa si la derivada se acerca a cero.
    """,

   "Diferencias Finitas": """
    ### Derivación Numérica (Diferencias Finitas)
    La **Derivación Numérica** permite estimar las derivadas de una función usando un conjunto de puntos discretos separados por un paso temporal o espacial constante ($h$). En cinemática, es la herramienta clave para pasar de Posición a Velocidad (1ra derivada) y a Aceleración (2da derivada).

    **1. Primera Derivada (Ej: Velocidad)**
    Mide la pendiente o tasa de cambio entre dos puntos.
    * **Progresiva (Adelante):** $f'(x_i) \\approx \\frac{f(x_{i+1}) - f(x_i)}{h}$
    * **Regresiva (Atrás):** $f'(x_i) \\approx \\frac{f(x_i) - f(x_{i-1})}{h}$
    * **Central (La más exacta):** $f'(x_i) \\approx \\frac{f(x_{i+1}) - f(x_{i-1})}{2h}$

    **2. Segunda Derivada (Ej: Aceleración)**
    Mide la concavidad o cómo cambia la tasa de cambio ("diferencia de diferencias").
    * **Progresiva (Adelante):** Usa el punto actual y los dos siguientes. Es obligatoria para el *primer* dato de una tabla.
      $$f''(x_i) \\approx \\frac{f(x_{i+2}) - 2f(x_{i+1}) + f(x_i)}{h^2}$$
    * **Regresiva (Atrás):** Usa el punto actual y los dos anteriores. Es obligatoria para el *último* dato de una tabla.
      $$f''(x_i) \\approx \\frac{f(x_i) - 2f(x_{i-1}) + f(x_{i-2})}{h^2}$$
    * **Central:** Usa un punto hacia adelante y uno hacia atrás. Es la más precisa (error de orden cuadrático) y se debe usar en todos los puntos *interiores* de la tabla.
      $$f''(x_i) \\approx \\frac{f(x_{i+1}) - 2f(x_i) + f(x_{i-1})}{h^2}$$

    > **💡 Regla:** Usa siempre las fórmulas **Centrales** cuando tengas datos a ambos lados. Reserva las progresivas y regresivas estrictamente para chocar contra las paredes (los extremos) de tu conjunto de datos.
    """,

   "Newton Cotes": """
   La **Integración Numérica** nos permite calcular el área bajo una curva definida por una integral $\\int_{a}^{b} f(x) dx$ cuando la función es muy difícil (o imposible) de integrar analíticamente.

   La familia de métodos de **Newton-Cotes** se basa en una idea geométrica simple: dividir el intervalo $[a, b]$ en $n$ partes iguales de ancho $h$ y reemplazar la curva original por polinomios más fáciles de integrar (líneas rectas, parábolas o cúbicas).

   ### 1. El ancho del subintervalo ($h$)
   Todas las reglas utilizan un paso constante que se calcula así:
   $$h = \\frac{b - a}{n}$$
   Donde $n$ es la cantidad de "pedacitos" en los que cortamos el área.

   ### 2. Regla del Trapecio
   * **Geometría:** Une los nodos usando líneas rectas (polinomios de grado 1).
   * **Restricción:** Ninguna. Funciona con cualquier valor de $n$.
   * **Precisión:** Es el método menos exacto. Su error global es de orden $O(h^2)$.
   $$\\text{Área} \\approx \\frac{h}{2} \\left[ f(x_0) + 2 \\sum_{i=1}^{n-1} f(x_i) + f(x_n) \\right]$$

   ### 3. Regla de Simpson 1/3
   * **Geometría:** Une los puntos de a tres, trazando una parábola suave (polinomio de grado 2).
   * **Restricción:** Obliga a que $n$ sea un **número par**.
   * **Precisión:** Es excelente para la mayoría de los casos. Su error global decae drásticamente, siendo de orden $O(h^4)$.
   $$\\text{Área} \\approx \\frac{h}{3} \\left[ f(x_0) + 4 \\sum f(x_{\\text{impares}}) + 2 \\sum f(x_{\\text{pares}}) + f(x_n) \\right]$$

   ### 4. Regla de Simpson 3/8
   * **Geometría:** Une los puntos de a cuatro, usando una curva cúbica (polinomio de grado 3). Se adapta mejor a curvas con cambios muy bruscos.
   * **Restricción:** Obliga a que $n$ sea **múltiplo de 3**.
   * **Precisión:** Tiene el mismo orden de error que Simpson 1/3 ($O(h^4)$), pero su coeficiente de error teórico es ligeramente menor.
   $$\\text{Área} \\approx \\frac{3h}{8} \\left[ f(x_0) + 3 \\sum f(x_{\\text{resto}}) + 2 \\sum f(x_{\\text{múltiplos de 3}}) + f(x_n) \\right]$$

   > **💡 El Secreto del Error:** A medida que aumentamos los subintervalos ($n$), el ancho $h$ se achica y el *Error de Truncamiento* disminuye. Sin embargo, para un mismo valor de $n$, las reglas de Simpson siempre darán una aproximación mucho mejor que la del Trapecio porque copian la curvatura real de la función.
   """
}
