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
    
    **Condiciones (Teorema de Bolzano):** Para que este método garantice encontrar una raíz, la función $f(x)$ **debe ser continua** en el intervalo cerrado $[a, b]$ y debe existir un cambio de signo tal que $f(a) \cdot f(b) < 0$. El Teorema de Bolzano es la base matemática que asegura que, bajo estas dos condiciones, la curva cortará el eje X al menos una vez.
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
    
    **Condiciones (Teorema de Banach y Condición de Lipschitz):** Para garantizar que la sucesión no diverja hacia el infinito, la función $g(x)$ debe ser una "función contractiva". Esto se demuestra mediante la **Condición de Lipschitz**: debe existir una constante $L < 1$ tal que la distancia entre dos puntos evaluados siempre se achique. En la práctica (si $g$ es derivable), esto exige que el valor absoluto de su derivada sea estrictamente menor a 1 ($|g'(x)| < 1$) en un entorno de la raíz.
    """,
    
    "Punto Fijo Acelerado c/ Aitken": """
    ### Aceleración de Aitken ($\Delta^2$)
    **El Concepto:**
    A veces, el Método de Punto Fijo avanza a pasos de tortuga (convergencia lineal). Aitken es un "atajo" matemático. Al ver cómo se comportan los primeros 3 puntos generados, Aitken analiza la tasa de error, adivina hacia dónde se está dirigiendo la secuencia y "salta" directamente hacia ese límite, logrando una convergencia casi cuadrática.
    
    **Pasos del Algoritmo:**
    1. Hacer dos iteraciones normales de Punto Fijo: $x_1 = g(x_0)$ y $x_2 = g(x_1)$.
    2. Usar esos tres valores consecutivos ($x_0, x_1, x_2$) en la fórmula de aceleración:
       $$x^* = x_0 - \\frac{(x_1 - x_0)^2}{x_2 - 2x_1 + x_0}$$
    3. Ese nuevo valor $x^*$ está mucho más cerca de la raíz. 
    4. Si el error no es lo suficientemente pequeño, tomar $x^*$ como el nuevo inicio ($x_0$) y volver al paso 1.
    
    **Condiciones:** El denominador de la fórmula no debe ser cero. Además, este método no hace milagros: solo funciona si la sucesión original de Punto Fijo ya iba a converger eventualmente (es decir, si $g(x)$ ya cumplía la condición de Lipschitz).
    """,
    
    "Newton-Raphson": """
    ### Método de Newton-Raphson
    **El Concepto:**
    Es el "Fórmula 1" de los métodos numéricos. En lugar de encerrar la raíz, se para en un punto de la curva, dibuja una línea recta tangente (basada en la derivada), y se fija dónde esa recta choca contra el eje X. Ese choque será el nuevo punto para la siguiente iteración.
    
    **Pasos del Algoritmo:**
    1. Elegir un valor inicial $x_0$.
    2. Calcular la derivada de la función $f'(x)$.
    3. Aplicar la fórmula iterativa que resta el valor actual menos la pendiente:
       $$x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)}$$
    4. Repetir hasta que la diferencia entre $x_{i+1}$ y $x_i$ sea casi nula.
    
    **Condiciones (Convergencia Local y Condición de Fourier):** Su falla fatal es la división por cero: si la curva se vuelve plana en el punto evaluado ($f'(x_i) = 0$), el método explota. A diferencia de Bisección, Newton no siempre converge. Para asegurar teóricamente que el método llegará a la raíz desde el punto $x_0$ elegido, se suele verificar la **Condición de Fourier**: $f(x) \cdot f''(x) > 0$ en el intervalo de búsqueda. Si converge, lo hace a velocidad cuadrática (duplica los decimales correctos en cada paso).
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
    Permite visualizar empíricamente el rendimiento de cada algoritmo, analizando su **Orden de Convergencia ($p$)** y su **Costo Computacional** (la cantidad de operaciones matemáticas por cada ciclo de ejecución):
    
    * **Bisección:** * **Orden de Ejecución:** Convergencia Lineal ($p=1$). 
      * **Costo:** 1 evaluación de función ($f(x)$) por iteración. Es el más lento computacionalmente, pero el único que garantiza el resultado.
    
    * **Punto Fijo:** * **Orden de Ejecución:** Convergencia Lineal ($p=1$). 
      * **Costo:** 1 evaluación de función ($g(x)$) por iteración. Su éxito depende exclusivamente de que la $g(x)$ elegida cumpla la condición de Lipschitz.
    
    * **Aitken ($\Delta^2$):** * **Orden de Ejecución:** Convergencia Superlineal (casi cuadrática). 
      * **Costo:** Muy eficiente. Acelera la convergencia lineal reciclando 3 iteraciones previas de Punto Fijo sin obligar a la computadora a calcular derivadas complejas.
    
    * **Newton-Raphson:** * **Orden de Ejecución:** Convergencia Cuadrática ($p=2$). Duplica la cantidad de cifras decimales correctas en cada paso.
      * **Costo:** 2 evaluaciones por iteración (la función $f(x)$ y su derivada $f'(x)$). Aunque cada paso es "computacionalmente más caro", requiere una cantidad de ciclos drásticamente menor para encontrar la raíz exacta.
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

   La familia de métodos de **Newton-Cotes** divide el intervalo $[a, b]$ en $n$ partes iguales de ancho $h$ y reemplaza la curva original por polinomios.

   ### 1. El ancho del subintervalo ($h$)
   $$h = \\frac{b - a}{n}$$

   ---

   ### 2. Regla del Trapecio
   * **Geometría:** Une los nodos usando líneas rectas (polinomio grado 1).
   * **Restricción:** Funciona con cualquier valor de $n$.
   * **Fórmula de Aproximación:**
   $$\\text{Área} \\approx \\frac{h}{2} \\left[ f(x_0) + 2 \\sum_{i=1}^{n-1} f(x_i) + f(x_n) \\right]$$
   * **Error de Truncamiento Global:**
   $$E_T = -\\frac{b-a}{12} h^2 f''(\\mu)$$

   ---

   ### 3. Regla de Simpson 1/3
   * **Geometría:** Une los puntos de a tres, trazando una parábola suave (polinomio grado 2).
   * **Restricción:** $n$ debe ser un **número par**.
   * **Fórmula de Aproximación:**
   $$\\text{Área} \\approx \\frac{h}{3} \\left[ f(x_0) + 4 \\sum f(x_{\\text{impares}}) + 2 \\sum f(x_{\\text{pares}}) + f(x_n) \\right]$$
   * **Error de Truncamiento Global:**
   $$E_{S1/3} = -\\frac{b-a}{180} h^4 f^{(4)}(\\mu)$$

   ---

   ### 4. Regla de Simpson 3/8
   * **Geometría:** Une los puntos de a cuatro, usando una curva cúbica (polinomio grado 3).
   * **Restricción:** $n$ debe ser **múltiplo de 3**.
   * **Fórmula de Aproximación:**
   $$\\text{Área} \\approx \\frac{3h}{8} \\left[ f(x_0) + 3 \\sum f(x_{\\text{resto}}) + 2 \\sum f(x_{\\text{múltiplos de 3}}) + f(x_n) \\right]$$
   * **Error de Truncamiento Global:**
   $$E_{S3/8} = -\\frac{b-a}{80} h^4 f^{(4)}(\\mu)$$

   ---

   > **💡 Secretos del Error:** > * $\\mu$ representa un valor desconocido que pertenece al intervalo $[a, b]$.
   > * $f''$ y $f^{(4)}$ representan la segunda y la cuarta derivada de la función original, respectivamente.
   > * **El Truco de Simpson:** Como el error de Simpson depende de la derivada cuarta ($f^{(4)}$), si intentás integrar un polinomio de grado 3 (ej: $x^3+x^2$), su cuarta derivada es **cero**. Esto hace que el error se anule por completo, logrando que Simpson calcule integrales cúbicas con **precisión exacta**, ¡a pesar de usar solo parábolas!
   """,

   "Montecarlo": """
   La **Integración por Monte Carlo** es un método numérico probabilístico. A diferencia de Newton-Cotes, que divide el área en figuras geométricas predecibles, Monte Carlo utiliza números pseudoaleatorios para estimar el resultado.

   ### El Método del Valor Medio
   El Teorema del Valor Medio para integrales nos dice que existe un rectángulo cuya área es exactamente igual al área bajo la curva. Monte Carlo busca aproximar la altura de ese rectángulo promediando la altura de la función en puntos aleatorios.

   La fórmula principal es:
   $$I \\approx (b - a) \\cdot \\frac{1}{N} \\sum_{i=1}^{N} f(x_i)$$

   Donde:
   * $(b - a)$ es el ancho de la base del intervalo.
   * $N$ es la cantidad de puntos (muestras) generados al azar.
   * $\\frac{1}{N} \\sum f(x_i)$ es el promedio de las alturas evaluadas (la altura del rectángulo).

   ### ⚠️ El Secreto del Error
   En los métodos determinísticos (como Simpson), el error disminuye drásticamente al aumentar los puntos ($O(h^4)$). En Monte Carlo, el error disminuye a una tasa de **$\\frac{1}{\\sqrt{N}}$**. 
   Esto significa que para reducir el error a la mitad, ¡necesitás multiplicar por 4 la cantidad de puntos! Por eso, Monte Carlo no es eficiente para integrales simples de 1 dimensión, pero se vuelve invencible en integrales múltiples (de 3, 4 o más dimensiones) donde Simpson colapsa.
   """,

   "Ecuaciones Diferenciales Ordinarias": """
   La resolución numérica de **Ecuaciones Diferenciales Ordinarias (EDO)** busca aproximar la curva de una función $y(x)$ sabiendo únicamente su punto de partida (Condición Inicial $y_0$) y una fórmula para calcular su pendiente en cualquier parte ($y' = f(x, y)$).

   ### 1. Método de Euler (El pionero)
   Avanza trazando líneas rectas puras usando la pendiente al inicio de cada intervalo.
   * **Fórmula:** $y_{i+1} = y_i + h \\cdot f(x_i, y_i)$
   * **Precisión:** Baja. Su error global es de orden lineal $O(h)$.

   ### 2. Método de Heun (Euler Mejorado)
   Calcula una pendiente al inicio, estima dónde terminaría (Predictor), calcula la pendiente en ese futuro, y promedia ambas pendientes para dar el paso final (Corrector).
   * **Predictor:** $y_{i+1}^0 = y_i + h \\cdot f(x_i, y_i)$
   * **Corrector:** $y_{i+1} = y_i + \\frac{h}{2} [f(x_i, y_i) + f(x_{i+1}, y_{i+1}^0)]$
   * **Precisión:** Media. Su error global es de orden cuadrático $O(h^2)$.

   ### 3. Runge-Kutta de 4to Orden (RK4)
   Es el estándar absoluto de la industria. Calcula y promedia 4 pendientes distintas dentro del mismo intervalo $h$, dándole el doble de peso a las pendientes centrales.
   1. $k_1 = f(x_i, y_i)$
   2. $k_2 = f(x_i + \\frac{h}{2}, y_i + k_1 \\frac{h}{2})$
   3. $k_3 = f(x_i + \\frac{h}{2}, y_i + k_2 \\frac{h}{2})$
   4. $k_4 = f(x_i + h, y_i + k_3 h)$
   * **Fórmula:** $y_{i+1} = y_i + \\frac{h}{6} (k_1 + 2k_2 + 2k_3 + k_4)$
   * **Precisión:** Excelente. Su error global es de orden $O(h^4)$.
   """
}
