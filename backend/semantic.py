import sqlite3

class Database:
    def __init__(self, db_name='mi_base.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.current_db = None

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return None
        except sqlite3.Error as e:
            return str(e)

    def create_database(self, name):
        self.current_db = name
        return None

    def use_database(self, name):
        self.current_db = name
        return None

    def create_table(self, name, columns):
        columns_def = ', '.join(f"{col[0]} {col[1][0]}({col[1][1]})" if len(col[1]) > 1 else f"{col[0]} {col[1][0]}" for col in columns)
        query = f"CREATE TABLE {name} ({columns_def})"
        return self.execute(query)

    def drop_table(self, name):
        query = f"DROP TABLE IF EXISTS {name}"
        return self.execute(query)

    def table_exists(self, name):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        self.cursor.execute(query, (name,))
        return self.cursor.fetchone() is not None

    def column_exists(self, table, column):
        query = f"PRAGMA table_info({table})"
        self.cursor.execute(query)
        columns = [info[1] for info in self.cursor.fetchall()]
        return column in columns

    def get_column_type(self, table, column):
        query = f"PRAGMA table_info({table})"
        self.cursor.execute(query)
        for info in self.cursor.fetchall():
            if info[1] == column:
                return info[2]
        return None

db = Database()

def check_semantics(commands):
    errors = []
    for command in commands:
        if command[0] == 'crear_base':
            error = db.create_database(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'usar_base':
            error = db.use_database(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'crear_tabla':
            error = db.create_table(command[1], command[2])
            if error:
                errors.append(error)
        elif command[0] == 'eliminar_tabla':
            error = db.drop_table(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'seleccionar':
            table = command[2]
            if not db.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            elif command[1] != '*':
                for col in command[1]:
                    if not db.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
            if command[3] is not None:
                if not db.column_exists(table, command[3][0]):
                    errors.append(f"Error: La columna '{command[3][0]}' no existe en la tabla '{table}'.")
        elif command[0] == 'insertar':
            table = command[1]
            if not db.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                for col, val in zip(command[2], command[3]):
                    if not db.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
                    elif not isinstance(val, int) and db.get_column_type(table, col) == 'INT':
                        errors.append(f"Error: Tipo de dato incorrecto para la columna '{col}'. Se esperaba 'INT'.")
        elif command[0] == 'actualizar':
            table = command[1]
            if not db.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                for col, op, val in command[2]:
                    if not db.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
                    elif not isinstance(val, int) and db.get_column_type(table, col) == 'INT':
                        errors.append(f"Error: Tipo de dato incorrecto para la columna '{col}'. Se esperaba 'INT'.")
                if not db.column_exists(table, command[3][0]):
                    errors.append(f"Error: La columna '{command[3][0]}' no existe en la tabla '{table}'.")
        elif command[0] == 'borrar':
            table = command[1]
            if not db.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                if not db.column_exists(table, command[2][0]):
                    errors.append(f"Error: La columna '{command[2][0]}' no existe en la tabla '{table}'.")

    return errors

def execute_queries(commands):
    for command in commands:
        if command[0] == 'crear_base':
            print(f"Creando base de datos '{command[1]}'...")
            db.create_database(command[1])
        elif command[0] == 'usar_base':
            print(f"Usando base de datos '{command[1]}'...")
            db.use_database(command[1])
        elif command[0] == 'crear_tabla':
            print(f"Creando tabla '{command[1]}' con columnas {command[2]}...")
            db.create_table(command[1], command[2])
        elif command[0] == 'eliminar_tabla':
            print(f"Eliminando tabla '{command[1]}'...")
            db.drop_table(command[1])
        elif command[0] == 'seleccionar':
            print(f"Seleccionando {command[1]} desde '{command[2]}' donde {command[3]}...")
            if command[1] == '*':
                query = f"SELECT * FROM {command[2]}"
            else:
                query = f"SELECT {', '.join(command[1])} FROM {command[2]}"
            if command[3]:
                query += f" WHERE {command[3][0]} = ?"
                params = (command[3][2],)
            else:
                params = ()
            db.cursor.execute(query, params)
            for row in db.cursor.fetchall():
                print(row)
        elif command[0] == 'insertar':
            print(f"Insertando en '{command[1]}' columnas {command[2]} valores {command[3]}...")
            placeholders = ', '.join(['?'] * len(command[3]))
            query = f"INSERT INTO {command[1]} ({', '.join(command[2])}) VALUES ({placeholders})"
            db.execute(query, command[3])
        elif command[0] == 'actualizar':
            print(f"Actualizando '{command[1]}' fijar {command[2]} donde {command[3]}...")
            assignments = ', '.join([f"{col} = ?" for col, _, _ in command[2]])
            query = f"UPDATE {command[1]} SET {assignments} WHERE {command[3][0]} = ?"
            params = [val for _, _, val in command[2]] + [command[3][2]]
            db.execute(query, params)
        elif command[0] == 'borrar':
            print(f"Borrando desde '{command[1]}' donde {command[2]}...")
            query = f"DELETE FROM {command[1]} WHERE {command[2][0]} = ?"
            db.execute(query, (command[2][2],))
