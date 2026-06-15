import json
from scannerPly import lexer
from parserPLY import parser
from semantica import AnalizadorSemantico
from motor_ascii import InterpreteASCII

if __name__ == '__main__':
    codigo_fuente = """
<Pista_Inicial> = Pasto(2)
<Fosa_Acuatica> = Agua(4)
<Trampa_Lava> = Lava
<Sprint> = Correr(2)

MAPA Nivel_Definitivo { 
    Pasto, 
    <Pista_Inicial>, 
    <Fosa_Acuatica>, 
    Pasto,
    Paloma, 
    <Pista_Inicial>, 
    <Trampa_Lava>, 
    Pasto, 
    Aguila, 
    Pasto, 
    Nave 
}

JUEGO Dino_Maestro { 
    Correr.mientras(Pasto), 
    Nadar.mientras(Agua), 
    Correr, 
    Saltar.doble.si_es(Paloma), 
    <Sprint>, 
    Saltar.simple, 
    Correr, 
    Saltar.triple.si_es(Aguila), 
    Correr, 
    Despegar.si_hay(Nave) 
}

Validar ( Nivel_Definitivo , Dino_Maestro )
    """

    print("--- INICIANDO COMPILADOR ---")
    
    # 1. Alimentamos el Lexer
    lexer.input(codigo_fuente)
    for tok in lexer:
        pass
    
        # 3. Parseamos y CAPTURAMOS EL AST
        lexer.lineno = 1  
        ast = parser.parse(codigo_fuente, lexer=lexer)
        # 4. Imprimimos el Árbol
        if ast:
            print("\n--- AST GENERADO ---")
            print(json.dumps(ast, indent=4))
    lexer.lineno = 1  
    ast = parser.parse(codigo_fuente, lexer=lexer)
    
    if ast:
            analizador = AnalizadorSemantico()
            es_valido = analizador.analizar(ast)
            if es_valido:
                # Volvemos a aplanar el mapa para pasárselo al motor gráfico
                mapa_plano = analizador.aplanar_mapa(ast["mapa"]["contenido"])
                
                motor = InterpreteASCII()
                motor.animar(mapa_plano)
