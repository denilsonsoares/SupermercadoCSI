import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="quase_tudo"
        )
        return conexao
    except mysql.connector.Error as err:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para buscar marcas do banco de dados
def buscar_marcas():
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome_da_marca FROM Marcas")
            marcas = cursor.fetchall()
            conexao.close()
            return [f"{m[0]} - {m[1]}" for m in marcas]
        else:
            return []
    except:
        return []

# Função para buscar tipos de produto do banco de dados
def buscar_tipos():
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, tipo FROM Tipos_de_produto")
            tipos = cursor.fetchall()
            conexao.close()
            return [f"{t[0]} - {t[1]}" for t in tipos]
        else:
            return []
    except:
        return []

# Função para buscar unidades de medida do banco de dados
def buscar_unidades():
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, unidade FROM unidades_de_medida")
            unidades = cursor.fetchall()
            conexao.close()
            return [f"{u[0]} - {u[1]}" for u in unidades]
        else:
            return []
    except:
        return []

# Função para buscar produtos do banco de dados
def buscar_produtos():
    try:
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, Produto FROM Produtos")
            produtos = cursor.fetchall()
            conexao.close()
            return [f"{p[0]} - {p[1]}" for p in produtos]
        else:
            return []
    except:
        return []

# Função para limpar o conteúdo do frame principal
def limpar_frame_principal():
    for widget in frame_principal.winfo_children():
        widget.destroy()

# Tela de cadastro de produto
def mostrar_cadastrar_produto():
    limpar_frame_principal()
    tk.Label(frame_principal, text="Cadastrar Produto", font=("Helvetica", 16)).pack(pady=10)

    entry_nome_produto = tk.Entry(frame_principal, width=30)
    entry_nome_produto.insert(0, "Nome do Produto")
    entry_nome_produto.pack(pady=5)

    entry_preco_produto = tk.Entry(frame_principal, width=30)
    entry_preco_produto.insert(0, "Preço por Unidade")
    entry_preco_produto.pack(pady=5)

    # Comboboxes para Marca, Tipo e Unidade de Medida
    combo_marca = ttk.Combobox(frame_principal, width=27)
    combo_marca['values'] = buscar_marcas()  # Carrega marcas
    combo_marca.pack(pady=5)

    combo_tipo = ttk.Combobox(frame_principal, width=27)
    combo_tipo['values'] = buscar_tipos()  # Carrega tipos de produto
    combo_tipo.pack(pady=5)

    combo_unidade = ttk.Combobox(frame_principal, width=27)
    combo_unidade['values'] = buscar_unidades()  # Carrega unidades de medida
    combo_unidade.pack(pady=5)

    def cadastrar_produto():
        nome_produto = entry_nome_produto.get()
        preco_produto = float(entry_preco_produto.get())
        marca_id = int(combo_marca.get().split(" - ")[0])
        tipo_id = int(combo_tipo.get().split(" - ")[0])
        unidade_id = int(combo_unidade.get().split(" - ")[0])

        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO Produtos (Produto, Marca_id, tipo_id, unidade_de_medida_id, preco_por_unidade) VALUES (%s, %s, %s, %s, %s)", 
                           (nome_produto, marca_id, tipo_id, unidade_id, preco_produto))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    button_cadastrar = tk.Button(frame_principal, text="Cadastrar Produto", command=cadastrar_produto)
    button_cadastrar.pack(pady=10)

# Tela de adicionar estoque
def mostrar_adicionar_estoque():
    limpar_frame_principal()
    tk.Label(frame_principal, text="Adicionar Estoque", font=("Helvetica", 16)).pack(pady=10)

    combo_produto = ttk.Combobox(frame_principal, width=27)
    combo_produto['values'] = buscar_produtos()  # Carrega produtos
    combo_produto.pack(pady=5)

    entry_quantidade = tk.Entry(frame_principal, width=30)
    entry_quantidade.insert(0, "Quantidade")
    entry_quantidade.pack(pady=5)

    def adicionar_estoque():
        produto_id = int(combo_produto.get().split(" - ")[0])
        quantidade = int(entry_quantidade.get())

        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE Produtos SET quantidade = quantidade + %s WHERE id = %s", (quantidade, produto_id))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")

    button_adicionar = tk.Button(frame_principal, text="Adicionar ao Estoque", command=adicionar_estoque)
    button_adicionar.pack(pady=10)

# Tela de venda de produto
def mostrar_vender_produto():
    limpar_frame_principal()
    tk.Label(frame_principal, text="Vender Produto", font=("Helvetica", 16)).pack(pady=10)

    combo_produto = ttk.Combobox(frame_principal, width=27)
    combo_produto['values'] = buscar_produtos()  # Carrega produtos
    combo_produto.pack(pady=5)

    entry_quantidade = tk.Entry(frame_principal, width=30)
    entry_quantidade.insert(0, "Quantidade")
    entry_quantidade.pack(pady=5)

    def vender_produto():
        produto_id = int(combo_produto.get().split(" - ")[0])
        quantidade = int(entry_quantidade.get())

        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE Produtos SET quantidade = quantidade - %s WHERE id = %s", (quantidade, produto_id))
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Venda realizada com sucesso!")

    button_vender = tk.Button(frame_principal, text="Vender Produto", command=vender_produto)
    button_vender.pack(pady=10)

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Supermercado - Quase-Tudo")
root.geometry("800x500")

# Frame da sidebar
frame_sidebar = tk.Frame(root, width=200, bg="#f0f0f0")
frame_sidebar.pack(fill="y", side="left")

# Botões da sidebar
button_cadastrar_produto = tk.Button(frame_sidebar, text="Cadastrar Produto", width=20, command=mostrar_cadastrar_produto)
button_cadastrar_produto.pack(pady=20)

button_adicionar_estoque = tk.Button(frame_sidebar, text="Adicionar Estoque", width=20, command=mostrar_adicionar_estoque)
button_adicionar_estoque.pack(pady=20)

button_vender_produto = tk.Button(frame_sidebar, text="Vender Produtos", width=20, command=mostrar_vender_produto)
button_vender_produto.pack(pady=20)

# Frame principal para exibir o conteúdo das interfaces
frame_principal = tk.Frame(root, bg="white")
frame_principal.pack(expand=True, fill="both", side="right")

# Inicializa a interface mostrando a tela de Cadastrar Produto
mostrar_cadastrar_produto()

root.mainloop()