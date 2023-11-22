from view import LoginView, TelaPrincipalView, CadastroCategoriaView, CadastroTransacaoView, CadastroContaView, CadastroUsuarioView
from model import Usuario, ContaFinanceira, CategoriaTransacao, Transacao
import pyodbc
from config import DB_CONFIG
from tkinter import messagebox
from dataBase import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class LoginController:
    def __init__(self, root, db_config):
        self.view = LoginView(root)
        self.db_config = db_config
        self.loginService = Usuario("nome", "email", "senha")
        self.view.login_button.config(command=self.login)
        self.db_manager = DatabaseManager()
        self.tela_principal_controller = None  
        
    def login(self):
        usuario = self.view.login_entry.get()
        senha = self.view.senha_entry.get()

        if self.loginService.validar_usuario(usuario, senha):
          
            self.abrir_telaPrincipal(usuario)
        
        else:
            messagebox.showerror("Erro de Login", "Credenciais incorretas. Verifique seu usuário e senha.")

    def abrir_telaPrincipal(self,nome_usuario):
        self.view.root.withdraw() 
        root = tk.Tk()  
        self.tela_principal = TelaPrincipalController(root,nome_usuario)  
        root.mainloop()

class TelaPrincipalController:
    def __init__(self, root, nome_usuario):
        self.view = TelaPrincipalView(root, nome_usuario)
        self.view.controller = self
        self.contaService = ContaFinanceira("nome", "saldo_inicial", "usuario", "datacriacao")
        self.view.btn_categoria.config(command=self.abrir_categoria)
        self.view.btn_conta.config(command=self.abrir_conta)
        self.view.btn_transacao.config(command=self.abrir_transacao)
        self.inicializar_valores()
        self.totalizador_Contas()
        self.view.btn_filtrarPeriodo.config(command=self.entrada_periodo)
        self.categoriaService = CategoriaTransacao("nome")
        self.get_valoresGrafico()
        
    def inicializar_valores(self):
        # Carregar contas e saldos
        contas_saldos = self.carregar_contas_saldos()
        # Alimentar a Treeview com os dados
        self.view.alimentar_treeview(contas_saldos)
    
    def get_valoresGrafico(self):
        valoresEntrada = self.categoriaService.get_TopCategoriaEntrada()
        self.view.criar_grafico_top_categoria_entrada(valoresEntrada)
        valoresSaida = self.categoriaService.get_TopCategoriaSaida()
        self.view.criar_grafico_top_categoria_saida(valoresSaida)
    
    def totalizador_Contas(self):
        saldo = self.carregar_contas_saldos()
        saldos_conta = [x['SaldoFinal'] for x in saldo]
        
        soma_saldos = sum(saldos_conta)
        
        self.view.lbl_SaldoTotal.config(text=f"SALDO TOTAL : R$ {soma_saldos}")

    def entrada_periodo(self):
        dtaInicial = self.view.entry_data_inicial.get_date()
        dtaFinal = self.view.entry_data_final.get_date()
        
        dtaInicialFormat = dtaInicial.strftime('%Y-%m-%d')
        dtaFinalFormat = dtaFinal.strftime('%Y-%m-%d')

        entradaPeriodo = self.contaService.get_entradaPeriodo(dtaInicialFormat,dtaFinalFormat)
        self.inicializar_valores()
        self.saida_periodo()
        self.saldo_periodo()
        self.totalizador_Contas()
        self.get_valoresGrafico()
        self.view.lbl_EntradaValor.config(text=f"R$ {entradaPeriodo}")

    def saida_periodo(self):
        dtaInicial = self.view.entry_data_inicial.get_date()
        dtaFinal = self.view.entry_data_final.get_date()

        dtaInicialFormat = dtaInicial.strftime('%Y-%m-%d')
        dtaFinalFormat = dtaFinal.strftime('%Y-%m-%d')

        saidaPeriodo = self.contaService.get_SaidaPeriodo(dtaInicialFormat,dtaFinalFormat)
        self.view.lbl_SaidaValor.config(text=f"R$ {saidaPeriodo}")

    def saldo_periodo(self):
        dtaInicial = self.view.entry_data_inicial.get_date()
        dtaFinal = self.view.entry_data_final.get_date()

        dtaInicialFormat = dtaInicial.strftime('%Y-%m-%d')
        dtaFinalFormat = dtaFinal.strftime('%Y-%m-%d')

        entradaPeriodo = self.contaService.get_entradaPeriodo(dtaInicialFormat,dtaFinalFormat)
        saidaPeriodo = self.contaService.get_SaidaPeriodo(dtaInicialFormat,dtaFinalFormat)

        saldoPeriodo = entradaPeriodo - saidaPeriodo
        self.view.lbl_saldoPeriodoValor.config(text=f"R$ {saldoPeriodo}")
    
    def carregar_contas_saldos(self):
     
        return self.contaService.get_SaldoContas()

    def abrir_categoria(self):

        categoria_window = tk.Toplevel(self.view.root)
        categoria_window.title("Cadastro de Categoria")
        CadastroCategoriaController(categoria_window)
    
    def abrir_conta(self):

        categoria_window = tk.Toplevel(self.view.root)
        categoria_window.title("Cadastro de Conta")
        CadastroContaController(categoria_window)
    
    def abrir_transacao(self):

        categoria_window = tk.Toplevel(self.view.root)
        categoria_window.title("Cadastro de Transação")
        CadastroTransacaoController(categoria_window)

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
        descricao = self.view.entry_categoria.get().strip()  
        if descricao:  
            if not self.categoria_transacao.existe_categoria(descricao):  
                self.categoria_transacao.inserir_categoria(descricao)
                self.carregar_categorias()
              
                messagebox.showinfo("Sucesso", "Categoria salva com sucesso!")
                self.view.entry_categoria.delete("0", "end") 
            else:
                
                messagebox.showerror("Erro", "Esta categoria já existe.")
        else:
            
            messagebox.showerror("Erro", "A descrição da categoria não pode ser vazia.")

    def excluir_categoriaController(self):
        id_categoria = self.view.obter_id_selecionado()

       
        if id_categoria:
            
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta categoria?")
            if resposta:
                self.categoria_transacao.excluir_categoria(id_categoria)
                self.carregar_categorias()
                
                messagebox.showinfo("Sucesso", "Categoria excluída com sucesso!")
        else:
            
            messagebox.showwarning("Aviso", "Selecione uma categoria para excluir.")

    def atualizar_categoria(self):
        id_categoria = self.view.obter_id_selecionado()
        nova_descricao = self.view.entry_categoria.get()

       
        if nova_descricao.strip() == "":
            messagebox.showwarning("Aviso", "A descrição não pode estar vazia.")
            return

        self.categoria_transacao.atualizar_categoria(id_categoria, nova_descricao)
        self.carregar_categorias()

       
        messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")

    def exibir_descricao_selecionada(self, event):
        
        item_selecionado = self.view.tree.selection()
        if item_selecionado:
          
            descricao = self.view.tree.item(item_selecionado)['values'][1]
            self.view.entry_categoria.delete(0, tk.END)  
            self.view.entry_categoria.insert(0, descricao)    

class CadastroTransacaoController:
    def __init__(self, root):
        self.view = CadastroTransacaoView(root)
        self.categoriaTrans = CategoriaTransacao("Nome")
        self.comboConta = ContaFinanceira("nome", "saldo_inicial", "usuario", "datacriacao")
        contas = self.comboConta.carregar_contasCmbBox()
        self.comboContaValores = self.comboConta.carregar_contasCmbBox()
        combobox_categoria = self.categoriaTrans.get_categoriaComboBox()
        self.view.combobox_categoria['values'] = combobox_categoria
        self.view.cmbContas['values'] = contas
        self.view.btn_salvar.config(command = self.cadastrar_transacao)
        self.view.btn_excluir.config(command = self.excluir_transacao)
        self.view.btn_atualizar.config(command = self.atualizar_transacao)
        self.transacao_service = Transacao( "valor", "data", "conta", "categoria", "tipo_transacao")
        transacoes = self.transacao_service.carregar_transacoes()
        self.view.exibir_transacoes(transacoes)
        self.view.entry_tipoTrans['values'] = ['ENTRADA','SAIDA']
        
    def cadastrar_transacao(self):
        
        valor = float(self.view.entry_valor.get())  

        data_objeto = self.view.entry_dtaTransacao.get_date()
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        categoria = self.view.combobox_categoria.get()
        tipo_transacao = self.view.entry_tipoTrans.get()
        conta = self.view.cmbContas.get()

        
        self.transacao_service.create_transacao(tipo_transacao,valor,data_formatada,categoria,conta)

        transacoes = self.transacao_service.carregar_transacoes()
        self.view.exibir_transacoes(transacoes)
       
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        self.limpar_campos()
        self.comboConta.get_SaldoContas()

    def excluir_transacao(self):
       
        id_transacao = self.view.obter_id_selecionado()

        self.transacao_service.delete_transacao(id_transacao)

        transacoes = self.transacao_service.carregar_transacoes()
        self.view.exibir_transacoes(transacoes)

        messagebox.showinfo("Sucesso", "Transação excluida com sucesso!")
        self.limpar_campos()

    def limpar_campos(self):
   
        self.view.entry_valor.delete(0, tk.END)

        self.view.combobox_categoria.set('')
        
        self.view.cmbContas.set('')

        self.view.entry_tipoTrans.set('')

    def atualizar_transacao(self):
      
        id_transacao =  self.view.obter_id_selecionado()
        
        valor = float(self.view.entry_valor.get())  
        data_objeto = self.view.entry_dtaTransacao.get_date()
        data_formatada = data_objeto.strftime('%Y-%m-%d')
        categoria = self.view.combobox_categoria.get()
        tipo_transacao = self.view.entry_tipoTrans.get()
        conta = self.view.cmbContas.get()

        self.transacao_service.update_transacao(id_transacao,tipo_transacao,valor,data_formatada,categoria,conta)

        transacoes = self.transacao_service.carregar_transacoes()
        self.view.exibir_transacoes(transacoes)

        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        self.limpar_campos()

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

        nome = self.view.entry_Conta.get().strip()
        saldo = self.view.entry_ContaSaldo.get().strip()
        descricao = self.view.entry_ContaDesc.get().strip()

        
        if not nome or not saldo or not descricao:
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar.")
            return

      
        if self.contaFinanceira.conta_existente(nome):
            messagebox.showerror("Erro", "Já existe uma conta com esse nome.")
            return

        
        self.contaFinanceira.inserir_conta(nome, saldo, descricao, 1)

       
        self.carregar_contas()

       
        self.view.entry_Conta.delete(0, "end")
        self.view.entry_ContaSaldo.delete(0, "end")
        self.view.entry_ContaDesc.delete(0, "end")

        
        messagebox.showinfo("Sucesso", "Conta salva com sucesso!")
        

    def atualizar_conta(self):
        id_conta = self.view.id_selecionado
        nome = self.view.entry_Conta.get().strip()
        saldo = self.view.entry_ContaSaldo.get().strip()
        descricao = self.view.entry_ContaDesc.get().strip()

       
        if nome and saldo and descricao: 
                self.contaFinanceira.atualizar_conta(id_conta, nome, saldo, descricao)
                self.carregar_contas()

                self.view.entry_Conta.delete(0, "end")
                self.view.entry_ContaSaldo.delete(0, "end")
                self.view.entry_ContaDesc.delete(0, "end")

                messagebox.showinfo("Sucesso", "Conta atualizada com sucesso!")
        else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
    
    def excluir_conta(self):
       
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir esta conta?")

        if resposta == "yes":
               

                id_conta = self.view.id_selecionado
        
                self.contaFinanceira.excluir_conta(id_conta)

                
                self.view.entry_Conta.delete(0, "end")
                self.view.entry_ContaSaldo.delete(0, "end")
                self.view.entry_ContaDesc.delete(0, "end")

                
                self.carregar_contas()

                
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
        else:
           
            messagebox.showerror("Erro", "Selecione uma conta para excluir.")    

class CadastroUsuarioController:
    def __init__(self, root):
        self.view = CadastroUsuarioView(root)
        #self.view.botao_cadastrar.config(command=self.cadastrar_usuario)
     
    #def cadastrar_usuario(self):