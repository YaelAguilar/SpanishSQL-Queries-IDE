from lexer import lexer
from parser import parser
from semantic import check_semantics, db, execute_queries

# Datos de prueba
data = '''
CREAR BASEDEDATOS mi_base;
USAR mi_base;
CREAR TABLA usuarios (id INT, nombre VARCHAR(100), edad INT);
INSERTAR EN usuarios (id, nombre, edad) VALORES (1, "Juan", 25);
INSERTAR EN usuarios (id, nombre, edad) VALORES (2, "Ana", 30);
SELECCIONAR * DESDE usuarios;
ACTUALIZAR usuarios FIJAR edad = 26 DONDE nombre = "Juan";
SELECCIONAR * DESDE usuarios;
BORRAR DESDE usuarios DONDE nombre = "Juan";
SELECCIONAR * DESDE usuarios;
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

print("\nAnálisis Semántico\n")

# Análisis semántico
errors = check_semantics(result)
if errors:
    print("Errores semánticos:")
    for error in errors:
        print(error)
else:
    print("No se encontraron errores semánticos.")
    print("\nEjecución de Consultas\n")
    execute_queries(result)
