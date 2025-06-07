import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# =====/PARTE EXCLUSIVA PARA O BANCO DE DADOS\=====
# Cria ou abre o banco de dados
def conectar_db():
    criar_banco()
    return sqlite3.connect("Banco.db")

def criar_banco():
    conexao = sqlite3.connect("Banco.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
        nome TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        PRIMARY KEY (nome)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipamento (
        id INTEGER,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,
        disponivel INTEGER DEFAULT 1,
        preco REAL NOT NULL,
        PRIMARY KEY (id)
        );
    """)

    conexao.commit()
    conexao.close()

def cadastrar_usuario(nome, senha):
    conexao = conectar_db()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO Usuario (nome, senha) VALUES (?, ?)", (nome, senha))
        conexao.commit()
    except sqlite3.IntegrityError:
        pass  # Caso o usuário já existe, o comando é ignorado
    conexao.close()

def cadastrar_equipamento(id, nome, tipo, disponivel, preco):
    conexao = conectar_db()
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO Equipamento (id, nome, tipo, disponivel, preco) VALUES (?, ?)", (id, nome, tipo, disponivel, preco))
        conexao.commit()
    except sqlite3.IntegrityError:
        pass  # Caso este equipamento já esteja registrado, este comando é apenas ignorado
    conexao.close()
#===================================================

# Muda a cor da letra ao selecionar para digitar algo no login
def escrever_ativado_usuario(event):
    if usuario_entry.get() == "Digite o seu Usuário aqui":
        usuario_entry.delete(0, "end")
        usuario_entry.config(fg="black")
def escrever_ativado_senha(event):
     if senha_entry.get() == "Digite a sua Senha aqui":
        senha_entry.delete(0, "end")
        senha_entry.config(fg="black")

# Retorna a cor da letra ao normal quando não selecionar para digitar algo no login
def escrever_desativado_usuario(event):
    if not usuario_entry.get():
        usuario_entry.insert(0, "Digite o seu Usuário aqui")
        usuario_entry.config(fg="gray")
def escrever_desativado_senha(event):
    if not senha_entry.get():
        senha_entry.insert(0, "Digite a sua senha aqui")
        senha_entry.config(fg="gray")

# Apenas um código simples para fazer uma transferencia de janela enquanto o banco de dados não é implementado
def verificar_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    conexao = conectar_db()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM Usuario WHERE nome = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    if resultado:
        messagebox.showinfo("Sucesso", "Login efetuado com sucesso")
        login.destroy()  # Fecha a janela de login quando usuário e senha estão corretos
        Login_Efetuado()  # Chama a ação Login_Efetuado, quando o usuário e senha estão corretos
    else:
        messagebox.showerror("Erro", "Usuário ou senha não foram encontrados no sistema")





# Cria a tela de login (tela inicial) e também as configurações de tamanho e etc da tela inicial de Login
criar_banco()
cadastrar_usuario("Rogerio", "1234") #Gigante Rogerio o maior de todos
login = tk.Tk()
login.title("Página de Login - Aluguel Genérico")
width = 500
height = 300
screen_width = login.winfo_screenwidth()
screen_height = login.winfo_screenheight()
x = int((screen_width / 2) - (width / 2))
y = int((screen_height / 2) - (height / 2))
login.geometry(f"{width}x{height}+{x}+{y}")


# Cria o espaço para digitar o nome de usuário do usuário no login
usuario_label = tk.Label(login, text="Usuário", font=("Arial", 16))
usuario_label.grid(row=1, column=0, padx=215, pady=10, sticky="n")

usuario_entry = tk.Entry(login, width=30, bg="white", fg="gray")
usuario_entry.grid(row=2, column=0, pady=10, sticky="n")
usuario_entry.insert(0, "Digite o seu Login aqui")
usuario_entry.bind("<FocusIn>", escrever_ativado_usuario) # Quando for escrever chama a função escrever_ativado_usuario
usuario_entry.bind("<FocusOut>", escrever_desativado_usuario) # Quando não for escrever chama a função escrever_desativado_usuario


# Cria o espaço para digitar a senha do usuário no login
senha_label = tk.Label(login, text="Senha", font=("Arial", 16))
senha_label.grid(row=5, column=0, pady=10, sticky="n")

senha_entry = tk.Entry(login, width=30, bg="white", fg="gray")
senha_entry.grid(row=6, column=0, pady=10, sticky="n")
senha_entry.insert(0, "Digite a sua Senha aqui")
senha_entry.bind("<FocusIn>", escrever_ativado_senha) # Quando for escrever chama a função escrever_ativado_senha
senha_entry.bind("<FocusOut>", escrever_desativado_senha) # Quando não for escrever chama a função escrever_desativado_senha


# Cria uma frame para ambos os botões conseguirem ficar lado a lado, sem isso os botões ficam muito distantes
botoes_frame = tk.Frame(login)
botoes_frame.grid(row=8, column=0, pady=10)
# Cria dois botões, um para logar e outro para sair do sistema
entrar_button = tk.Button(botoes_frame, text="Entrar", width= 10, command=verificar_login)
entrar_button.pack(side="left", padx=10)

sair_button = tk.Button(botoes_frame, text="Sair", width= 10)
sair_button.pack(side="left", padx=10)

def Login_Efetuado():
# Cria uma nova janela, sendo essa janela uma de gerenciamento, além disso personaliza ela mudando tamanho, cor e etc
    gerenciamento = tk.Tk()
    gerenciamento.title("Página de Gerenciamento - Aluguel Genérico")
    frame1 = tk.Frame(master=gerenciamento, height=50, bg="#7AC6C0")
    frame1.pack(fill=tk.X)
    width = 700
    height = 400
    screen_width = gerenciamento.winfo_screenwidth()
    screen_height = gerenciamento.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    gerenciamento.geometry(f"{width}x{height}+{x}+{y}")

# Frame que troca a parte de baixo da tela ao clicar nos botões, fiz para não ter que ficar criando várias janelas diferentes conforme eu vou clicando nos botões.
    frame_troca_tela = tk.Frame(gerenciamento)
    frame_troca_tela.pack(fill=tk.BOTH, expand=True)
    
# Faz com que a janela relatorio seja aberta quando o botão "relatório" é pressionado (Talvez eu remova no futuro)
    def ir_relatorio():
        abrir_relatorio()  # Abre a janela do relatorio
    
# Nome autoexplicativo, é uma função que mostra o estoque quando você clicar no botão "estoque"
    def mostrar_estoque():
        for widget in frame_troca_tela.winfo_children():
            widget.destroy()
        tabela_estoque = ttk.Treeview(frame_troca_tela, columns=("id", "nome", "tipo", "disponivel", "preco"), show="headings")
        tabela_estoque.pack(fill=tk.BOTH, expand=True)       

        tabela_estoque.heading("id", text="ID")
        tabela_estoque.heading("nome", text="Nome")
        tabela_estoque.heading("tipo", text="Tipo")
        tabela_estoque.heading("disponivel", text="Situação")
        tabela_estoque.heading("preco", text="Preço por dia")

        tabela_estoque.column("id", width=50)
        tabela_estoque.column("nome", width=100)
        tabela_estoque.column("tipo", width=100)
        tabela_estoque.column("disponivel", width=100)
        tabela_estoque.column("preco", width=100)

        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Equipamento")
        equipamentos = cursor.fetchall()
        conexao.close()

        for equipamento in equipamentos:
            id, nome, tipo, disponivel, preco = equipamento
            situacao = "Alugado" if disponivel else "Não Alugado"
            tabela_estoque.insert("", "end", values=(id, nome, tipo, situacao, preco))

# Mostra o estoque porém adiciona a função de editar caso um equipamento do estoque tenha sido selecionado
    def mostrar_editar():
        for widget in frame_troca_tela.winfo_children():
            widget.destroy()

        tabela = ttk.Treeview(frame_troca_tela, columns=("id", "nome", "tipo", "disponivel", "preco"), show="headings")
        tabela.pack(fill=tk.BOTH, expand=True)

        for col in ("id", "nome", "tipo", "disponivel", "preco"):
            tabela.heading(col, text=col.capitalize())
            tabela.column(col, width=100)

        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Equipamento")
        for row in cursor.fetchall():
            id, nome, tipo, disponivel, preco = row
            situacao = "Alugado" if disponivel else "Não Alugado"
            tabela.insert("", "end", values=(id, nome, tipo, situacao, preco))
        conexao.close()

# Cria uma nova janela quando um equipamento é selecionado para editar
        def editar():
            item = tabela.selection()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um equipamento para editar.")
                return

            valores = tabela.item(item)["values"]
            id_atual = valores[0]

            edit_window = tk.Toplevel()
            edit_window.title("Editar Equipamento")
            edit_window.geometry("300x220")

            campos = ["Nome", "Tipo", "Situação", "Preço por dia"]
            entradas = []

            for i, campo in enumerate(campos):
                tk.Label(edit_window, text=campo).grid(row=i, column=0, padx=5, pady=5)
                entrada = ttk.Entry(edit_window)
                entrada.grid(row=i, column=1, padx=5, pady=5)
                entrada.insert(0, valores[i + 1])
                entradas.append(entrada)

# Função que salva o que foi editado na janela nova de edição
            def salvar():
                nome = entradas[0].get()
                tipo = entradas[1].get()
                disponivel_str = entradas[2].get().strip().lower()
                disponivel = 1 if disponivel_str == "alugado" else 0
                try:
                    preco = float(entradas[3].get())
                except ValueError:
                    messagebox.showerror("Erro", "O preço deve ser um número.")
                    return

                conexao = conectar_db()
                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE Equipamento SET nome=?, tipo=?, disponivel=?, preco=? WHERE id=?
                """, (nome, tipo, disponivel, preco, id_atual))
                conexao.commit()
                conexao.close()

                messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso.")
                edit_window.destroy()
                mostrar_estoque()

            tk.Button(edit_window, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=10)

        # Botão para editar item selecionado
        botao_editar = tk.Button(frame_troca_tela, text="Editar Selecionado", command=editar)
        botao_editar.pack(pady=10)


    def mostrar_remover ():
        for widget in frame_troca_tela.winfo_children():
            widget.destroy()
        tabela = ttk.Treeview(frame_troca_tela, columns=("id", "nome", "tipo", "disponivel", "preco"), show="headings")
        tabela.pack(fill=tk.BOTH, expand=True)

        for col in ("id", "nome", "tipo", "disponivel", "preco"):
            tabela.heading(col, text=col.capitalize())
            tabela.column(col, width=100)

        conexao = conectar_db()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Equipamento")
        for row in cursor.fetchall():
            id, nome, tipo, disponivel, preco = row
            situacao = "Alugado" if disponivel else "Não Alugado"
            tabela.insert("", "end", values=(id, nome, tipo, situacao, preco))
        conexao.close()
        def remover():
            item = tabela.selection()
            if not item:
                messagebox.showwarning("Atenção", "Selecione um equipamento para remover.")
                return

            valores = tabela.item(item)["values"]
            id_atual = valores[0]

            conexao = conectar_db()
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM Equipamento WHERE id=?", (id_atual,))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Equipamento removido com sucesso.")
            mostrar_estoque()

        botao_remover = tk.Button(frame_troca_tela, text="Remover Selecionado", command=remover)
        botao_remover.pack(pady=10)
        
    
# Cria os botões Cadastrar, Estoque, Editar e Remover
    cadastrar_button = tk.Button(frame1, text="Cadastrar", width= 10, bg="#7AC6C0", relief="flat", command=abrir_cadastrar)
    cadastrar_button.pack(side="left", pady=5, padx=5)

    estoque_button = tk.Button(frame1, text="Estoque", width=10, bg="#7AC6C0", relief="flat", command=mostrar_estoque)
    estoque_button.pack(side="left", pady=5, padx=5)

    editar_button = tk.Button(frame1, text="Editar", width=10, bg="#7AC6C0", relief="flat", command=mostrar_editar)
    editar_button.pack(side="left", pady=5, padx=5)

    remover_button = tk.Button(frame1, text="Remover", width=10, bg="#7AC6C0", relief="flat", command=mostrar_remover)
    remover_button.pack(side="left", pady=5, padx=5)

    relatorio_button = tk.Button(frame1, text="Relatório", width=10, bg="#7AC6C0", relief="flat", command=ir_relatorio)
    relatorio_button.pack(side="left", pady=5, padx=5)

# Após a função ir_relatorio ser acionada, está função abre uma nova janela chamada relatório
def abrir_relatorio ():
    relatorio = tk.Tk()
    relatorio.title("Página de Relatório - Aluguel Genérico")
    width = 500
    height = 300
    screen_width = relatorio.winfo_screenwidth()
    screen_height = relatorio.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    relatorio.geometry(f"{width}x{height}+{x}+{y}")

def abrir_cadastrar ():
    cadastro = tk.Tk()
    cadastro.title("Cadastro de Equipamentos - Aluguel Genérico")
    width = 500
    height = 350
    screen_width = cadastro.winfo_screenwidth()
    screen_height = cadastro.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    cadastro.geometry(f"{width}x{height}+{x}+{y}")

    cadastro_frame = tk.Frame(cadastro)
    cadastro_frame.grid(row=2, padx=4, pady=10)

# Cria o título da pagina
    titulo_label = tk.Label(cadastro, text="Cadastre de Equipamento", font=("Arial", 17))
    titulo_label.grid(row=1, column= 0, columnspan=2, padx=150, pady= 10)

# Cria um espaço para digitar o ID do equipamento de som
    id_produto = tk.Label(cadastro_frame, text= "ID do Equipamento:", font=("Arial", 13))
    id_produto.grid(row=4, column=0)
    id_entry = tk.Entry(cadastro_frame, width=30, bg="white")
    id_entry.grid(row=4, column=1, pady=10)

# Cria um espaço para digitar o nome do equipamento de som
    nome_produto = tk.Label(cadastro_frame, text= "Nome do Equipamento:", font=("Arial", 13))
    nome_produto.grid(row=5, column=0, padx=0)
    nomeP_entry = tk.Entry(cadastro_frame, width=30, bg="white")
    nomeP_entry.grid(row=5, column=1, pady=10)

# Cria um espaço para digitar o tipo do equipamento de som
    tipo_produto = tk.Label(cadastro_frame, text= "Tipo do Equipamento:", font=("Arial", 13))
    tipo_produto.grid(row=6, column=0, padx=0)
    tipo_entry = tk.Entry(cadastro_frame, width=30, bg="white")
    tipo_entry.grid(row=6, column=1, pady=10)

# Cria um espaço para digitar o preço do aluguel
    preco_produto = tk.Label(cadastro_frame, text= "Preço:", font=("Arial", 13))
    preco_produto.grid(row=7, column=0, padx=0)
    preco_entry = tk.Entry(cadastro_frame, width=30, bg="white")
    preco_entry.grid(row=7, column=1, pady=10)

# Nesse espaço vou criar uma texto com duas opções, uma escrito "alugado" e outra "não alugado"
    disponivel_label = tk.Label(cadastro_frame, text= "Situação:", font=("Arial", 13))
    disponivel_label.grid(row=8, column=0, padx=0)
    disponivel_opcao = ["Não Alugado", "Alugado"]
    disponivel_combo = ttk.Combobox(cadastro_frame, values= disponivel_opcao)
    disponivel_combo.grid(row= 8, column=1, pady=10)
    disponivel_combo.current(0)

# Configurações dos botões de "Confirmar" e "Cancelar" da tela de cadastro, botões criados logo abaixo
    def cancelar_cadastro():
        cadastro.destroy()

    def confirmar_cadastro():
        id = int(id_entry.get())
        nome = nomeP_entry.get()
        tipo = tipo_entry.get()
        disponivel = disponivel_combo.get()
        preco = int(preco_entry.get())


        if id and nome and tipo and preco and disponivel:
            try:
                disponivel_int = 0 if disponivel == "Não Alugado" else 1
                conexao = conectar_db()
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO Equipamento (id, nome, tipo, disponivel, preco) VALUES (?, ?, ?, ?, ?)", (id, nome, tipo, float(preco), disponivel_int))
                conexao.commit()
                conexao.close()
                messagebox.showinfo("Sucesso", "O Equipamento foi cadastrado com sucesso")
            except Exception as e:
                messagebox.showinfo("Erro", f"Erro ao cadastrar: {e}")
        else:
                messagebox.showerror("Erro", "Verifique se você preencheu todos os campos")


# Cria dois botões, um para confirmar o cadastro e outro para cancelar a criação
    enviar_buttom = tk.Button(cadastro_frame, text= "Concluir", width= 15, command=confirmar_cadastro)
    enviar_buttom.grid (row=9, column=0, pady=20)

    cancelar_buttom = tk.Button (cadastro_frame,text="Cancelar", width= 15, command=cancelar_cadastro)
    cancelar_buttom.grid (row=9, column=1, pady=20)

login.mainloop()
