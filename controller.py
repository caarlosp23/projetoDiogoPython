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
             self.view.root.destroy()
             
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
        self.view.root.withdraw() 
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
    
    # def fechar_projeto(self):
    #     self.view.root.quit()
        
class TelaPrincipalController:
    def __init__(self, root, nome_usuario):
        self.view = TelaPrincipalView(root, nome_usuario)
        self.view.controller = self
        
    #def listar_topEntrada(self):
    #def listar_topSaida(self):
    #def totalizarSaldoConta(self):
    #def totalizarSaldoContaPeriodo(self):
    #def totalEntradaPeriodo(self):
    #def totalSaidaPeriodo(self):

    def __init__(self, root):
        self.view = CadastroCategoriaView(root)
      
class CadastroCategoriaController:
    def __init__(self, root):
        self.view = CadastroCategoriaView(root)
        self.categoria_transacao = CategoriaTransacao("Nome da Categoria")
        categorias = self.categoria_transacao.carregar_categorias()
        self.view.exibir_categorias(categorias)
        self.view.btn_salvar.config(command = self.cadastrar_categoria)
        self.view.btn_excluir.config(command = self.excluir_categoriaController)
        self.view.btn_atualizar.config(command = self.atualizar_categoria)
        self.view.tree.bind("<ButtonRelease-1>", self.exibir_descricao_selecionada)

    def carregar_categorias(self):
        categorias = self.categoria_transacao.carregar_categorias()
        self.view.exibir_categorias(categorias)

    def cadastrar_categoria(self):
        descricao = self.view.entry_categoria.get().strip()  # Obter descrição da categoria e remover espaços em branco
        if descricao:  # Verificar se a descrição não é vazia
            if not self.categoria_transacao.existe_categoria(descricao):  # Verificar se a categoria já existe
                self.categoria_transacao.inserir_categoria(descricao)
                self.carregar_categorias()
                # Exibir messagebox de sucesso
                messagebox.showinfo("Sucesso", "Categoria salva com sucesso!")
                self.view.entry_categoria.delete("0", "end")  # Limpar o Entry após salvar
            else:
                # Exibir messagebox de erro se a categoria já existir
                messagebox.showerror("Erro", "Esta categoria já existe.")
        else:
            # Exibir messagebox de erro se a descrição estiver vazia
            messagebox.showerror("Erro", "A descrição da categoria não pode ser vazia.")

    def excluir_categoriaController(self):
        id_categoria = self.view.obter_id_selecionado()

        # Verificar se um item está selecionado
        if id_categoria:
            # Perguntar ao usuário se tem certeza
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta categoria?")
            if resposta:
                self.categoria_transacao.excluir_categoria(id_categoria)
                self.carregar_categorias()
                # Exibir messagebox de sucesso
                messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
        else:
            # Nenhum item selecionado, exiba uma mensagem de aviso
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir.")

    def atualizar_categoria(self):
        id_categoria = self.view.obter_id_selecionado()
        nova_descricao = self.view.entry_categoria.get()

        # Verifica se a descrição não está vazia antes de prosseguir
        if nova_descricao.strip() == "":
            messagebox.showwarning("Aviso", "A descrição não pode estar vazia.")
            return

        self.categoria_transacao.atualizar_categoria(id_categoria, nova_descricao)
        self.carregar_categorias()

        # Exibe uma mensagem de sucesso
        messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")

    def exibir_descricao_selecionada(self, event):
        # Função chamada quando um item na Treeview é clicado
        item_selecionado = self.view.tree.selection()
        if item_selecionado:
            # Obtém a descrição do item selecionado e a exibe no entry
            descricao = self.view.tree.item(item_selecionado)['values'][1]
            self.view.entry_categoria.delete(0, tk.END)  # Limpa o entry
            self.view.entry_categoria.insert(0, descricao)  # Insere a descrição no entry
        
class CadastroTransacaoController:
    def __init__(self, root):
        self.view = CadastroTransacaoView(root)
        
  
    #def listar_transacao(self):
    #def cadastrar_transacao(self):
    #def atualizar_transacao(self):
    #def excluir_transacao(self):

class CadastroContaController:
    def __init__(self, root):
        self.view = CadastroContaView(root)
        self.contaFinanceira = ContaFinanceira("nome","saldo","usuario","datacriacao")
        contas = self.contaFinanceira.carregar_contas()
        self.view.exibir_contas(contas)


        self.view.btn_salvarConta.config(command = self.salvar_conta)
        self.view.btn_excluirConta.config(command = self.excluir_conta)
        self.view.btn_atualizarConta.config(command = self.atualizar_conta)

    def carregar_contas(self):
        contas = self.contaFinanceira.carregar_contas()
        self.view.exibir_contas(contas)
    
    def salvar_conta(self):
        # Chamar método do model para salvar a conta
        nome = self.view.entry_Conta.get()
        saldo = self.view.entry_ContaSaldo.get()
        descricao = self.view.entry_ContaDesc.get()
        
        self.contaFinanceira.inserir_conta(nome, saldo, descricao,1)  # Substitua 1 pelo ID do usuário

    def atualizar_conta(self, id_conta, nome_conta, saldo, descricao, data_criacao):
        # Chamar método do model para atualizar a conta
        self.contaFinanceira.atualizar_conta(id_conta, nome_conta, saldo, descricao, data_criacao, usuario_id=1)  # Substitua 1 pelo ID do usuário
    
    def excluir_conta(self, id_conta):
        # Chamar método do model para excluir a conta
        self.model.excluir_conta(id_conta)
    
class CadastroUsuarioController:
    def __init__(self, root):
        self.view = CadastroUsuarioView(root)
        #self.view.botao_cadastrar.config(command=self.cadastrar_usuario)
     
    #def cadastrar_usuario(self):
   
       
