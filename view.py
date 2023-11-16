import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import PhotoImage
from tkinter import ttk
from controller import *
from model import CategoriaTransacao
from tkcalendar import Calendar, DateEntry


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        # Define o tamanho da tela como 900x570
        width = 900
        height = 570
        self.center_window(width, height)
        # Define a cor de fundo da tela para "#008BD6"
        self.root.configure(bg="#008BD6")
        # Cria campos de entrada (inputs) para login e senha
        self.create_login_fields()
        # Cria o botão de login
        self.create_login_button()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_login_fields(self):
        rect_width = 300
        rect_height = 200
        rounded_rect = Image.new("RGBA", (rect_width, rect_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(rounded_rect)
        draw.rounded_rectangle((0, 0, rect_width, rect_height), radius=20, fill="#FFFFFF")
        photo = ImageTk.PhotoImage(rounded_rect)
        label = tk.Label(self.root, image=photo, bg="#008BD6")
        label.place(relx=0.5, rely=0.5, anchor="center")

        money_label = tk.Label(self.root, text="MONEY", font=("Helvetica", 24), bg="#008BD6", fg="white")
        money_label.place(relx=0.5, rely=0.25, anchor="center")

        self.login_entry = tk.Entry(self.root, font=("Helvetica", 12), justify="center", fg="gray")
        self.login_entry.insert(0, "Usuário")
        self.login_entry.bind("<FocusIn>", self.on_entry_click)
        self.login_entry.bind("<FocusOut>", self.on_entry_leave)
        self.login_entry.place(relx=0.5, rely=0.42, anchor="center")

        self.senha_entry = tk.Entry(self.root, font=("Helvetica", 12), justify="center", show="*", fg="gray")
        self.senha_entry.insert(0, "Senha")
        self.senha_entry.bind("<FocusIn>", self.on_entry_click)
        self.senha_entry.bind("<FocusOut>", self.on_entry_leave)
        self.senha_entry.place(relx=0.5, rely=0.50, anchor="center")

    def create_login_button(self):
        self.login_button = tk.Button(self.root, text="LOGIN", font=("Helvetica", 12), bg="#008BD6", fg="white")
        self.login_button.place(relx=0.5, rely=0.60, anchor="center")

    def on_entry_click(self, event):
        if self.login_entry.get() == "Usuário":
            self.login_entry.delete(0, "end")
            self.login_entry.configure(fg="black")

    def on_entry_leave(self, event):
        if self.login_entry.get() == "":
            self.login_entry.insert(0, "Usuário")
            self.login_entry.configure(fg="gray")
        
class TelaPrincipalView:
    def __init__(self, root, nome_usuario):
        self.root = root
        self.root.title("Money")
        self.root.configure(bg="#008BD6")
        self.create_widgets(nome_usuario)
        self.center_window(900,570)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_projeto)
        
    def fechar_projeto(self):
        self.root.quit()

    def create_widgets(self, nome_usuario):
        white_rectangle = tk.Canvas(self.root, bg="#FFFFFF", width=900, height=465)
        white_rectangle.place(relx=0, rely=1, anchor="sw")

         # Adicione o nome do usuário ao rótulo de boas-vindas
        lbl_bemvindo = tk.Label(self.root, text=f"BEM VINDO, {nome_usuario}", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_bemvindo.place(relx=0.17, rely=0.12, anchor="center")

        cadastrar_dropdown = tk.Menubutton(self.root, text="CADASTRAR", font=("Helvetica", 12), bg="#008BD6", fg="white")
        cadastrar_dropdown.place(relx=0.75, rely=0.12, anchor="center")

        cadastrar_menu = tk.Menu(cadastrar_dropdown)
        cadastrar_dropdown.configure(menu=cadastrar_menu)
  
        opcoes_cadastro = ["CATEGORIA", "CONTA", "USUÁRIO"]
        for opcao in opcoes_cadastro:
            cadastrar_menu.add_command(label=opcao, command=lambda o=opcao: self.abrir_cadastro(o))

    

       
        btn_financeiro = tk.Menubutton(self.root, text="TRANSAÇÕES", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_financeiro.place(relx=0.90, rely=0.12, anchor="center")
       
        menu = tk.Menu(btn_financeiro, tearoff=0)
        menu.add_command(label="Cadastrar Transação", command=self.abrir_transacao)
        btn_financeiro.config(menu=menu)

        label_periodo = tk.Label(self.root, text="PERÍODO", font=("Helvetica", 16), bg="#FFFFFF" ,fg="black")
        label_periodo.place(relx=0.05, rely=0.28, anchor="w")

        entry_data_inicial = tk.Entry(self.root, font=("Helvetica", 12),width=9)
        entry_data_inicial.place(relx=0.02, rely=0.35, anchor="w")
        entry_data_inicial.insert(0, "dd/mm/aaaa")

        entry_data_final = tk.Entry(self.root, font=("Helvetica", 12),width=9)
        entry_data_final.place(relx=0.12, rely=0.35, anchor="w")
        entry_data_final.insert(0, "dd/mm/aaaa")

        btn_filtrarPeriodo = tk.Button(self.root, text="Filtrar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_filtrarPeriodo.place(relx=0.08, rely=0.45, anchor="w")

        # Adicione um botão para atualizar o saldo (se necessário)
        botao_atualizar_saldo = tk.Button(self.root, text="Atualizar Saldo", font=("Helvetica", 12), bg="#008BD6", fg="white", command=self.atualizar_saldo)
        botao_atualizar_saldo.place(relx=0.05, rely=0.78, anchor="w")

        # Crie o rótulo de saldo inicialmente com um valor padrão
        self.label_saldo = tk.Label(self.root, text=f"SALDO: R$ 0.00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.label_saldo.place(relx=0.02, rely=0.7, anchor="w")

        #Saldo
        self.lbl_saldoPeriodo = tk.Label(self.root, text="SALDO PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_saldoPeriodo.place(relx=0.25, rely=0.28, anchor="w")

        self.lbl_saldoPeriodoValor = tk.Label(self.root, text="R$500,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_saldoPeriodoValor.place(relx=0.29, rely=0.35, anchor="w")

        #Entrada
        self.lbl_Entrada = tk.Label(self.root, text="ENTRADA PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_Entrada.place(relx=0.49, rely=0.28, anchor="w")

        self.lbl_EntradaValor = tk.Label(self.root, text="R$500,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_EntradaValor.place(relx=0.55, rely=0.35, anchor="w")

        #Saida
        self.lbl_Saida = tk.Label(self.root, text="SAIDA PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_Saida.place(relx=0.75, rely=0.28, anchor="w")

        self.lbl_SaidaValor = tk.Label(self.root, text="R$500,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_SaidaValor.place(relx=0.80, rely=0.35, anchor="w")

    def abrir_cadastro(self, opcao):
        if opcao == "CATEGORIA":
            # Implemente a lógica para abrir a tela de cadastro de categorias
            categoria_window = tk.Toplevel(self.root)
            categoria_window.title("Cadastro de Categoria")
            CadastroCategoriaView(categoria_window)
        # Inicialize o controlador da tela de cadastro de categoria
        elif opcao == "CONTA":
            categoria_window = tk.Toplevel(self.root)
            CadastroContaView(categoria_window)
            # Implemente a lógica para abrir a tela de cadastro de contas
         
        elif opcao == "USUÁRIO":

            categoria_window = tk.Toplevel(self.root)
            CadastroUsuarioView(categoria_window)
            # Implemente a lógica para abrir a tela de cadastro de usuários
            
    

    def abrir_transacao(self):
        transacao_window = tk.Toplevel(self.root)
        transacao_window.title("Transações")
        CadastroTransacaoView(transacao_window)

    def atualizar_saldo(self):
        # Aqui você pode implementar a lógica para atualizar o saldo
        # Substitua o valor a seguir pelo saldo real
        saldo = 1000.00  # Exemplo de saldo
        self.label_saldo.config(text=f"SALDO: R$ {saldo:.2f}")

    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")    

    def create_login_fields(self, nome_usuario):
        # Adicione o nome do usuário ao rótulo
        lbl_bemvindo = tk.Label(self.root, text=f"BEM VINDO, {nome_usuario}", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_bemvindo.place(relx=0.17, rely=0.12, anchor="center") 

class CadastroCategoriaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Categoria")
        self.root.configure(bg="#008BD6")
        self.center_window(900, 570)
        self.create_widgets()

    def exibir_janela(self):
        categoria_window = tk.Toplevel(self.root)
        categoria_window.title("Cadastro de Categoria")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        white_rectangle = tk.Canvas(self.root, bg="#FFFFFF", width=900, height=465)
        white_rectangle.place(relx=0, rely=1, anchor="sw")
        
        ret_cinza = tk.Canvas(self.root, bg="#D9D9D9", width=390, height=425)
        ret_cinza.place(relx=0.03, rely=0.22, anchor="nw")
        
        lbl_cadCategoria = tk.Label(self.root, text=f"CADASTRO DE CATEGORIA", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_cadCategoria.place(relx=0.5, rely=0.10, anchor="center")
        
        self.entry_categoria = tk.Entry(self.root, font=("Helvetica", 12),width=15 ,highlightthickness=1, highlightbackground="black")
        self.entry_categoria.place(relx=0.7, rely=0.25, anchor="w")

        lbl_cadCategoria = tk.Label(self.root, text=f"CATEGORIA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadCategoria.place(relx=0.58, rely=0.25, anchor="w")

        self.btn_salvar = tk.Button(self.root, text="Salvar", font=("Helvetica", 12), bg="#008BD6", fg="white",command=self.salvar_categoria)
        self.btn_salvar.place(relx=0.64, rely=0.35, anchor="w")

    # Botão Atualizar
        self.btn_atualizar = tk.Button(self.root, text="Atualizar", font=("Helvetica", 12), bg="#008BD6", fg="white", command=self.atualizar_categoria)
        self.btn_atualizar.place(relx=0.71, rely=0.35, anchor="w")

    # Botão Excluir
        self.btn_excluir = tk.Button(self.root, text="Excluir", font=("Helvetica", 12), bg="#008BD6", fg="white", command=self.excluir_categoria)
        self.btn_excluir.place(relx=0.80, rely=0.35, anchor="w")

        self.tree = ttk.Treeview(self.root, columns=("idcategoriatransacao", "Categoria"), show="headings")
        self.tree.heading("idcategoriatransacao", text="ID")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.place(relx=0.03, rely=0.22, anchor="nw", width=390, height=425)

        self.tree.tag_configure("center", anchor="center")

# Aplicar a tag "center" às colunas
        # self.tree.heading("idcategoriatransacao", text="ID Categoria", anchor="center")
        # self.tree.heading("Categoria", text="Categoria", anchor="center")

        self.tree.column("idcategoriatransacao", width=30)
        self.tree.column("Categoria", width=250)
    
    def exibir_categorias(self, categorias):
    # Limpar qualquer conteúdo anterior no retângulo cinza
        self.tree.delete(*self.tree.get_children())
        for categoria in categorias:
        # Insira uma tupla contendo o ID e a descrição
            self.tree.insert("", "end", values=(categoria['idcategoriatransacao'], categoria['descricao']))
    
    def salvar_categoria(self):
        # Lógica para obter dados do Entry e chamar a stored procedure de inserção
        descricao = self.entry_categoria.get()  # Obter descrição da categoria
        self.categoria_transacao.inserir_categoria(descricao)
        self.atualizar_lista_categorias()
        
    
    def atualizar_lista_categorias(self):
        # Lógica para obter dados da tabela e exibir na Treeview
        categorias = self.categoria_service.obter_todas_categorias()
        self.exibir_categorias(categorias)

    def atualizar_categoria(self):
    # Lógica para obter dados do Entry e chamar a stored procedure de atualização
        self.categoria_transacao.atualizar_categoria()
        self.atualizar_lista_categorias()

    def excluir_categoria(self):
        # Lógica para obter dados do Entry e chamar a stored procedure de exclusão
        self.categoria_transacao.excluir_categoriaController()
        self.atualizar_lista_categorias()
    
    def obter_id_selecionado(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            return self.tree.item(item_selecionado)['values'][0]
        return None

class CadastroTransacaoView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Transação")
        self.root.configure(bg="#008BD6")
        self.center_window(900, 570)
        self.create_widgets()
                 
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        white_rectangle = tk.Canvas(self.root, bg="#FFFFFF", width=900, height=465)
        white_rectangle.place(relx=0, rely=1, anchor="sw")
        
        ret_cinza = tk.Canvas(self.root, bg="#D9D9D9", width=390, height=425)
        ret_cinza.place(relx=0.03, rely=0.22, anchor="nw")
        
        lbl_cadTransacao = tk.Label(self.root, text=f"CADASTRO DE TRANSAÇÃO", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_cadTransacao.place(relx=0.5, rely=0.10, anchor="center")
        
        lbl_cadTipo = tk.Label(self.root, text=f"TIPO", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadTipo.place(relx=0.58, rely=0.25, anchor="w")
        # entry_tipo = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        # entry_tipo.place(relx=0.78, rely=0.25, anchor="w")

        cmbTipo = ['ENTRADA', 'SAIDA']
        self.cmbTipo = ttk.Combobox(self.root, values=cmbTipo, font=("Helvetica", 12), width=10)
        self.cmbTipo.place(relx=0.78, rely=0.25, anchor="w")
        # Configurar uma variável de controle para armazenar a categoria selecionada
        self.cmbTipoValor = tk.StringVar()
         # Atribuir a variável de controle ao Combobox
        self.cmbTipo.config(textvariable=self.cmbTipo)
        

        lbl_cadValor = tk.Label(self.root, text=f"VALOR", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadValor.place(relx=0.58, rely=0.35, anchor="w")
        entry_valor = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        entry_valor.place(relx=0.78, rely=0.35, anchor="w")

        lbl_dtaTransacao = tk.Label(self.root, text=f"DATA TRANSACAO", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_dtaTransacao.place(relx=0.58, rely=0.45, anchor="w")
        entry_dtaTransacao = DateEntry(self.root, font=("Helvetica", 12),locale= 'pt_BR', date_pattern = 'dd/mm/yyyy', width=10 ,highlightthickness=1, highlightbackground="black")
        entry_dtaTransacao.place(relx=0.78, rely=0.45, anchor="w")

        lbl_Categoria = tk.Label(self.root, text=f"CATEGORIA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_Categoria.place(relx=0.58, rely=0.55, anchor="w")
        # entry_Categoria = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        # entry_Categoria.place(relx=0.78, rely=0.55, anchor="w")
        categorias = ['Categoria 1', 'Categoria 2', 'Categoria 3']
        self.combobox_categoria = ttk.Combobox(self.root, values=categorias, font=("Helvetica", 12), width=10)
        self.combobox_categoria.place(relx=0.78, rely=0.55, anchor="w")
        # Configurar uma variável de controle para armazenar a categoria selecionada
        self.categoria_selecionada = tk.StringVar()
         # Atribuir a variável de controle ao Combobox
        self.combobox_categoria.config(textvariable=self.categoria_selecionada)
         # Configurar um evento para ser acionado quando a seleção for alterada
        self.combobox_categoria.bind("<<ComboboxSelected>>", self.selecionar_categoria)

        lbl_ContaFinanceira = tk.Label(self.root, text=f"CONTA FINANCEIRA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_ContaFinanceira.place(relx=0.58, rely=0.65, anchor="w")
        entry_ContaFinanceira = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        entry_ContaFinanceira.place(relx=0.78, rely=0.65, anchor="w")

        

     # Botão Salvar
        btn_salvar = tk.Button(self.root, text="Salvar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_salvar.place(relx=0.64, rely=0.75, anchor="w")

    # Botão Atualizar
        btn_atualizar = tk.Button(self.root, text="Atualizar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_atualizar.place(relx=0.71, rely=0.75, anchor="w")

    # Botão Excluir
        btn_excluir = tk.Button(self.root, text="Excluir", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_excluir.place(relx=0.80, rely=0.75, anchor="w")
    

    def selecionar_categoria(self, event):
        # Este método é chamado quando a seleção no Combobox é alterada
        categoria_selecionada = self.categoria_selecionada.get()
        print(f"Categoria selecionada: {categoria_selecionada}")
    
class CadastroContaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Conta")
        self.root.configure(bg="#008BD6")
        self.center_window(900,570)
        self.root.configure(bg="#008BD6")
        self.create_widgets()
        self.tree.bind("<ButtonRelease-1>", self.selecionar_conta)
        
                 
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):

        white_rectangle = tk.Canvas(self.root, bg="#FFFFFF", width=900, height=465)
        white_rectangle.place(relx=0, rely=1, anchor="sw")
        
        ret_cinza = tk.Canvas(self.root, bg="#D9D9D9", width=390, height=425)
        ret_cinza.place(relx=0.03, rely=0.22, anchor="nw")
        
        lbl_cadConta = tk.Label(self.root, text=f"CADASTRO DE CONTAS", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_cadConta.place(relx=0.5, rely=0.10, anchor="center")
        
        lbl_cadConta = tk.Label(self.root, text=f"CONTA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadConta.place(relx=0.58, rely=0.25, anchor="w") 

        self.entry_Conta = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        self.entry_Conta.place(relx=0.75, rely=0.25, anchor="w")

        lbl_cadSaldo = tk.Label(self.root, text=f"SALDO INICIAL", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadSaldo.place(relx=0.58, rely=0.35, anchor="w") 
        
        self.entry_ContaSaldo = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        self.entry_ContaSaldo.place(relx=0.75, rely=0.35, anchor="w")

        lbl_cadDesc = tk.Label(self.root, text=f"DESCRIÇÃO", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadDesc.place(relx=0.58, rely=0.45, anchor="w") 
        
        self.entry_ContaDesc = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        self.entry_ContaDesc.place(relx=0.75, rely=0.45, anchor="w")

        self.btn_salvarConta = tk.Button(self.root, text="Salvar", font=("Helvetica", 12), bg="#008BD6", fg="white",command=self.salvar_conta)
        self.btn_salvarConta.place(relx=0.64, rely=0.55, anchor="w")

    # Botão Atualizar
        self.btn_atualizarConta = tk.Button(self.root, text="Atualizar", font=("Helvetica", 12), bg="#008BD6", fg="white",command=self.atualizar_conta)
        self.btn_atualizarConta.place(relx=0.71, rely=0.55, anchor="w")

    # Botão Excluir
        self.btn_excluirConta = tk.Button(self.root, text="Excluir", font=("Helvetica", 12), bg="#008BD6", fg="white",command=self.excluir_conta)
        self.btn_excluirConta.place(relx=0.80, rely=0.55, anchor="w")

        self.tree = ttk.Treeview(self.root, columns=("idContaFinanceira", "NomeDaConta","Saldo","Descricao","DataCriacao"), show="headings")
        self.tree.heading("idContaFinanceira", text="ID")
        self.tree.heading("NomeDaConta", text="Nome da Conta")
        self.tree.heading("Saldo", text="Saldo")
        self.tree.heading("Descricao", text="Descricao")
        self.tree.heading("DataCriacao", text="Data Criação")
        self.tree.place(relx=0.03, rely=0.22, anchor="nw", width=450, height=425)

        self.tree.tag_configure("center", anchor="center")



        self.tree.column("idContaFinanceira", width=30)
        self.tree.column("NomeDaConta", width=100)
        self.tree.column("Saldo", width=70)
        self.tree.column("Descricao", width=130)
        self.tree.column("DataCriacao", width=100)
    
    def exibir_contas(self, contas):

    # Limpar qualquer conteúdo anterior no retângulo cinza
        self.tree.delete(*self.tree.get_children())

        for conta in contas:
        # Insira uma tupla contendo os valores
            self.tree.insert("", "end", values=(
            conta['idContaFinanceira'],
            conta['NomeDaConta'],
            conta['Saldo'],
            conta['Descricao'],
            conta['DataCriacao']
        ),tags="center")
    
    def carregar_contas(self):
        contas = self.contaFinanceira.carregar_contas()
        self.exibir_contas(contas)


    def salvar_conta(self):
        # Obter dados do Entry e chamar método do controller
        nome_conta = self.entry_conta.get()
        saldo = self.entry_saldo.get()
        descricao = self.entry_descricao.get()

        # Chamar método do controller para salvar a conta
        self.contaFinanceira.salvar_conta()

        print("chegou aqui no salvar")
        # Limpar dados após salvar
        self.limpar_dados()

        # Atualizar a exibição das contas na Treeview
        self.carregar_contas()  # Chamar o método carregar_contas para obter a lista atualizada
        print("passou carregador contas")
        self.exibir_contas()  # Chamar diretamente o método exibir_contas
        print("passou exibir contas")
        # Exibir messagebox de sucesso
        messagebox.showinfo("Sucesso", "Conta salva com sucesso!")

    def atualizar_conta(self):
        # Obter ID da conta selecionada
        self.controller.atualizar_conta()

    def excluir_conta(self):
        # Obter ID da conta selecionada
        selected_item = self.tree.selection()
        if selected_item:
            id_conta = self.tree.item(selected_item, "values")[0]

            # Perguntar se tem certeza antes de excluir
            resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir esta conta?")

            if resposta == "yes":
                # Chamar método do controller para excluir a conta
                self.contaFinanceira.excluir_conta(id_conta)

                # Limpar dados após excluir
                self.limpar_dados()

                # Atualizar a exibição das contas na Treeview
                self.carregar_contas()

                # Exibir messagebox de sucesso
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
        else:
            # Exibir messagebox de erro se nenhum item estiver selecionado
            messagebox.showerror("Erro", "Selecione uma conta para excluir.")

    def limpar_dados(self):
        self.entry_conta.delete(0, tk.END)
        self.entry_saldo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
    
    def selecionar_conta(self, event):
        # Obtém a linha clicada
        item = self.tree.selection()

        self.id_selecionado = 99
        

        if item:
            # Obtém os valores da linha clicada
            values = self.tree.item(item, "values")

            id_conta = self.tree.item(item, "values")[0]
            self.id_selecionado = id_conta

            # Preenche os campos entry_Conta, entry_ContaSaldo e entry_ContaDesc
            self.entry_Conta.delete(0, "end")
            self.entry_Conta.insert(0, values[1])  # Nome da Conta

            self.entry_ContaSaldo.delete(0, "end")
            self.entry_ContaSaldo.insert(0, values[2])  # Saldo

            self.entry_ContaDesc.delete(0, "end")
            self.entry_ContaDesc.insert(0, values[3])  # Descrição
  
class CadastroUsuarioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Usuário")
        self.root.configure(bg="#008BD6")
        self.center_window(900,570)
        self.root.configure(bg="#008BD6")
        self.create_widgets()
        
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        white_rectangle = tk.Canvas(self.root, bg="#FFFFFF", width=900, height=465)
        white_rectangle.place(relx=0, rely=1, anchor="sw") 
        lbl_cadUsuario = tk.Label(self.root, text=f"CADASTRO DE USUARIO", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_cadUsuario.place(relx=0.5, rely=0.10, anchor="center")


        lbl_cadNome = tk.Label(self.root, text=f"NOME", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadNome.place(relx=0.4, rely=0.25, anchor="w") 

        entry_NomeUser = tk.Entry(self.root, font=("Helvetica", 12),width=9 ,highlightthickness=1, highlightbackground="black")
        entry_NomeUser.place(relx=0.5, rely=0.25, anchor="w")

        lbl_cadUser = tk.Label(self.root, text=f"USUARIO", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadUser.place(relx=0.4, rely=0.35, anchor="w") 

        entry_CadUser = tk.Entry(self.root, font=("Helvetica", 12),width=9 ,highlightthickness=1, highlightbackground="black")
        entry_CadUser.place(relx=0.5, rely=0.35, anchor="w")

        lbl_cadSenha = tk.Label(self.root, text=f"SENHA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadSenha.place(relx=0.4, rely=0.45, anchor="w") 

        entry_CadSenha = tk.Entry(self.root, font=("Helvetica", 12),width=9 ,highlightthickness=1, highlightbackground="black")
        entry_CadSenha.place(relx=0.5, rely=0.45, anchor="w")

        lbl_ConfirmSenha = tk.Label(self.root, text=f"CONFIRMAR SENHA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_ConfirmSenha.place(relx=0.30, rely=0.55, anchor="w") 

        entry_ConfirmSenha= tk.Entry(self.root, font=("Helvetica", 12),width=9 ,highlightthickness=1, highlightbackground="black")
        entry_ConfirmSenha.place(relx=0.5, rely=0.55, anchor="w")


        btn_salvarConta = tk.Button(self.root, text="Salvar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_salvarConta.place(relx=0.45, rely=0.65, anchor="w")

    # Botão Atualizar
        btn_atualizarConta = tk.Button(self.root, text="Atualizar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        btn_atualizarConta.place(relx=0.55, rely=0.65, anchor="w")
      
    