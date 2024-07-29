import mysql.connector
from mysql.connector import errorcode
import logging
from io import StringIO

# Configurar el logging
log_stream = StringIO()
logger = logging.getLogger()

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
                    logging.info(f"Base de datos '{database}' no existe. Creándola...")
                    self.create_database(database)
                    self.use_database(database)
                else:
                    raise err

    def execute(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return None
        except mysql.connector.Error as err:
            return str(err)

    def create_database(self, name):
        try:
            self.cursor.execute(f"CREATE DATABASE {name}")
            self.connection.database = name
            self.current_db = name
            logging.info(f"Base de datos '{name}' creada.")
            return None
        except mysql.connector.Error as err:
            return str(err)

    def drop_database(self, name):
        try:
            self.cursor.execute(f"DROP DATABASE {name}")
            self.connection.commit()
            if self.current_db == name:
                self.current_db = None
            logging.info(f"Base de datos '{name}' eliminada.")
            return None
        except mysql.connector.Error as err:
            return str(err)

    def use_database(self, name):
        try:
            self.connection.database = name
            self.current_db = name
            return None
        except mysql.connector.Error as err:
            return str(err)

    def create_table(self, name, columns):
        columns_def = ', '.join(f"{col[0]} {col[1][0]}({col[1][1]})" if len(col[1]) > 1 else f"{col[0]} {col[1][0]}" for col in columns)
        query = f"CREATE TABLE {name} ({columns_def})"
        return self.execute(query)

    def drop_table(self, name):
        query = f"DROP TABLE IF EXISTS {name}"
        return self.execute(query)

    def table_exists(self, name):
        query = "SHOW TABLES LIKE %s"
        self.cursor.execute(query, (name,))
        return self.cursor.fetchone() is not None

    def column_exists(self, table, column):
        query = f"SHOW COLUMNS FROM {table} LIKE %s"
        self.cursor.execute(query, (column,))
        return self.cursor.fetchone() is not None

    def get_column_type(self, table, column):
        query = f"SHOW COLUMNS FROM {table} LIKE %s"
        self.cursor.execute(query, (column,))
        result = self.cursor.fetchone()
        if result:
            return result[1]
        return None
