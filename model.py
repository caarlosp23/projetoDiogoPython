from config import DB_CONFIG
from dataBase import DatabaseManager
import datetime

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.db_manager = DatabaseManager() 

    
    def validar_usuario(self, login, senha):
        conn = None
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                query = "SELECT idUsuario FROM Tbl_Usuario WHERE Login = ? AND Senha = ?"
                cursor.execute(query, (login, senha))
                resultado = cursor.fetchone()
                if resultado:
                    return True
                else:
                    return False
            
            self.db_manager.desconectar() 

        except Exception as e:
            print(f"Erro ao validar login: {e}")
            return False
        finally:
            if self.db_manager.conn:
                 self.db_manager.desconectar()   

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

    def atualizar_conta(self, id_conta, nome, saldo, descricao):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute(
                    "EXEC Update_ContaFinanceira @idContaFinanceira=?, @NomeDaConta=?, @Saldo=?, @Descricao=?",
                    (id_conta, nome, saldo, descricao)
                )
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar conta: {e}")
        finally:
            self.db_manager.desconectar()

    def conta_existente(self, nome_conta):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                query = "SELECT 1 FROM TBL_ContaFinanceira WHERE NomeDaConta = ?"
                cursor.execute(query, (nome_conta,))
                resultado = cursor.fetchone()
                return resultado is not None
        except Exception as e:
            print(f"Erro ao verificar conta existente: {e}")
        finally:
            if self.db_manager.conn:
                self.db_manager.desconectar()
        return False

    def carregar_contasCmbBox(self):  
        contas = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("select  NomeDaConta from TBL_ContaFinanceira")
                rows = cursor.fetchall()

                for row in rows:
                    conta = row[0]  # Assume que a coluna NomeDaConta é a primeira coluna no resultado da consulta
                    contas.append(conta)

        except Exception as e:
            print(f"Erro ao carregar contas: {e}")
        finally:
            self.db_manager.desconectar()

        return contas

    def get_SaldoContas(self):
        saldos_contas = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()

                # Chamar a função no banco de dados para obter saldos
                cursor.execute("SELECT * FROM FN_CalcularSaldoPorConta()")

                rows = cursor.fetchall()

                for row in rows:
                    saldo_conta = {
                        'idContaFinanceira': row.idContaFinanceira,
                        'NomeDaConta': row.NomeDaConta,
                        'SaldoFinal': row.SaldoFinal,
                    }

                    saldos_contas.append(saldo_conta)
        except Exception as e:
            print(f"Erro ao obter saldos das contas: {e}")
        finally:
            self.db_manager.desconectar()

        return saldos_contas

    def get_entradaPeriodo(self, dtaInicial, dtaFinal):
        try:
            if self.db_manager.conectar():
                    cursor = self.db_manager.conn.cursor()
                    sql_query = "SELECT somaperiodo FROM [dbo].[FN_EntradaPorPeriodo](?, ?)"
                    cursor.execute(sql_query, (dtaInicial, dtaFinal))
                    resultado_entrada = cursor.fetchone()
                    if resultado_entrada:
                         # Converter valor decimal para ponto flutuante
                         soma_periodo = float(resultado_entrada[0])
                         print(soma_periodo)
                         return soma_periodo
                    else:
                         print("A função não retornou resultados.")
                         return None
                    
        except Exception as e:
            print(f"Erro ao obter a soma de entradas no período: {e}")
        finally:
            self.db_manager.desconectar()

        return 0  # Retorna 0 em caso de erro
    
    def get_SaidaPeriodo(self, dtaInicial, dtaFinal):
        try:
            if self.db_manager.conectar():
                    cursor = self.db_manager.conn.cursor()
                    sql_query = "SELECT somaperiodo FROM [dbo].[FN_SaidaPorPeriodo](?, ?)"
                    cursor.execute(sql_query, (dtaInicial, dtaFinal))
                    resultado_entrada = cursor.fetchone()
                    if resultado_entrada:
                         # Converter valor decimal para ponto flutuante
                         soma_periodo = float(resultado_entrada[0])
                         print(soma_periodo)
                         return soma_periodo
                    else:
                         print("A função não retornou resultados.")
                         return None
                    
        except Exception as e:
            print(f"Erro ao obter a soma de saida no período: {e}")
        finally:
            self.db_manager.desconectar()

        return 0  # Retorna 0 em caso de erro
    
    def get_saldoPeriodo(self, dtaInicial, dtaFinal):
        try:
            if self.db_manager.conectar():
                    cursor = self.db_manager.conn.cursor()
                    sql_query = "selecT sum(SaldoFinal) as SaldoPeriodo From [dbo].[FN_CalcularSaldoPorPeriodo](?, ?)"
                    cursor.execute(sql_query, (dtaInicial, dtaFinal))
                    resultado_entrada = cursor.fetchone()
                    if resultado_entrada:
                         # Converter valor decimal para ponto flutuante
                         saldo = float(resultado_entrada[0])
                        
                         return saldo
                    else:
                         print("A função não retornou resultados.")
                         return None
                    
        except Exception as e:
            print(f"Erro ao obter a soma de saldo no período: {e}")
        finally:
            self.db_manager.desconectar()

        return 0  # Retorna 0 em caso de erro

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
    
    def get_categoriaComboBox(self):
        categorias = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT descricao FROM Tbl_CategoriaTransacao")
                rows = cursor.fetchall()
                for row in rows:
                    categoria = row[0]  # Assume que a coluna descricao é a primeira coluna no resultado da consulta
                    categorias.append(categoria)

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

    def get_TopCategoriaEntrada(self):
        topCatEntrada = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()

                # Chamar a função no banco de dados para obter categorias
                cursor.execute("selecT* from dbo.TopEntradaCategoria()")

                rows = cursor.fetchall()
                for row in rows:
                    categoria = {
                        'Categoria': row.Categoria,  # Substitua pelo nome real da primeira coluna
                        'Valor': row.Valor   # Substitua pelo nome real da segunda coluna
                    }
                    topCatEntrada.append(categoria)

        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
        finally:
            self.db_manager.desconectar()

        return topCatEntrada
    
    def get_TopCategoriaSaida(self):
        topCatSaida = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()

                # Chamar a função no banco de dados para obter categorias
                cursor.execute("selecT* from dbo.TopSaidaCategoria()")

                rows = cursor.fetchall()
                for row in rows:
                    categoria = {
                        'Categoria': row.Categoria,  # Substitua pelo nome real da primeira coluna
                        'Valor': row.Valor   # Substitua pelo nome real da segunda coluna
                    }
                    topCatSaida.append(categoria)

        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
        finally:
            self.db_manager.desconectar()

        return topCatSaida

class Transacao:
    def __init__(self, descricao, valor, data, conta, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.conta = conta
        self.categoria = categoria
        self.db_manager = DatabaseManager()

    def create_transacao(self, tipoTransacao, valor, data, categoria, conta):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()

                    # Executar a procedure
                cursor.execute(
                    "EXEC Insert_Transacao @TipoTransacao=?, @Valor=?, @DataTransacao=?, @CategoriaTransacao_Descricao=?, @ContaFinanceira_Descricao=?",
                    (tipoTransacao, valor,data,categoria,conta)
                )
                print(data)
                
                self.db_manager.conn.commit()

        except Exception as e:
            print(f"Erro ao criar transação: {e}")
        finally:
            self.db_manager.desconectar()

    def update_transacao(self, id,tipoTransacao, valor, data, categoria, conta):
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute(
                "EXEC Update_Transacao @idTransacao=?, @TipoTransacao=?, @Valor=?, @DataTransacao=?, @CategoriaTransacao_Descricao=?, @ContaFinanceira_Descricao=?",
                (id, tipoTransacao,valor,data,categoria,conta)
                )
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar transação: {e}")
        finally:
            self.db_manager.desconectar()

    def delete_transacao(self, id_transacao):

        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("DELETE FROM TBL_Transacao WHERE idTransacao=?", (id_transacao,))
                self.db_manager.conn.commit()
        except Exception as e:
            print(f"Erro ao excluir transação: {e}")
        finally:
            self.db_manager.desconectar()

    def carregar_transacoes(self):
        transacao = []
        try:
            if self.db_manager.conectar():
                cursor = self.db_manager.conn.cursor()
                cursor.execute("select idtransacao, tipotransacao, valor,datatransacao,cat.descricao as categoria, conta.nomedaconta as conta from TBL_Transacao trans inner join TBL_CategoriaTransacao cat on trans.CategoriaTransacao_idCategoriaTransacao = cat.idcategoriatransacao inner join TBL_ContaFinanceira conta on trans.ContaFinanceira_idContaFinanceira = conta.idContaFinanceira")
                rows = cursor.fetchall()
                transacao = [{'idtransacao': row.idtransacao, 'tipotransacao': row.tipotransacao, 'valor': row.valor,'datatransacao': row.datatransacao,'categoria': row.categoria,'conta': row.conta} for row in rows]
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
        finally:
                self.db_manager.desconectar()

        return transacao