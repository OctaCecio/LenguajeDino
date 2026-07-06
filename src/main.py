from scannerPly import lexer
from parserPLY import parser
from semantica import AnalizadorSemantico
from motor_ascii import InterpreteASCII
import os 

def compilar_y_jugar(ruta_archivo):
    print(f"Cargando nivel: {ruta_archivo}...")
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en la ruta '{ruta_archivo}'.")
        return

    ast = parser.parse(codigo, lexer=lexer)

    if ast:
        analizador = AnalizadorSemantico()
        
        if analizador.analizar(ast):
            mapa = analizador.aplanar_mapa(ast["mapa"]["contenido"])
            interprete = InterpreteASCII()
            interprete.animar(mapa)
        else:
            print("\n Compilación cancelada por errores semánticos.")
    else:
        print("\n Compilación cancelada por errores de sintaxis.")

if __name__ == "__main__":
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    RUTA_ARCHIVO = os.path.join(directorio_actual, "Niveles", "dinoGanador2.dino")
    
    compilar_y_jugar(RUTA_ARCHIVO)