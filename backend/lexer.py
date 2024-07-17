import ply.lex as lex

# tokens
tokens = (
    'SELECCIONAR',
    'DESDE',
    'DONDE',
    'INSERTAR',
    'ACTUALIZAR',
    'BORRAR',
    'EN',
    'VALORES',
    'FIJAR',
    'Y',
    'O',
    'CREAR',
    'BASEDEDATOS',
    'TABLA',
    'ELIMINAR',
    'USAR',
    'IDENTIFICADOR',
    'NUMERO',
    'CADENA',
    'IGUAL',
    'MENOR',
    'MAYOR',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'DIFERENTE',
    'ASTERISCO',
    'LPAREN',
    'RPAREN',
    'PUNTO_COMA',
    'COMA'
)

# Regular expressions for tokens
t_IGUAL = r'='
t_MENOR = r'<'
t_MAYOR = r'>'
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_DIFERENTE = r'!='
t_ASTERISCO = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PUNTO_COMA = r';'
t_COMA = r','

def t_SELECCIONAR(t):
    r'SELECCIONAR'
    return t

def t_DESDE(t):
    r'DESDE'
    return t

def t_DONDE(t):
    r'DONDE'
    return t

def t_INSERTAR(t):
    r'INSERTAR'
    return t

def t_ACTUALIZAR(t):
    r'ACTUALIZAR'
    return t

def t_BORRAR(t):
    r'BORRAR'
    return t

def t_EN(t):
    r'EN'
    return t

def t_VALORES(t):
    r'VALORES'
    return t

def t_FIJAR(t):
    r'FIJAR'
    return t

def t_Y(t):
    r'Y'
    return t

def t_O(t):
    r'O'
    return t

def t_CREAR(t):
    r'CREAR'
    return t

def t_BASEDEDATOS(t):
    r'BASEDEDATOS'
    return t

def t_TABLA(t):
    r'TABLA'
    return t

def t_ELIMINAR(t):
    r'ELIMINAR'
    return t

def t_USAR(t):
    r'USAR'
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'"(?:\\["\\]|[^\n"\\])*"'
    t.value = t.value[1:-1] 
    return t

t_ignore = ' \t'

def t_comment(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
