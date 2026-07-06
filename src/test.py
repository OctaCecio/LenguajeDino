import os
from pathlib import Path

from scannerPly import lexer
from parserPLY import parser
from semantica import AnalizadorSemantico

CARPETA_NIVELES = Path(__file__).resolve().parent / "Niveles"

def ejecutar_prueba(ruta_archivo):

    with open(ruta_archivo, "r", encoding="utf-8-sig") as archivo:
        codigo = archivo.read()

    # ==================================================
    # ETAPA 1 - SCANNER
    # ==================================================
    lexer.lineno = 1
    lexer.hubo_error = False

    lexer.input(codigo)

    while lexer.token():
        pass

    if lexer.hubo_error:
        return False

    # ==================================================
    # ETAPA 2 - PARSER
    # ==================================================
    lexer.lineno = 1
    lexer.hubo_error = False

    ast = parser.parse(codigo, lexer=lexer)

    if ast is None:
        return False

    # ==================================================
    # ETAPA 3 - ANALIZADOR SEMÁNTICO
    # ==================================================
    analizador = AnalizadorSemantico()

    return analizador.analizar(ast)

def main():

    if not CARPETA_NIVELES.exists():
        print("No existe la carpeta Niveles.")
        return

    archivos = sorted(CARPETA_NIVELES.glob("*.dino"))

    print("\n========== TEST AUTOMATIZADO ==========\n")

    ok = 0

    for i, archivo in enumerate(archivos, start=1):

        print("-" * 60)

        try:
            resultado = ejecutar_prueba(archivo)

            if resultado:
                print(f'Archivo {i}: "{archivo.name}" -> OK')
                ok += 1
            else:
                print(f'Archivo {i}: "{archivo.name}" -> ERROR')

        except Exception as e:
            print(e)
            print(f'Archivo {i}: "{archivo.name}" -> ERROR')

        print()

    print("=" * 60)
    print(f"Total: {len(archivos)}")
    print(f"Correctos: {ok}")
    print(f"Con errores: {len(archivos)-ok}")
    print("=" * 60)


if __name__ == "__main__":
    main()