from scanner import LexerDino  
from parser import ParserDino 


def ejecutar_compilador(codigo):
    print("--- INICIANDO COMPILADOR DINO ---")
    
    lexer = LexerDino(codigo)
    tokens = lexer.tokenizar()
    
    if not tokens or tokens[-1][0] == "ERROR LÉXICO":
        print("El proceso falló en la fase léxica.")
        return

    print(f"Tokens generados: {tokens}")
    
    try:
        parser = ParserDino(tokens)
        parser.parse_Programa() # Inicia el análisis por la regla inicial
    except SyntaxError as e:
        print(f"\n¡Error encontrado! {e}")

codigo_ejemplo = """
<Meta> = Nave

MAPA Nivel_Uno {
    Pasto(3), <Meta>
}

JUEGO Dino_Azul {
    Correr(3), Saltar.simple, Despegar.si_hay(<Meta>)
}

Validar(Nivel_Uno, Dino_Azul)
"""

ejecutar_compilador(codigo_ejemplo)