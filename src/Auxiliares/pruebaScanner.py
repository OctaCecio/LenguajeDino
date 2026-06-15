from Auxiliares.scanner import LexerDino  

codigo_prueba = """
<Trampa mortal> = Correr
Pasto(3), <Trampa mortal>
"""

mi_lexer = LexerDino(codigo_prueba)
lista_de_tokens = mi_lexer.tokenizar()

print("--- LISTA DE TOKENS ENCONTRADOS ---")
for t in lista_de_tokens:
    print(t)


mi_lexer = LexerDino(codigo_prueba)
lista_de_tokens = mi_lexer.tokenizar()

for t in lista_de_tokens:
    print(t)



