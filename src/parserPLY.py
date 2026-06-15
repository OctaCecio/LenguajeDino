import ply.yacc as yacc

tokens = (
    'ID', 'NUMERO', 'ELEMENTO', 'MOVIMIENTO', 'MODIFICADOR', 
    'TK_MAPA', 'TK_JUEGO', 'TK_VALIDAR'
)

literals = ['=', '{', '}', '(', ')', ',', '.']

def p_programa(p):
    '''programa : lista_declaraciones mapa juego validacion'''
    p[0] = {
        "tipo": "PROGRAMA",
        "declaraciones": p[1],
        "mapa": p[2],
        "juego": p[3],
        "validacion": p[4]
    }
    print("¡Análisis exitoso! AST generado correctamente.")

def p_lista_declaraciones(p):
    '''lista_declaraciones : declaracion lista_declaraciones
                           | empty'''
    if len(p) == 3: # para ver si entra por la opción recursiva
        p[0] = [p[1]] + p[2]
    else:           
        p[0] = []

def p_declaracion(p):
    '''declaracion : ID '=' secuencia'''
    p[0] = {
        "tipo": "DECLARACION",
        "identificador": p[1],
        "valor": p[3]
    }

def p_mapa(p):
    '''mapa : TK_MAPA ID '{' secuencia '}' '''
    p[0] = {
        "tipo": "MAPA",
        "nombre": p[2],
        "contenido": p[4]
    }

def p_juego(p):
    '''juego : TK_JUEGO ID '{' secuencia '}' '''
    p[0] = {
        "tipo": "JUEGO",
        "nombre": p[2],
        "contenido": p[4]
    }

def p_validacion(p):
    '''validacion : TK_VALIDAR '(' ID ',' ID ')' '''
    p[0] = {
        "tipo": "VALIDACION",
        "mapa_objetivo": p[3],
        "juego_objetivo": p[5]
    }

def p_secuencia(p):
    '''secuencia : invocacion ',' secuencia
                 | invocacion'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_invocacion(p):
    '''invocacion : ID
                  | ELEMENTO opcional_param_numero
                  | MOVIMIENTO extension_movimiento'''
    if len(p) == 2:
        p[0] = {"tipo": "INVOCACION_ID", "id": p[1]}
    elif p.slice[1].type == 'ELEMENTO':
        p[0] = {"tipo": "INVOCACION_ELEMENTO", "elemento": p[1], "cantidad": p[2]}
    elif p.slice[1].type == 'MOVIMIENTO':
        p[0] = {"tipo": "INVOCACION_MOVIMIENTO", "movimiento": p[1], "opciones": p[2]}

def p_extension_movimiento(p):
    '''extension_movimiento : '(' NUMERO ')'
                            | cadena_modificadores
                            | empty'''
    if len(p) == 4:
        p[0] = {"parametro_numerico": int(p[2]), "modificadores": []}
    elif p[1] is not None:
        p[0] = {"parametro_numerico": None, "modificadores": p[1]}
    else:
        p[0] = {"parametro_numerico": None, "modificadores": []}

def p_cadena_modificadores(p):
    '''cadena_modificadores : '.' MODIFICADOR opciones_modificador'''
    modificador_actual = {"nombre": p[2], "condicion": None}
    
    if isinstance(p[3], dict) and "condicion" in p[3]:
        modificador_actual["condicion"] = p[3]["condicion"]
        p[0] = [modificador_actual]
    elif isinstance(p[3], list): # si siguen mas modificadores
        p[0] = [modificador_actual] + p[3]
    else:
        p[0] = [modificador_actual]

def p_opciones_modificador(p):
    '''opciones_modificador : '.' MODIFICADOR opciones_modificador
                            | '(' parametro_modificador ')'
                            | empty'''
    if len(p) == 4 and p[1] == '.':
        modificador_actual = {"nombre": p[2], "condicion": None}
        if isinstance(p[3], dict) and "condicion" in p[3]:
            modificador_actual["condicion"] = p[3]["condicion"]
            p[0] = [modificador_actual]
        elif isinstance(p[3], list):
            p[0] = [modificador_actual] + p[3]
        else:
            p[0] = [modificador_actual]
    elif len(p) == 4 and p[1] == '(':
        p[0] = {"condicion": p[2]}
    else:
        p[0] = []

def p_parametro_modificador(p):
    '''parametro_modificador : ELEMENTO
                             | ID'''
    p[0] = p[1]

def p_opcional_param_numero(p):
    '''opcional_param_numero : '(' NUMERO ')'
                             | empty'''
    if len(p) == 4:
        p[0] = int(p[2])
    else:
        p[0] = None

# caso lambda
def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"ERROR SINTÁCTICO: cerca del token '{p.value}' (Tipo: {p.type})")
    else:
        print("ERROR SINTÁCTICO: Fin de archivo inesperado")

parser = yacc.yacc()