## Objetivo

Crear un lenguaje que simula el entorno de un videojuego que consiste en esquivar objetivos.
Validando la creación de un nivel ganable y el comportamiento de un jugador para ganarlo.

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
* No puede haber más de una Lava, Paloma o Águila contiguas. Deben ir precedidas de un pasto.
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