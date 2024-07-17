import ply.yacc as yacc
from lexer import tokens

# Definición de la gramática
def p_query(p):
    '''query : query crear_base
             | query usar_base
             | query eliminar_base
             | query crear_tabla
             | query eliminar_tabla
             | query seleccionar
             | query insertar
             | query actualizar
             | query borrar
             | crear_base
             | usar_base
             | eliminar_base
             | crear_tabla
             | eliminar_tabla
             | seleccionar
             | insertar
             | actualizar
             | borrar'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_crear_base(p):
    'crear_base : CREAR BASE DATOS IDENTIFICADOR PUNTO_COMA'
    p[0] = ('crear_base', p[4])

def p_usar_base(p):
    'usar_base : USAR IDENTIFICADOR PUNTO_COMA'
    p[0] = ('usar_base', p[2])

def p_eliminar_base(p):
    'eliminar_base : ELIMINAR BASE DATOS IDENTIFICADOR PUNTO_COMA'
    p[0] = ('eliminar_base', p[4])

def p_crear_tabla(p):
    'crear_tabla : CREAR TABLA IDENTIFICADOR LPAREN definiciones_columnas RPAREN PUNTO_COMA'
    p[0] = ('crear_tabla', p[3], p[5])

def p_definiciones_columnas(p):
    '''definiciones_columnas : definiciones_columnas COMA definicion_columna
                             | definicion_columna'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_definicion_columna(p):
    'definicion_columna : IDENTIFICADOR tipo_columna'
    p[0] = (p[1], p[2])

def p_tipo_columna(p):
    '''tipo_columna : IDENTIFICADOR LPAREN NUMERO RPAREN
                    | IDENTIFICADOR'''
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1],)

def p_eliminar_tabla(p):
    'eliminar_tabla : ELIMINAR TABLA IDENTIFICADOR PUNTO_COMA'
    p[0] = ('eliminar_tabla', p[3])

def p_seleccionar(p):
    '''seleccionar : SELECCIONAR lista_columnas DESDE IDENTIFICADOR condicion_opt PUNTO_COMA
                   | SELECCIONAR ASTERISCO DESDE IDENTIFICADOR condicion_opt PUNTO_COMA'''
    if p[2] == '*':
        p[0] = ('seleccionar', '*', p[4], p[5])
    else:
        p[0] = ('seleccionar', p[2], p[4], p[5])

def p_lista_columnas(p):
    '''lista_columnas : lista_columnas COMA IDENTIFICADOR
                      | IDENTIFICADOR'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_condicion_opt(p):
    '''condicion_opt : DONDE condicion
                     | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_condicion(p):
    'condicion : IDENTIFICADOR IGUAL valor'
    p[0] = (p[1], '=', p[3])

def p_valor(p):
    '''valor : NUMERO
             | CADENA'''
    p[0] = p[1]

def p_insertar(p):
    'insertar : INSERTAR EN IDENTIFICADOR LPAREN lista_columnas RPAREN VALORES LPAREN lista_valores RPAREN PUNTO_COMA'
    p[0] = ('insertar', p[3], p[5], p[9])

def p_lista_valores(p):
    '''lista_valores : lista_valores COMA valor
                     | valor'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_actualizar(p):
    'actualizar : ACTUALIZAR IDENTIFICADOR FIJAR asignaciones condicion_opt PUNTO_COMA'
    p[0] = ('actualizar', p[2], p[4], p[5])

def p_asignaciones(p):
    '''asignaciones : asignaciones COMA asignacion
                    | asignacion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_asignacion(p):
    'asignacion : IDENTIFICADOR IGUAL valor'
    p[0] = (p[1], '=', p[3])

def p_borrar(p):
    'borrar : BORRAR DESDE IDENTIFICADOR condicion_opt PUNTO_COMA'
    p[0] = ('borrar', p[3], p[4])

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en línea {p.lineno}")
    else:
        print("Error de sintaxis al final de la entrada")

parser = yacc.yacc()
