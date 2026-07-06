## Lenguaje Dino
El siguiente Readme oficia de informe sobre el lenguaje DINO creado para la materia Parseo y generación de código.

Previo a su ejecución -> Instalar ply en la terminal : pip install ply

Ejecutar test.py recorrera todos los archivos .dino en la carpeta Niveles, retornando por consola los errores que tenga en cada etapa (Scanner,Parser o analizador semantico)

El main también retorna los errores en caso de ejecutarse sobre un archivo.dino no válido. Si se ejecuta un archivo.dino 100% jugable, se podrá observar el movimiento del dinosaurio por consola.

## Conclusión


El presente trabajo abarca la creación de un lenguaje de programación, implementando un scanner, parser, y analizador semantico utilizando la biblioteca PLY para python.

En un comienzo, se comenzó a trabajar sobre el scanner como un AFD, permitiendo cambiar de estados a medida que lee los caracteres que forman los distintos elementos permitidos, para asi retornar su token.

Al agregar la implementación con PLY, el desarrollo del scanner se redujo de un código de más de 140 lineas, a tan solo 65. PLY utiliza una lógica de caja negra en donde simplemente al definir los tokens que podría tener, se encarga de realizar las lecturas de las cadenas de texto replicando este AFD internamente. Mucho más sencillo para el desarrollador.

El parser se comenzó a trabajar también de manera independiente, sin utilizar PLY. Si bien en cantidad de lineas de código es similar, la versión con PLY es mucho más fácil de comprender ya que no necesita implementar manualmente el recorrido de la gramática sino que a partir de una gramatica en BNF, el parser genera automaticamente el análisis sintáctico y la construcción del AST de manera recursiva.

El trabajo representó un gran desafío y terminó de comprenderse al completo luego de realizar la totalidad de clases teóricas de la materia, al comienzo había muchas dudas que, gracias al uso de herramientas de asistencia basadas en inteligencia artificial y los apuntes en el repositorio de la materia, pudieron solucionarse parcialmente. Aunque fue la comprensión teórica de cada etapa, una vez completadas las clases, la que permitió comprender los errores existentes, y la verdadera ventaja de utilizar PLY como herramienta de desarrollo.

Haciendo referencia a la teoría de la materia, PLY aplica LALR(1). Es un parser ascendente basado en desplazamiento y reducción. Lee un token adelantado y decide si aplicar shift o reduce. Al hacer shift Lee el token de entrada y lo pone en la pila de análisis, y aplica el reduce cuando el elemento en el tope de la pila coincide con el lado derecho de una producción.

Cuando coincide el elemento de la pila con el lado derecho de una producción, reduce los símbolos a un no terminal y ejecuta la acción asociada, que construirá parte del AST.

Al ejecutarse sobre toda la entrada, construye el árbol sintáctico de manera progresiva.

## Explicación de archivos que conforman el trabajo

Scanner:
    Define el vocabulario estableciendo las palabras y simbolos que existen mediante expresiones regulares.
    El scanner tiene que evaluar si la secuencia de caracteres ( lexema ) coincide con un patrón válido ( expresión regular) y retornar su token.
    Por detras, PLY genera un automata finito determinista y y construye una maquina de estados, el avance entre los caracteres lo hace automaticamente, y resuelve automaticamente la agrupacion de las palabras en base a la coincidencia más larga posible definida mientras el patrón de lectura siga siendo válido.
Parser:
    El analizador sintáctico va a verificar el orden de los tokens y revisar que la oración tenga sentido en su estructura.
    Toma la lista de tokens que recibe del scanner , y valida si las palabras, en el orden que llegaron, forman una estructura válida según la gramatica BNF y produce un AST ( arbol sintáctico)
    Cada función p representa una regla de producción de la gramática, se comenta la regla gramatical  en los docstrings y ply usa estos comentarios para reconocer las reglas.
    Si la regla se reconoce la función construye un diccionario, las estructuras pequeñas se combinan y la funcion p_programa  convierte la suma de estos diccionarios en un ast. 
Analizador semántico:
    Recibe el AST construido por el parser, y recorre el árbol verificando que tenga sentido según las reglas del lenguaje.
    Crea una tabla de simbolos utilizando un diccionario, en donde almacena los identificadores utilizados por el usuario, y el valor real de los mismos.
    Comprueba que las variables de identificador utilizadas hayan sido declaradas previamente (Consultando en su tabla de simbolos)
    Las funciones aplanar_mapa() y aplanar_juego() sirven para convertir los identificadores en los elementos que realmente representan, para posteriormente recorrer tanto el mapa como el juego de manera simultanea comparando 1 a 1 si los movimientos realizados corresponden al tipo de terreno.
    No solo verifica reglas estáticas, sino que recorre el mapa junto a los movimientos, por lo que hace parcialmente de interpete.
    El analizador retorna true o false, imprimiendo errores en caso de ser necesario.
    El analizador semántico también valida la lógica del juego. Si detecta una colisión o un movimiento inválido, el nivel se considera no jugable y el intérprete no se ejecuta 





## Objetivo del trabajo

Crear un lenguaje de dominio específico (DSL) llamado DINO que simula el entorno de un videojuego que consiste en esquivar objetivos.
El propósito del compilador es realizar una validación entre la creación de un nivel ganable y el comportamiento de un jugador para ganarlo.

---

## Características Principales

* Definir alias para elementos del entorno (trampas, aves, metas).
* Agrupar secuencias de acciones en "combos" o macros reutilizables.
* Construir la topología de un nivel (MAPA) usando bloques de entorno.
* Especificar el comportamiento de un agente o jugador (JUEGO).
* Validar si la secuencia de acciones permite superar el mapa definido.

---

## Alcance

* El lenguaje permitirá la parametrización mediante variables, otorgándole al programador flexibilidad en la creación de reglas reutilizables.
* El programa validará primero la estructura estática del entorno (el mapa) y luego simulará la lógica de ejecución del personaje.
* Como resultado, devolverá un reporte validando si el nivel es ganable o informando el motivo exacto del fallo.

---

## Especificaciones Léxicas

* **Palabras reservadas:** `MAPA` - `JUEGO` - `Validar`
* **Identificadores:** Cadenas de texto libre (pueden contener espacios) que deben ir estrictamente encerradas entre los símbolos `<` y `>`. Ej: `<Mi variable>`
* **Elementos:** `Lava` - `Pasto` - `Agua` - `Paloma` - `Aguila` - `Nave`
* **Movimientos:** `Correr` - `Nadar` - `Saltar` - `Despegar`
* **Modificadores:** `simple` - `doble` - `triple` - `mientras` - `si_es` - `si_hay`
* **Números:** `1` - `2` - `3` - `4` - `5` - `6` - `7` - `8` - `9` - `0`
* **Símbolos:** `{` - `}` - `(` - `)` - `.` - `,` - `=`

---

## Especificaciones Sintácticas

```text
<identificador> = elemento // <Trampa> = Lava
<identidicador> = movimiento // <CorrerMucho> = Correr(5)
<Identificador> = <Identificador>,Movimiento // <CorrerMás> = <CorrerMucho>,Correr(5)

Entorno{ 				// MAPA
    Elemento(Número)			// Pasto(10)
    ,Elemento	 	 	// ,Paloma
    ,Elemento(Número)		// Agua(3)
    ,Identificador	 		// Lava
    ,Elemento 				// Nave
}

Entorno { 					// JUEGO
    Movimiento					// Correr
    Movimiento.Modificador 			// Saltar.simple
    Movimiento.Modificador(Elemento)	// Correr.mientras(Pasto)
                                        // Nadar.mientras(Agua)
                                        // Despegar.si_hay(Nave)
    Movimiento.Modificador.Modificador(Elemento)  // Saltar.doble.si_es(Paloma) 
                                                  // Saltar.triple.si_es(Águila)
    Movimiento(Número)				 // Correr(2)
}

```

* Se permite asignar a un `<Identificador>` un elemento individual, un movimiento individual, o una secuencia de estos, separados por coma.
* En la declaración de una variable/macro, el lado derecho de la igualdad puede contener Elementos, Movimientos, y también otros `<Identificadores>` previamente definidos.
* Esto debe hacerse fuera de los bloques de entorno  `// <Secuencia escape> = Correr(5), Saltar[doble]`
* Dentro del entorno `JUEGO`, un `<Identificador>` puede utilizarse en reemplazo de un Movimiento normal.
* El símbolo `,` solo puede utilizarse para separar indicadores del mismo tipo (Elementos y Movimientos).
* Los entornos no pueden tener modificadores de ningún tipo y deben desarrollarse enteramente bajo `{` y `}`.
* Los símbolos `(` y `)` solo albergan números cuando son invocados junto a un Elemento o Movimiento, o Elementos al ser ejecutados junto a un Modificador.
* El modificador `si_es` solo puede usarse a continuación de otro modificador.

---

## Especificaciones Semánticas

* El símbolo `,` solo puede utilizarse para separar indicadores del mismo tipo. `Elemento,Elemento` / `Movimiento,Movimiento` / se incluye también entre identificadores del mismo tipo. `Elemento,<Identificador1>` siempre y cuando `<Identificador1>` sea un Elemento.
* El modificador `simple`, `doble` y `triple` solo pueden usarse con el Movimiento `Saltar`.
* El modificador `si_es` solo puede usarse a continuación de otro modificador y previo a `Águila` o `paloma` únicamente.
* Los Elementos `Agua` y `Pasto` son los únicos elementos que pueden ir acompañados de números. (Intentar hacer `Lava(3)` es un error de tipo).
* No puede haber más de una `lava`, `paloma`, o `águila` seguidas.
* Los elementos `Lava`, `Paloma` Y `Aguila` deben ir luego de un Elemento `Pasto`.
* La condición `si_es` solo es válida con `paloma` o `aguila`.
* La condición `si hay` solo es válida si hay `nave`.
* El entorno `MAPA` debe comenzar con al menos un elemento `Pasto`.
* El entorno `JUEGO` debe coincidir con el entorno `MAPA` bajo las siguientes reglas:
* La lava debe saltarse
* El agua debe nadarse
* Solo se puede correr en el Pasto
* Solo se puede nadar en el agua
* No se puede saltar inmediatamente después de salir del agua, o de haber realizado un salto previo.
* No se puede ejecutar un salto inmediatamente después de salir del Agua. Se requiere al menos un pasto.
* Se debe saltar doble una paloma y saltar triple un águila.
* Se debe despegar solo cuando hay una nave y esta debe ser el último elemento del mapa.


* Es un error intentar utilizar un Identificador en el bloque `MAPA` o `JUEGO` si este no fue declarado y asignado previamente en la parte superior del archivo.
* Es un error asignar un Número a una variable y luego intentar usarla como un elemento de mapa. `// <Cinco> = 5. Correr(<Cinco>)` No está permitido.
* No se pueden crear dos entornos (`MAPA` o `JUEGO`) con el mismo nombre.
* La función `Verificar(X, Y)` exige estrictamente que el primer parámetro sea un identificador de tipo `MAPA` y el segundo un identificador de tipo `JUEGO`.
* La acción `Saltar[simple]` es obligatoria para la entidad Lava. Usar un salto simple provocará un error de colisión.
* La acción `Saltar[doble]` es obligatoria para la entidad Paloma. Usar un salto simple provocará un error de colisión.
* La acción `Saltar[triple]` es obligatoria para la entidad Águila. Usar un salto simple provocará un error de colisión.
* La función `Verificar(MAPA, JUEGO)` debe retornar `True` (Nivel Válido y Ganable) o lanzar excepciones descriptivas si el jugador muere.
* Un `<Identificador>` sólo puede utilizar en su definición a otros identificadores que hayan sido declarados en líneas superiores.

---

## Gramatica BNF

```text
<Programa>            ::= <ListaDeclaraciones> <Mapa> <Juego> <Validacion>

<ListaDeclaraciones>  ::= <Declaracion> <ListaDeclaraciones>| λ

<Declaracion>         ::= ID "=" <Secuencia>

<Mapa>                ::= "MAPA" ID "{" <Secuencia> "}"

<Juego>               ::= "JUEGO" ID "{" <Secuencia> "}"

<Validacion>          ::= "Validar" "(" ID "," ID ")"

<Secuencia>           ::= <Invocacion> "," <Secuencia> | <Invocacion>

<Invocacion>          ::= ID | ELEMENTO <OpcionalParamNumero> | MOVIMIENTO <ExtensionMovimiento>

<OpcionalParamNumero> ::= "(" NUMERO ")" | λ

<ExtensionMovimiento> ::= "(" NUMERO ")" | <CadenaModificadores>| λ

<CadenaModificadores> ::= "." MODIFICADOR <OpcionesModificador>

<OpcionesModificador> ::= "." MODIFICADOR <OpcionesModificador> | "(" <ParametroModificador> ")" | λ

<ParametroModificador>::= ELEMENTO | ID
```

--------

