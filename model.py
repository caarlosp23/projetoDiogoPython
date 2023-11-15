import pyodbc
from config import DB_CONFIG
from dataBase import DatabaseManager
from tkinter import messagebox
import datetime

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
        self.db_manager = DatabaseManager() 

    def carregar_contas(self):
        contas = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("select idContaFinanceira, NomeDaConta, Saldo, Descricao, DataCriacao from TBL_ContaFinanceira")
                rows = cursor.fetchall()

                for row in rows:
                    # Verifica se a DataCriacao é uma string
                    if isinstance(row.DataCriacao, str):
                        # Converte a string para um objeto datetime
                        row.DataCriacao = datetime.datetime.strptime(row.DataCriacao, '%Y-%m-%d')

                    # Formatando a DataCriacao para o formato dd-mm-aaaa
                    formatted_data_criacao = row.DataCriacao.strftime('%d-%m-%Y')

                    conta = {
                        'idContaFinanceira': row.idContaFinanceira,
                        'NomeDaConta': row.NomeDaConta,
                        'Saldo': row.Saldo,
                        'Descricao': row.Descricao,
                        'DataCriacao': formatted_data_criacao   
                    }

                    contas.append(conta)
        except Exception as e:
            print(f"Erro ao carregar contas: {e}")
        finally:
            self.db_manager.desconectar()

        return contas

    def inserir_conta(self, nome_conta, saldo, descricao, usuario_id):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute(
                    "EXEC Insert_ContaFinanceira @NomeDaConta=?, @Saldo=?, @Descricao=?, @Usuario_idUsuario=?",
                    (nome_conta, saldo, descricao, usuario_id)
                )
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao inserir conta: {e}")
        finally:
            self.db_manager.desconectar()
        
    def excluir_conta(self, id_conta):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("EXEC Delete_ContaFinanceira @idContaFinanceira=?", (id_conta,))
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao excluir conta: {e}")
        finally:
            self.db_manager.desconectar()

    def atualizar_conta(self, id_conta, nome_conta, saldo, descricao, usuario_id):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute(
                    "EXEC Update_ContaFinanceira @idContaFinanceira=?, @NomeDaConta=?, @Saldo=?, @Descricao=?, @DataCriacao=?, @Usuario_idUsuario=?",
                    (id_conta, nome_conta, saldo, descricao, usuario_id)
                )
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar conta: {e}")
        finally:
            self.db_manager.desconectar()


class CategoriaTransacao:
    def __init__(self, nome):
        self.nome = nome
        self.db_manager = DatabaseManager()  
    
    def inserir_categoria(self, descricao):
        try:
            # Verifica se a categoria já existe antes de inserir
            if not self.existe_categoria(descricao):
                if self.db_manager.conectar():
                    cursor = self.db_manager.conn.cursor()
                    cursor.execute("EXEC Insert_CategoriaTransacao @Descricao=?", (descricao,))
                    self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao inserir categoria: {e}")
        finally:
            self.db_manager.desconectar()

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
    
    def excluir_categoria(self, id_categoria):

        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("EXEC Delete_CategoriaTransacao @idCategoriaTransacao=?", (id_categoria,))
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao excluir categoria: {e}")
        finally:
            self.db_manager.desconectar()

    def atualizar_categoria(self, id_categoria, nova_descricao):

        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("EXEC Update_CategoriaTransacao @idCategoriaTransacao=?, @NovaDescricao=?", (id_categoria, nova_descricao))
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")
        finally:
            self.db_manager.desconectar()

    def existe_categoria(self, descricao):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT 1 FROM Tbl_CategoriaTransacao WHERE Descricao = ?", (descricao,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar existência da categoria: {e}")
            return False
        finally:
            self.db_manager.desconectar()

class Transacao:
    def __init__(self, descricao, valor, data, conta, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.conta = conta
        self.categoria = categoria