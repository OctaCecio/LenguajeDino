class LexerDino:
   
    T_RESERVADA = "RESERVADA"
    T_ELEMENTO = "ELEMENTO"
    T_MOVIMIENTO = "MOVIMIENTO"
    T_MODIFICADOR = "MODIFICADOR"
    T_IDENTIFICADOR = "ID"
    T_NUMERO = "NUMERO"
    T_SIMBOLO = "SIMBOLO"
    
    
    PALABRAS_CLAVE = {
    "MAPA": T_RESERVADA,
    "JUEGO": T_RESERVADA,
    "Validar": T_RESERVADA,
    
    "Lava": T_ELEMENTO, "Pasto": T_ELEMENTO, "Agua": T_ELEMENTO, 
    "Paloma": T_ELEMENTO, "Aguila": T_ELEMENTO, "Nave": T_ELEMENTO,
    
    "Correr": T_MOVIMIENTO, "Nadar": T_MOVIMIENTO, 
    "Saltar": T_MOVIMIENTO, "Despegar": T_MOVIMIENTO,
    
    "simple": T_MODIFICADOR, "doble": T_MODIFICADOR, "triple": T_MODIFICADOR,
    "mientras": T_MODIFICADOR, "si_es": T_MODIFICADOR, "si_hay": T_MODIFICADOR
    }

    def __init__(self, palabra):
        self.palabra = palabra
        self.cursor = -1
        self.linea_actual = 1

    def getCaracter(self):
        if (self.cursor + 1) < len(self.palabra):
            self.cursor += 1
            c = self.palabra[self.cursor]
            if c == '\n':  # asi podemos devolver la linea que tiene error
                self.linea_actual += 1
                
            return c# Y la devolvemos
        return None

    def retroceder(self):
        if self.cursor >= 0:
            # Si el caracter que vamos a devolver era un salto de línea,
            # tenemos que restar 1 al contador porque getCaracter lo sumó.
            if self.palabra[self.cursor] == '\n':
                self.linea_actual -= 1
            self.cursor -= 1

    def q0(self):
        c = self.getCaracter()
        
        if c in [' ', '\t', '\n', '\r']:
            return self.q0()
            
        if c == '<': #Comienzo a leer un id.
            return self.q_identificador() 
            
        if c is None: # Se termino el archivo
            return "EOF", None
            
        if c.isalpha(): #Es una letra
            self.retroceder()
            return self.q_palabra()
            
        if c.isdigit(): #Es un numero
            self.retroceder()
            return self.q_numero()
            
        if c in ['{', '}', '(', ')', '.', ',', '=']: # simbolos del lenguaje.
            return self.T_SIMBOLO, c
            
        return "ERROR LÉXICO", f"Carácter '{c}' no reconocido en la línea {self.linea_actual}"
        
    def q_identificador(self):
        lexema = ""
        while True:
            c = self.getCaracter()
            
            if c == '>':
                if lexema == "":
                    return "ERROR LÉXICO", f"Identificador vacío '<>' en la línea {self.linea_actual}"
                # Éxito: retornamos el token. Le agrego los <> al lexema devuelto 
                # para que sea más fácil distinguirlos visualmente después.
                return self.T_IDENTIFICADOR, f"<{lexema}>"
            
            if c is None:
                return "ERROR LÉXICO", f"Identificador '<{lexema}' sin cerrar en la línea {self.linea_actual}"
            
            lexema += c

        
    def q_palabra(self):
        lexema = ""
        while True:
            c = self.getCaracter()
            
            if c is not None and (c.isalnum() or c == '_'):
                lexema += c
            else:
                self.retroceder()
                break
            
        tipo_token = self.PALABRAS_CLAVE.get(lexema, "T_TEXTO_DESCONOCIDO")
        
        # EL CAMBIO CLAVE:
        if tipo_token == "T_TEXTO_DESCONOCIDO": 
            # Si no es MAPA, Lava, Correr, etc., entonces es un nombre crudo (ej: Nivel_Uno).
            # Lo devolvemos como ID para que el parser lo acepte.
            return self.T_IDENTIFICADOR, lexema
            
        return tipo_token, lexema

        
    def q_numero(self):
        lexema = ""
        while True:
            c = self.getCaracter()
            
            if c is not None and c.isdigit(): # si es un numero los vamos acumulando)
                lexema += c
            else:
                self.retroceder() # si deja de serlo, sacamos el que hizo que rompa, y lo devolvemo.
                break
        return self.T_NUMERO, lexema
        
    def tokenizar(self):
        tokens = []
        while True:
            tipo, lexema = self.q0()
            
            if tipo == "EOF":# Se terminó el archivo
                break 
                
            tokens.append((tipo, lexema))
            
            if tipo == "ERROR LÉXICO":
                print(lexema) # Imprimimos el error
                break         # Si hay un error, frenamos todo
                
        return tokens
        
