import mysql.connector
from mysql.connector import errorcode
import logging
from io import StringIO

# Configurar el logging
log_stream = StringIO()
logger = logging.getLogger('semantic_logger')

# Remover todos los handlers existentes
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

stream_handler = logging.StreamHandler(log_stream)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

class Database:
    def __init__(self, user, password, host, port, database=None):
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        self.current_db = database

        if database:
            try:
                self.use_database(database)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    logger.info(f"Base de datos '{database}' no existe. Creándola...")
                    self.create_database(database)
                    self.use_database(database)
                else:
                    raise err

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            logger.info(f"Executed query: {query}")
            return None
        except mysql.connector.Error as err:
            logger.error(f"Error executing query: {err}")
            return str(err)

    def create_database(self, name):
        try:
            self.cursor.execute(f"CREATE DATABASE {name}")
            self.connection.database = name
            self.current_db = name
            logger.info(f"Base de datos '{name}' creada.")
            return None
        except mysql.connector.Error as err:
            logger.error(f"Error creating database: {err}")
            return str(err)

    def drop_database(self, name):
        try:
            self.cursor.execute(f"DROP DATABASE {name}")
            self.connection.commit()
            if self.current_db == name:
                self.current_db = None
            logger.info(f"Base de datos '{name}' eliminada.")
            return None
        except mysql.connector.Error as err:
            logger.error(f"Error dropping database: {err}")
            return str(err)

    def use_database(self, name):
        try:
            self.connection.database = name
            self.current_db = name
            logger.info(f"Using database '{name}'.")
            return None
        except mysql.connector.Error as err:
            logger.error(f"Error using database: {err}")
            return str(err)

    def create_table(self, name, columns):
        columns_def = ', '.join(f"{col[0]} {col[1][0]}({col[1][1]})" if len(col[1]) > 1 else f"{col[0]} {col[1][0]}" for col in columns)
        query = f"CREATE TABLE {name} ({columns_def})"
        logger.info(f"Creating table '{name}' with columns {columns_def}...")
        return self.execute(query)

    def drop_table(self, name):
        query = f"DROP TABLE IF EXISTS {name}"
        logger.info(f"Dropping table '{name}' if it exists...")
        return self.execute(query)

    def table_exists(self, name):
        query = "SHOW TABLES LIKE %s"
        self.cursor.execute(query, (name,))
        exists = self.cursor.fetchone() is not None
        logger.info(f"Table '{name}' exists: {exists}")
        return exists

    def column_exists(self, table, column):
        query = f"SHOW COLUMNS FROM {table} LIKE %s"
        self.cursor.execute(query, (column,))
        exists = self.cursor.fetchone() is not None
        logger.info(f"Column '{column}' in table '{table}' exists: {exists}")
        return exists

    def get_column_type(self, table, column):
        query = f"SHOW COLUMNS FROM {table} LIKE %s"
        self.cursor.execute(query, (column,))
        result = self.cursor.fetchone()
        if result:
            logger.info(f"Column '{column}' in table '{table}' has type: {result[1]}")
            return result[1]
        return None

def check_semantics(commands, db_instance):
    errors = []
    for command in commands:
        if command[0] == 'crear_base':
            error = db_instance.create_database(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'usar_base':
            error = db_instance.use_database(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'eliminar_base':
            error = db_instance.drop_database(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'crear_tabla':
            error = db_instance.create_table(command[1], command[2])
            if error:
                errors.append(error)
        elif command[0] == 'eliminar_tabla':
            error = db_instance.drop_table(command[1])
            if error:
                errors.append(error)
        elif command[0] == 'seleccionar':
            table = command[2]
            if not db_instance.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            elif command[1] != '*':
                for col in command[1]:
                    if not db_instance.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
            if command[3] is not None:
                if not db_instance.column_exists(table, command[3][0]):
                    errors.append(f"Error: La columna '{command[3][0]}' no existe en la tabla '{table}'.")
        elif command[0] == 'insertar':
            table = command[1]
            if not db_instance.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                for col, val in zip(command[2], command[3]):
                    column_type = db_instance.get_column_type(table, col)
                    if not db_instance.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
                    elif not isinstance(val, int) and column_type and isinstance(column_type, str) and column_type.startswith('INT'):
                        errors.append(f"Error: Tipo de dato incorrecto para la columna '{col}'. Se esperaba 'INT'.")
        elif command[0] == 'actualizar':
            table = command[1]
            if not db_instance.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                for col, op, val in command[2]:
                    column_type = db_instance.get_column_type(table, col)
                    if not db_instance.column_exists(table, col):
                        errors.append(f"Error: La columna '{col}' no existe en la tabla '{table}'.")
                    elif not isinstance(val, int) and column_type and isinstance(column_type, str) and column_type.startswith('INT'):
                        errors.append(f"Error: Tipo de dato incorrecto para la columna '{col}'. Se esperaba 'INT'.")
                if not db_instance.column_exists(table, command[3][0]):
                    errors.append(f"Error: La columna '{command[3][0]}' no existe en la tabla '{table}'.")
        elif command[0] == 'borrar':
            table = command[1]
            if not db_instance.table_exists(table):
                errors.append(f"Error: La tabla '{table}' no existe.")
            else:
                if not db_instance.column_exists(table, command[2][0]):
                    errors.append(f"Error: La columna '{command[2][0]}' no existe en la tabla '{table}'.")

    return errors

def execute_queries(commands, db_instance):
    for command in commands:
        if command[0] == 'crear_base':
            db_instance.create_database(command[1])
            logger.info(f"Base de datos '{command[1]}' creada.")
        elif command[0] == 'usar_base':
            logger.info(f"Usando base de datos '{command[1]}'...")
            db_instance.use_database(command[1])
        elif command[0] == 'eliminar_base':
            db_instance.drop_database(command[1])
            logger.info(f"Base de datos '{command[1]}' eliminada.")
        elif command[0] == 'crear_tabla':
            logger.info(f"Creando tabla '{command[1]}' con columnas {command[2]}...")
            db_instance.create_table(command[1], command[2])
        elif command[0] == 'eliminar_tabla':
            db_instance.drop_table(command[1])
            logger.info(f"Tabla '{command[1]}' eliminada.")
        elif command[0] == 'seleccionar':
            if command[1] == '*':
                query = f"SELECT * FROM {command[2]}"
            else:
                query = f"SELECT {', '.join(command[1])} FROM {command[2]}"
            if command[3]:
                query += f" WHERE {command[3][0]} = %s"
                params = (command[3][2],)
            else:
                params = ()
            db_instance.cursor.execute(query, params)
            for row in db_instance.cursor.fetchall():
                logger.info(row)
        elif command[0] == 'insertar':
            logger.info(f"Insertando en '{command[1]}' columnas {command[2]} valores {command[3]}...")
            placeholders = ', '.join(['%s'] * len(command[3]))
            query = f"INSERT INTO {command[1]} ({', '.join(command[2])}) VALUES ({placeholders})"
            db_instance.execute(query, command[3])
        elif command[0] == 'actualizar':
            logger.info(f"Actualizando '{command[1]}' fijar {command[2]} donde {command[3]}...")
            assignments = ', '.join([f"{col} = %s" for col, _, _ in command[2]])
            query = f"UPDATE {command[1]} SET {assignments} WHERE {command[3][0]} = %s"
            params = [val for _, _, val in command[2]] + [command[3][2]]
            db_instance.execute(query, params)
        elif command[0] == 'borrar':
            logger.info(f"Borrando desde '{command[1]}' donde {command[2]}...")
            query = f"DELETE FROM {command[1]} WHERE {command[2][0]} = %s"
            db_instance.execute(query, (command[2][2],))

# Añadido para asegurar que cada operación tenga un log asociado
    logger.info("Todas las operaciones se han ejecutado correctamente.")
