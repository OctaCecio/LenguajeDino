import ply.lex as lex

reservadas = {
    "MAPA": "TK_MAPA",
    "JUEGO": "TK_JUEGO",
    "Validar": "TK_VALIDAR",
    
    "Lava": "ELEMENTO", "Pasto": "ELEMENTO", "Agua": "ELEMENTO", 
    "Paloma": "ELEMENTO", "Aguila": "ELEMENTO", "Nave": "ELEMENTO",
    
    "Correr": "MOVIMIENTO", "Nadar": "MOVIMIENTO", 
    "Saltar": "MOVIMIENTO", "Despegar": "MOVIMIENTO",
    
    "simple": "MODIFICADOR", "doble": "MODIFICADOR", "triple": "MODIFICADOR",
    "mientras": "MODIFICADOR", "si_es": "MODIFICADOR", "si_hay": "MODIFICADOR"
}

tokens = (
    'ID',
    'NUMERO',
    'TK_MAPA',
    'TK_JUEGO',
    'TK_VALIDAR',
    'ELEMENTO',
    'MOVIMIENTO',
    'MODIFICADOR'
)

literals = ['{', '}', '(', ')', '.', ',', '=', '<', '>']

t_ignore = ' \t\r'



def t_NUMERO(t):
    r'\d+'
    return t


def t_ID_CORCHETE(t):
    r'<[^>]+>'
    t.type = 'ID'  
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')    
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"ERROR LÉXICO: Carácter '{t.value[0]}' no reconocido en la línea {t.lexer.lineno}")
    t.lexer.hubo_error = True
    t.lexer.skip(1) #Sigue leyendo ignorando el caracter que dio error, asi de una sola ejecución trae todos los errores.

lexer = lex.lex()
lexer.hubo_error = False
