class Database:
    def __init__(self):
        self.databases = {}
        self.current_db = None

    def create_database(self, name):
        if name in self.databases:
            return f"Error: La base de datos '{name}' ya existe."
        self.databases[name] = {}
        return None

    def use_database(self, name):
        if name not in self.databases:
            return f"Error: La base de datos '{name}' no existe."
        self.current_db = name
        return None

    def create_table(self, name, columns):
        if self.current_db is None:
            return "Error: No se ha seleccionado ninguna base de datos."
        db = self.databases[self.current_db]
        if name in db:
            return f"Error: La tabla '{name}' ya existe en la base de datos '{self.current_db}'."
        db[name] = {col[0]: col[1] for col in columns}
        return None

    def drop_table(self, name):
        if self.current_db is None:
            return "Error: No se ha seleccionado ninguna base de datos."
        db = self.databases[self.current_db]
        if name not in db:
            return f"Error: La tabla '{name}' no existe en la base de datos '{self.current_db}'."
        del db[name]
        return None

    def table_exists(self, name):
        if self.current_db is None:
            return False
        return name in self.databases[self.current_db]

    def column_exists(self, table, column):
        if self.current_db is None:
            return False
        return column in self.databases[self.current_db].get(table, {})

    def get_column_type(self, table, column):
        if self.current_db is None:
            return None
        return self.databases[self.current_db].get(table, {}).get(column, None)


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
            # Aquí puedes implementar la lógica para seleccionar datos
        elif command[0] == 'insertar':
            print(f"Insertando en '{command[1]}' columnas {command[2]} valores {command[3]}...")
            # Aquí puedes implementar la lógica para insertar datos
        elif command[0] == 'actualizar':
            print(f"Actualizando '{command[1]}' fijar {command[2]} donde {command[3]}...")
            # Aquí puedes implementar la lógica para actualizar datos
        elif command[0] == 'borrar':
            print(f"Borrando desde '{command[1]}' donde {command[2]}...")
            # Aquí puedes implementar la lógica para borrar datos
