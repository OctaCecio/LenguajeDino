class ParserDino:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        # token_actual es la tupla que llega del scanner: (TIPO, LEXEMA)
        self.token_actual = self.tokens[self.cursor] if self.tokens else None

    def avanzar(self):
        self.cursor += 1
        if self.cursor < len(self.tokens):
            self.token_actual = self.tokens[self.cursor]
        else:
            self.token_actual = ("EOF", None)

    def match(self, tipo_esperado, valor_esperado=None):
        if self.token_actual and self.token_actual[0] == tipo_esperado:
            if valor_esperado is None or self.token_actual[1] == valor_esperado:
                lexema_consumido = self.token_actual[1]
                self.avanzar()
                return lexema_consumido
                
        esperado = valor_esperado if valor_esperado else tipo_esperado
        encontrado = self.token_actual[1] if self.token_actual else "FIN DE ARCHIVO"
        raise SyntaxError(f"Error Sintáctico: Se esperaba '{esperado}', pero se encontró '{encontrado}'")

    # Reglas de la gramatica

    # <Programa> ::= <ListaDeclaraciones> <Mapa> <Juego> <Validacion>
    def parse_Programa(self):
        print("Iniciando análisis sintáctico...")
        self.parse_ListaDeclaraciones()
        self.parse_Mapa()
        self.parse_Juego()
        self.parse_Validacion()
        print("¡Análisis Sintáctico Exitoso! El código tiene la forma correcta.")

    # <ListaDeclaraciones> ::= <Declaracion> <ListaDeclaraciones> | λ
    def parse_ListaDeclaraciones(self):
        if self.token_actual and self.token_actual[0] == "ID":
            siguiente_token = self.tokens[self.cursor + 1] if self.cursor + 1 < len(self.tokens) else None
            if siguiente_token and siguiente_token[1] == "=":
                self.parse_Declaracion()
                self.parse_ListaDeclaraciones() 

    # <Declaracion> ::= ID "=" <Secuencia>
    def parse_Declaracion(self):
        self.match("ID")
        self.match("SIMBOLO", "=")
        self.parse_Secuencia()

    # <Mapa> ::= "MAPA" ID "{" <Secuencia> "}"
    def parse_Mapa(self):
        self.match("RESERVADA", "MAPA")
        self.match("ID") 
        self.match("SIMBOLO", "{")
        self.parse_Secuencia()
        self.match("SIMBOLO", "}")

    # <Juego> ::= "JUEGO" ID "{" <Secuencia> "}"
    def parse_Juego(self):
        self.match("RESERVADA", "JUEGO")
        self.match("ID")
        self.match("SIMBOLO", "{")
        self.parse_Secuencia()
        self.match("SIMBOLO", "}")

    # <Validacion> ::= "Validar" "(" ID "," ID ")"
    def parse_Validacion(self):
        self.match("RESERVADA", "Validar")
        self.match("SIMBOLO", "(")
        self.match("ID")
        self.match("SIMBOLO", ",")
        self.match("ID")
        self.match("SIMBOLO", ")")

    # <Secuencia> ::= <Invocacion> "," <Secuencia> | <Invocacion>
    def parse_Secuencia(self):
        self.parse_Invocacion()
        if self.token_actual and self.token_actual[1] == ",":
            self.match("SIMBOLO", ",")
            self.parse_Secuencia()

    # <Invocacion> ::= ID | ELEMENTO <OpcionalParamNumero> | MOVIMIENTO <ExtensionMovimiento>
    def parse_Invocacion(self):
        tipo = self.token_actual[0]
        
        if tipo == "ID":
            self.match("ID")
        elif tipo == "ELEMENTO":
            self.match("ELEMENTO")
            self.parse_OpcionalParamNumero()
        elif tipo == "MOVIMIENTO":
            self.match("MOVIMIENTO")
            self.parse_ExtensionMovimiento()
        else:
            raise SyntaxError(f"Se esperaba una Acción (ID, ELEMENTO o MOVIMIENTO), se encontró: {self.token_actual[1]}")

    # <ExtensionMovimiento> ::= "(" NUMERO ")" | <CadenaModificadores> | λ
    def parse_ExtensionMovimiento(self):
        if self.token_actual and self.token_actual[1] == "(":
            self.match("SIMBOLO", "(")
            self.match("NUMERO")
            self.match("SIMBOLO", ")")
        elif self.token_actual and self.token_actual[1] == ".":
            self.parse_CadenaModificadores()

    # <CadenaModificadores> ::= "." MODIFICADOR <OpcionesModificador>
    def parse_CadenaModificadores(self):
        self.match("SIMBOLO", ".")
        self.match("MODIFICADOR")
        self.parse_OpcionesModificador()

    # <OpcionesModificador> ::= "." MODIFICADOR <OpcionesModificador> | "(" <ParametroModificador> ")" | λ
    def parse_OpcionesModificador(self):
        if self.token_actual and self.token_actual[1] == ".":
            self.match("SIMBOLO", ".")
            self.match("MODIFICADOR")
            self.parse_OpcionesModificador() 
        elif self.token_actual and self.token_actual[1] == "(":
            self.match("SIMBOLO", "(")
            self.parse_ParametroModificador()
            self.match("SIMBOLO", ")")

    # <ParametroModificador> ::= ELEMENTO | ID
    def parse_ParametroModificador(self):
        tipo = self.token_actual[0]
        if tipo == "ELEMENTO":
            self.match("ELEMENTO")
        elif tipo == "ID":
            self.match("ID")
        else:
            raise SyntaxError(f"El parámetro de un modificador debe ser ELEMENTO o ID, se encontró: {self.token_actual[1]}")

    # <OpcionalParamNumero> ::= "(" NUMERO ")" | λ
    def parse_OpcionalParamNumero(self):
        if self.token_actual and self.token_actual[1] == "(":
            self.match("SIMBOLO", "(")
            self.match("NUMERO")
            self.match("SIMBOLO", ")")
