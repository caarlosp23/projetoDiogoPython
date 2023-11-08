import pyodbc
from config import DB_CONFIG
from dataBase import DatabaseManager

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

class ContaFinanceira:
    def __init__(self, nome, saldo_inicial, usuario, datacriacao):
        self.nome = nome
        self.saldo = saldo_inicial
        self.usuario = usuario
        self.datacriacao = datacriacao

class CategoriaTransacao:
    def __init__(self, nome):
        self.nome = nome
        self.db_manager = DatabaseManager()  

    def carregar_categorias(self):
        categorias = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("selecT idcategoriatransacao, descricao from Tbl_CategoriaTransacao")
                rows = cursor.fetchall()
                categorias = [{'idcategoriatransacao': row.idcategoriatransacao, 'descricao': row.descricao} for row in rows]
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
        finally:
                self.db_manager.desconectar()

        return categorias

class Transacao:
    def __init__(self, descricao, valor, data, conta, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.conta = conta
        self.categoria = categoria