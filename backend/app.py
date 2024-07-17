from lexer import lexer
from parser import parser

# Ejemplos
data = '''
CREAR BASE DATOS mi_base;
USAR mi_base;
CREAR TABLA usuarios (id INT, nombre VARCHAR(100), edad INT);
ELIMINAR TABLA usuarios;
SELECCIONAR * DESDE usuarios DONDE id = 1;
INSERTAR EN usuarios (nombre, edad) VALORES ("Juan", 25);
ACTUALIZAR usuarios FIJAR edad = 26 DONDE nombre = "Juan";
BORRAR DESDE usuarios DONDE nombre = "Juan";
'''

# Análisis léxico
lexer.input(data)
print("Análisis Léxico")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

print("\nAnálisis Sintáctico\n")

# Análisis sintáctico
result = parser.parse(data)
print(result)
