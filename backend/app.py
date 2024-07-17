from lexer import lexer
from parser import parser
from semantic import check_semantics, db, execute_queries

# Ejemplo
data = '''
CREAR BASEDEDATOS mi_base;
USAR mi_base;
CREAR TABLA usuarios (id INT, nombre VARCHAR(100), edad INT);
ELIMINAR TABLA usuarios;
CREAR TABLA usuarios (id INT, nombre VARCHAR(100), edad INT);
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
