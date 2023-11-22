import pyodbc
from config import DB_CONFIG

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def conectar(self):
        try:
            self.conn = pyodbc.connect(
                f"DRIVER=SQL Server;SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
            )
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def desconectar(self):
        if self.conn:
            self.conn.close()
            self.conn = None

