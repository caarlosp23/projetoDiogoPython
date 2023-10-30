from view import LoginView, TelaPrincipalView, CadastroCategoriaView, CadastroTransacaoView, CadastroContaView, CadastroUsuarioView
from model import Usuario, ContaFinanceira, CategoriaTransacao, Transacao
import pyodbc
from config import DB_CONFIG
from tkinter import messagebox
from dataBase import *
import tkinter as tk

class LoginController:
    def __init__(self, root, db_config):
        self.view = LoginView(root)
        self.db_config = db_config
        self.view.login_button.config(command=self.login)
        self.db_manager = DatabaseManager()
        self.tela_principal_controller = None  

    def login(self):
    
        usuario = self.view.login_entry.get()
        senha = self.view.senha_entry.get()

        if self.validar_usuario(usuario, senha):
             self.abrir_telaPrincipal(usuario)
             self.view.root.quit()
            # O login foi bem-sucedido, você pode redirecionar para a próxima tela ou realizar outras ações aqui
            
        else:
            # # O login falhou, exiba uma mensagem de erro ou realize outras ações necessárias
            messagebox.showerror("Erro de Login", "Credenciais incorretas. Verifique seu usuário e senha.")

    def login(self):
        usuario = self.view.login_entry.get()
        senha = self.view.senha_entry.get()

        if self.validar_usuario(usuario, senha):
            # Abra a tela principal diretamente na mesma janela
            self.abrir_telaPrincipal(usuario)
            # Não é mais necessário destruir a janela de login
        else:
            messagebox.showerror("Erro de Login", "Credenciais incorretas. Verifique seu usuário e senha.")

    def abrir_telaPrincipal(self, nome_usuario):
        # Em vez de criar uma nova janela com tk.Tk(), crie o controlador da tela principal na janela existente
        self.tela_principal_controller = TelaPrincipalController(self.view.root, nome_usuario)

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
    
    def abrir_telaPrincipal(self,nome_usuario):
         
        self.view.root.withdraw()  # Oculta a janela de login
        root = tk.Tk()  # Crie uma nova janela principal
        self.tela_principal = TelaPrincipalView(root,nome_usuario)  # Crie a Tela Principal
        root.mainloop() # Crie a Tela Principal
    
    def fechar_projeto(self):
        self.view.root.quit()
        
        
        

class TelaPrincipalController:
    def __init__(self, root, nome_usuario):
        self.view = TelaPrincipalView(root, nome_usuario)
        
    #def listar_topEntrada(self):
    #def listar_topSaida(self):
    #def totalizarSaldoConta(self):
    #def totalizarSaldoContaPeriodo(self):
    #def totalEntradaPeriodo(self):
    #def totalSaidaPeriodo(self):
       
class CadastroCategoriaController:
    def __init__(self, root):
        self.view = CadastroCategoriaView(root)
        #self.view.botao_cadastrar.config(command=self.cadastrar_categoria)
        
        #self.view.botao_cadastrar.config(command=self.cadastrar_categoria)
        self.categoria_model = CategoriaTransacao('teste')
        #self.carregar_categorias()  # Carregar as categorias ao inicializar

    def carregar_categorias(self):
        categorias = self.categoria_model.carregar_categorias()
        self.view.exibir_categorias(categorias)

  

    #def listar_categoria(self):
    #def cadastrar_categoria(self):
    #def atualizar_categoria(self):
    #def excluir_categoria(self):
        
class CadastroTransacaoController:
    def __init__(self, root):
        self.view = CadastroTransacaoView(root)
        self.view.botao_cadastrar.config(command=self.cadastrar_transacao)

    #def listar_transacao(self):
    #def cadastrar_transacao(self):
    #def atualizar_transacao(self):
    #def excluir_transacao(self):

class CadastroContaController:
    def __init__(self, root):
        self.view = CadastroContaView(root)
        #self.view.botao_cadastrar.config(command=self.cadastrar_conta)

    #def listar_conta(self):    
    #def cadastrar_conta(self):
    #def atualizar_conta(self):
    #def excluir_conta(self):
        

class CadastroUsuarioController:
    def __init__(self, root):
        self.view = CadastroUsuarioView(root)
        #self.view.botao_cadastrar.config(command=self.cadastrar_usuario)
     
    #def cadastrar_usuario(self):
   
       
