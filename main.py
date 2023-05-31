from tkinter import Tk, Label, Entry, Button, Toplevel
import sqlite3


lista_produtos = []

label_info = None


def fazer_login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()

    conn.close()

    if usuario:
        resultado.configure(text="Login realizado com sucesso!", fg="white")
        abrir_nova_janela()
    else:
        resultado.configure(text="Nome de usuário ou senha incorretos.", fg="white")
def abrir_janela_cadastro():
    janela_cadastro = Toplevel(janela)
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.configure(bg="black")

    label_username = Label(janela_cadastro, text="Nome de Usuário:", font=("Arial", 12), fg="white", bg="black")
    label_username.pack()
    entry_username = Entry(janela_cadastro)
    entry_username.pack()

    label_password = Label(janela_cadastro, text="Senha:", font=("Arial", 12), fg="white", bg="black")
    label_password.pack()
    entry_password = Entry(janela_cadastro, show="*")
    entry_password.pack()

    botao_cadastrar = Button(janela_cadastro, text="Cadastrar", command=cadastrar_usuario, bg="white")
    botao_cadastrar.pack()

def criar_banco_dados():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (username TEXT, password TEXT)")

    conn.commit()
    conn.close()
def cadastrar_usuario():
    # Código para cadastrar o novo usuário
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        resultado.configure(text="Usuário cadastrado com sucesso!", fg="white")
    else:
        resultado.configure(text="Preencha todos os campos!", fg="white")

criar_banco_dados()
def abrir_nova_janela():
    nova_janela = Toplevel(janela)
    nova_janela.title("Controle de Estoque")
    nova_janela.configure(bg="black")


    label_nova_janela = Label(nova_janela, text="Produtos", bg="black", fg="white")
    label_nova_janela.pack()

    label_produto = Label(nova_janela, text="Produto:", font=("Arial", 12), fg="white", bg="black")
    label_produto.pack()
    entry_produto = Entry(nova_janela)
    entry_produto.pack()

    label_codigo = Label(nova_janela, text="Código:", font=("Arial", 12), fg="white", bg="black")
    label_codigo.pack()
    entry_codigo = Entry(nova_janela)
    entry_codigo.pack()

    label_preco = Label(nova_janela, text="Preço:", font=("Arial", 12), fg="white", bg="black")
    label_preco.pack()
    entry_preco = Entry(nova_janela)
    entry_preco.pack()

    def adicionar_produto():
        produto = entry_produto.get()
        codigo = entry_codigo.get()
        preco = entry_preco.get()


        if produto and codigo and preco:

            conn = sqlite3.connect("estoque.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO produtos (produto, codigo, preco) VALUES (?, ?, ?)", (produto, codigo, preco))

            conn.commit()
            conn.close()

            atualizar_lista_produtos()
        else:
            label_info.configure(text="Preencha todos os campos!")

        botao_enviar = Button(nova_janela, text="Enviar", command=adicionar_produto, bg="white")
        botao_enviar.pack()

    global label_info
    label_info = Label(nova_janela, text="", fg="white", bg="black")
    label_info.pack()

    def mostrar_produtos():
        conn = sqlite3.connect("estoque.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        conn.close()

        info_text = ""
        for produto in produtos:
            info_text += f"Produto: {produto[0]}, Código: {produto[1]}, Preço: {produto[2]}\n"
        label_info.configure(text=info_text)

    botao_mostrar = Button(nova_janela, text="Mostrar Produtos", command=mostrar_produtos, bg="white")
    botao_mostrar.pack()

def excluir_produto(produto):
    lista_produtos.remove(produto)
    atualizar_lista_produtos()
def atualizar_lista_produtos():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()

    info_text = ""
    for produto in produtos:
        info_text += f"Produto: {produto[0]}, Código: {produto[1]}, Preço: {produto[2]}\n"
    label_info.configure(text=info_text)
def criar_banco_dados():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (produto TEXT, codigo TEXT, preco REAL)")

    conn.commit()
    conn.close()

# Chamar a função criar_banco_dados para criar o arquivo do banco de dados
criar_banco_dados()

def armazenar_produtos():
    # Conexão com o banco de dados
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()

    # Criação da tabela se ainda não existir
    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (produto TEXT, codigo TEXT, preco REAL)")

    # Inserção dos produtos na tabela
    for produto in lista_produtos:
        cursor.execute("INSERT INTO produtos (produto, codigo, preco) VALUES (?, ?, ?)", produto)

    # Commit das alterações e fechamento da conexão
    conn.commit()
    conn.close()

janela = Tk()
janela.title("Tela de Login")
janela.configure(bg="black")


titulo = Label(janela, text="Controle de Estoque", font=("Arial", 16, "bold"), fg="white", bg="black")
titulo.pack()


label_username = Label(janela, text="Nome de Usuário:", font=("Arial", 12), fg="white", bg="black")
label_username.pack()
entry_username = Entry(janela)
entry_username.pack()

label_password = Label(janela, text="Senha:", font=("Arial", 12), fg="white", bg="black")
label_password.pack()
entry_password = Entry(janela, show="*")
entry_password.pack()


botao_login = Button(janela, text="Login", command=fazer_login, bg="white")
botao_login.pack()


botao_cadastrar = Button(janela, text="Cadastre-se", command=abrir_janela_cadastro, bg="white")
botao_cadastrar.pack()


resultado = Label(janela, text="", fg="white", bg="black")
resultado.pack()

janela.protocol("WM_DELETE_WINDOW", armazenar_produtos)


janela.mainloop()