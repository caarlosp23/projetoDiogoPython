import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk
from controller import *
from tkcalendar import DateEntry
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import textwrap


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        width = 900
        height = 570
        self.center_window(width, height)
        self.root.configure(bg="#008BD6")
        self.create_login_fields()
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

        
        lbl_bemvindo = tk.Label(self.root, text=f"BEM VINDO, {nome_usuario}", font=("Helvetica", 20), bg="#008BD6", fg="white")
        lbl_bemvindo.place(relx=0.17, rely=0.12, anchor="center")

        self.btn_categoria = tk.Button(self.root, text="CATEGORIA", font=("Helvetica", 10), bg="#008BD6", fg="white")
        self.btn_categoria.place(relx=0.74, rely=0.12, anchor="center")

        self.btn_conta = tk.Button(self.root, text="CONTA", font=("Helvetica", 10), bg="#008BD6", fg="white")
        self.btn_conta.place(relx=0.84, rely=0.12, anchor="center")

        self.btn_transacao = tk.Button(self.root, text="TRANSACAO", font=("Helvetica", 10), bg="#008BD6", fg="white")
        self.btn_transacao.place(relx=0.94, rely=0.12, anchor="center")

        label_periodo = tk.Label(self.root, text="PERÍODO", font=("Helvetica", 16), bg="#FFFFFF" ,fg="black")
        label_periodo.place(relx=0.05, rely=0.28, anchor="w")


        label_periodoInicial = tk.Label(self.root, text="Data Inicio", font=("Helvetica", 10), bg="#FFFFFF" ,fg="black")
        label_periodoInicial.place(relx=0.02, rely=0.35, anchor="w")

        self.entry_data_inicial = DateEntry(self.root, locale= 'pt_BR', date_pattern = 'dd/mm/yyyy', font=("Helvetica", 10),width=9)
        self.entry_data_inicial.place(relx=0.10, rely=0.35, anchor="w")
  

        label_periodoInicial = tk.Label(self.root, text="Data Fim", font=("Helvetica", 10), bg="#FFFFFF" ,fg="black")
        label_periodoInicial.place(relx=0.02, rely=0.42, anchor="w")

        self.entry_data_final = DateEntry(self.root,locale= 'pt_BR', date_pattern = 'dd/mm/yyyy', font=("Helvetica", 10),width=9)
        self.entry_data_final.place(relx=0.10, rely=0.42, anchor="w")
       
        self.btn_filtrarPeriodo = tk.Button(self.root, text="Filtrar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        self.btn_filtrarPeriodo.place(relx=0.08, rely=0.50, anchor="w")


        #Saldo
        self.lbl_saldoPeriodo = tk.Label(self.root, text="SALDO PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_saldoPeriodo.place(relx=0.25, rely=0.28, anchor="w")

        self.lbl_saldoPeriodoValor = tk.Label(self.root, text="R$0,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_saldoPeriodoValor.place(relx=0.29, rely=0.35, anchor="w")

        #Entrada
        self.lbl_Entrada = tk.Label(self.root, text="ENTRADA PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_Entrada.place(relx=0.49, rely=0.28, anchor="w")

        self.lbl_EntradaValor = tk.Label(self.root, text="R$0,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_EntradaValor.place(relx=0.55, rely=0.35, anchor="w")

        #Saida
        self.lbl_Saida = tk.Label(self.root, text="SAIDA PERIODO", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_Saida.place(relx=0.75, rely=0.28, anchor="w")

        self.lbl_SaidaValor = tk.Label(self.root, text="R$0,00", font=("Helvetica", 16), bg="#FFFFFF", fg="black")
        self.lbl_SaidaValor.place(relx=0.80, rely=0.35, anchor="w")

        self.lbl_SaldoPorConta = tk.Label(self.root, text="SALDO POR CONTA", font=("Helvetica", 10), bg="#FFFFFF", fg="black")
        self.lbl_SaldoPorConta.place(relx=0.05, rely=0.57, anchor="w")
        #TREE VIEW SALDO CONTAS
        self.treeviewSaldoContas = ttk.Treeview(self.root, columns=('Nome da Conta', 'Saldo'), show='headings')

        # Definir cabeçalhos
        self.treeviewSaldoContas.heading('Nome da Conta', text='Nome da Conta')
        self.treeviewSaldoContas.heading('Saldo', text='Saldo')
        self.treeviewSaldoContas.place(relx=0.03, rely=0.60, anchor="nw", width=180, height=180)

        self.treeviewSaldoContas.column("Nome da Conta", width=65)
        self.treeviewSaldoContas.column("Saldo", width=50)
        self.treeviewSaldoContas.tag_configure("center", anchor="center")


        self.lbl_SaldoTotal = tk.Label(self.root,  font=("Helvetica", 10), bg="#FFFFFF", fg="black")
        self.lbl_SaldoTotal.place(relx=0.03, rely=0.95, anchor="w")



        
        #Grafico Entrada
        self.figura = Figure(figsize=(8, 6), tight_layout=True)
        self.eixo = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.43, rely=0.7, anchor="center",width= 300, height=300)

        self.figuraSaida = Figure(figsize=(8, 6), tight_layout=True)
        self.eixoSaida = self.figuraSaida.add_subplot(111)  
        self.canvasSaida = FigureCanvasTkAgg(self.figuraSaida, master=self.root)  
        self.canvas_widgetSaida = self.canvasSaida.get_tk_widget() 
        self.canvas_widgetSaida.place(relx=0.80, rely=0.7, anchor="center", width=300, height=300)
        

       


    def criar_grafico_top_categoria_entrada(self,valoresContro):
        self.eixo.clear()

        categorias = [textwrap.fill(dado['Categoria'], width=10) for dado in valoresContro]
        valores = [float(dado['Valor']) for dado in valoresContro]
        self.eixo.bar(categorias, valores, color='green')
        self.eixo.set_ylabel('Valor')
        self.eixo.set_title('Top Entrada por categoria')

        self.canvas.draw()
    
    def criar_grafico_top_categoria_saida(self,valoresContro):
        
        self.eixoSaida.clear()

        categorias = [textwrap.fill(dado['Categoria'], width=10) for dado in valoresContro]
        valores = [float(dado['Valor']) for dado in valoresContro]

        self.eixoSaida.bar(categorias, valores, color='red')
        self.eixoSaida.set_ylabel('Valor')
        self.eixoSaida.set_title('Top Saida por categoria')

        self.canvasSaida.draw()

    def alimentar_treeview(self, dados):
        for item in self.treeviewSaldoContas.get_children():
            self.treeviewSaldoContas.delete(item)
        for dado in dados:
            self.treeviewSaldoContas.insert('', 'end', values=(dado['NomeDaConta'], dado['SaldoFinal']))

    

    def atualizar_saldo(self):

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
        print('entrou aqui na salvar categoria')
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
        self.treeview.bind("<ButtonRelease-1>", self.preencher_campos)
                 
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

        self.entry_tipoTrans = ttk.Combobox(self.root, font=("Helvetica", 12), width=10)
        self.entry_tipoTrans.place(relx=0.78, rely=0.25, anchor="w")

        lbl_cadValor = tk.Label(self.root, text=f"VALOR", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_cadValor.place(relx=0.58, rely=0.35, anchor="w")
        # entry_valor = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        # entry_valor.place(relx=0.78, rely=0.35, anchor="w")
        validate_cmd = (self.root.register(self.validar_numero), '%P')
        
        self.entry_valor = tk.Entry(self.root, font=("Helvetica", 12), width=12, highlightthickness=1, highlightbackground="black", validate="key", validatecommand=validate_cmd)
        self.entry_valor.place(relx=0.78, rely=0.35, anchor="w")

        lbl_dtaTransacao = tk.Label(self.root, text=f"DATA TRANSACAO", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_dtaTransacao.place(relx=0.58, rely=0.45, anchor="w")
        
        self.entry_dtaTransacao = DateEntry(self.root, font=("Helvetica", 12),locale= 'pt_BR', date_pattern = 'dd/mm/yyyy', width=10 ,highlightthickness=1, highlightbackground="black")
        self.entry_dtaTransacao.place(relx=0.78, rely=0.45, anchor="w")

        lbl_Categoria = tk.Label(self.root, text=f"CATEGORIA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_Categoria.place(relx=0.58, rely=0.55, anchor="w")
        # entry_Categoria = tk.Entry(self.root, font=("Helvetica", 12),width=12 ,highlightthickness=1, highlightbackground="black")
        # entry_Categoria.place(relx=0.78, rely=0.55, anchor="w")
        
        self.combobox_categoria = ttk.Combobox(self.root, font=("Helvetica", 12), width=10)
        self.combobox_categoria.place(relx=0.78, rely=0.55, anchor="w")
        # Configurar uma variável de controle para armazenar a categoria selecionada
        self.categoria_selecionada = tk.StringVar()
         # Atribuir a variável de controle ao Combobox
        self.combobox_categoria.config(textvariable=self.categoria_selecionada)
         # Configurar um evento para ser acionado quando a seleção for alterada
        self.combobox_categoria.bind("<<ComboboxSelected>>", self.selecionar_categoria)

        lbl_ContaFinanceira = tk.Label(self.root, text=f"CONTA FINANCEIRA", font=("Helvetica", 12), bg="#FFFFFF", fg="black")
        lbl_ContaFinanceira.place(relx=0.58, rely=0.65, anchor="w")

        self.cmbContas = ttk.Combobox(self.root, font=("Helvetica", 11), width=11)
        self.cmbContas.place(relx=0.78, rely=0.65, anchor="w")

     # Botão Salvar
        self.btn_salvar = tk.Button(self.root, text="Salvar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        self.btn_salvar.place(relx=0.64, rely=0.75, anchor="w")

    # Botão Atualizar
        self.btn_atualizar = tk.Button(self.root, text="Atualizar", font=("Helvetica", 12), bg="#008BD6", fg="white")
        self.btn_atualizar.place(relx=0.71, rely=0.75, anchor="w")

    # Botão Excluir
        self.btn_excluir = tk.Button(self.root, text="Excluir", font=("Helvetica", 12), bg="#008BD6", fg="white")
        self.btn_excluir.place(relx=0.80, rely=0.75, anchor="w")

       
        # Criar Treeview
        self.treeview = ttk.Treeview(self.root, columns=('ID', 'Tipo Transação', 'Valor', 'Data', 'Categoria', 'Conta'), show='headings', height=10)
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Tipo Transação', text='Transação')
        self.treeview.heading('Valor', text='Valor')
        self.treeview.heading('Data', text='Data')
        self.treeview.heading('Categoria', text='Categoria')
        self.treeview.heading('Conta', text='Conta')

        # Configurar o tamanho das colunas individualmente
        self.treeview.column('ID', width=25, anchor=tk.CENTER)
        self.treeview.column('Tipo Transação', width=70, anchor=tk.CENTER)
        self.treeview.column('Valor', width=80, anchor=tk.CENTER)
        self.treeview.column('Data', width=80, anchor=tk.CENTER)
        self.treeview.column('Categoria', width=100, anchor=tk.CENTER)
        self.treeview.column('Conta', width=100, anchor=tk.CENTER)


        # Criar e posicionar a Treeview no mesmo local do retângulo, definindo largura e altura
        self.treeview.place(relx=0.03, rely=0.22, anchor="nw", width=475, height=425)


   
    def validar_numero(self, novo_valor):
        if novo_valor == "" or novo_valor == "-":
            return True  # Permite Backspace e apagar o conteúdo

        try:
            # Tenta converter o novo valor para float
            float(novo_valor)
            return True
        except ValueError:
            # Se a conversão falhar, significa que não é um número
            return False
        
    def selecionar_categoria(self, event):
        # Este método é chamado quando a seleção no Combobox é alterada
        categoria_selecionada = self.categoria_selecionada.get()
        print(f"Categoria selecionada: {categoria_selecionada}")
    
    def preencher_campos(self, event):
        # Obter a linha clicada
        item = self.treeview.selection()[0]

        # Obter os valores da linha clicada
        valores = self.treeview.item(self.treeview.selection(), 'values')

    # Preencha os campos com os valores obtidos
        self.entry_tipoTrans.set(valores[1])  # Tipo de transação
        self.entry_valor.delete(0, tk.END)
        self.entry_valor.insert(0, valores[2])  # Valor
    # Converta a string de data para um objeto date
        data_transacao = datetime.strptime(valores[3], "%Y-%m-%d").date()
        self.entry_dtaTransacao.set_date(data_transacao)  # Data de transação
        self.combobox_categoria.set(valores[4])  # Categoria
        self.cmbContas.set(valores[5]) 
    

    def obter_id_selecionado(self):
        item_selecionado = self.treeview.selection()
        if item_selecionado:
            return self.treeview.item(item_selecionado)['values'][0]
        return None

    def exibir_transacoes(self, transacoes):
    # Limpar qualquer conteúdo anterior na Treeview
        
        self.treeview.delete(*self.treeview.get_children())

        for transacao in transacoes:
        # Insira uma tupla contendo os valores da transação
            self.treeview.insert("", "end", values=(transacao['idtransacao'], transacao['tipotransacao'], transacao['valor'],
                                                     transacao['datatransacao'], transacao['categoria'],
                                                       transacao['conta']))

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
      
    