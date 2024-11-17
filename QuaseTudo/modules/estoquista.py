import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from .database import *
from .utils import *
from .common_views import *

# Caminho base relativo
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")


# Função para carregar a imagem do produto
def carregar_imagem_produto(label_imagem):
    caminho_imagem = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.png;*.jpg;*.jpeg"), ("Todos os Arquivos", "*.*")]
    )
    if caminho_imagem:
        imagem = Image.open(caminho_imagem).resize((150, 150), Image.LANCZOS)
        imagem = ImageTk.PhotoImage(imagem)
        label_imagem.configure(image=imagem)
        label_imagem.image = imagem  # Manter referência para evitar coleta de lixo
        label_imagem.caminho = caminho_imagem  # Guardar o caminho para futura referência

# Função para busca dinâmica com uma lista suspensa
def adicionar_busca_dinamica(entry, parent, buscar_funcao):
    listbox = tk.Listbox(parent, height=5, selectmode="single")
    listbox.place_forget()  # Inicialmente, a lista está oculta

    def atualizar_resultados(event=None):
        termo = entry.get().strip()
        if termo:
            resultados = buscar_funcao(termo)
            if resultados:
                listbox.delete(0, tk.END)
                for id_, nome in resultados:
                    listbox.insert(tk.END, f"{id_} - {nome}")
                listbox.place(x=entry.winfo_x(), y=entry.winfo_y() + entry.winfo_height())
            else:
                listbox.place_forget()
        else:
            listbox.place_forget()

    def selecionar_item(event):
        selecionado = listbox.get(tk.ACTIVE)
        if selecionado:
            id_, nome = selecionado.split(" - ", 1)
            entry.delete(0, tk.END)
            entry.insert(0, id_)
            listbox.place_forget()

    entry.bind("<KeyRelease>", atualizar_resultados)
    listbox.bind("<ButtonRelease-1>", selecionar_item)

# Função para adicionar um produto ao estoque
def adicionar_produto_estoque(nome, marca_nome, tipo_nome, unidade_nome, preco):
    if not (nome.get() and marca_nome.get() and tipo_nome.get() and unidade_nome.get() and preco.get()):
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    try:
        preco_float = float(preco.get())
    except ValueError:
        messagebox.showerror("Erro", "O preço deve ser um número válido.")
        return

    try:
        # Buscar IDs correspondentes para marca, tipo e unidade
        marca_id = obter_id_por_nome("marcas", "nome", marca_nome.get())
        tipo_id = obter_id_por_nome("tipos", "nome", tipo_nome.get())
        unidade_id = obter_id_por_nome("unidades", "nome", unidade_nome.get())

        # Verificar se os IDs foram encontrados
        if not marca_id:
            messagebox.showerror("Erro", f"Marca '{marca_nome.get()}' não encontrada no banco de dados.")
            return
        if not tipo_id:
            messagebox.showerror("Erro", f"Tipo '{tipo_nome.get()}' não encontrado no banco de dados.")
            return
        if not unidade_id:
            messagebox.showerror("Erro", f"Unidade '{unidade_nome.get()}' não encontrada no banco de dados.")
            return

        # Chamar a função de adicionar produto no banco de dados
        sucesso = adicionar_produto(nome.get(), marca_id, tipo_id, unidade_id, preco_float)
        if sucesso:
            messagebox.showinfo("Sucesso", "Produto adicionado ao estoque com sucesso!")
            # Limpar os campos após adicionar
            nome.set("")
            marca_nome.set("")
            tipo_nome.set("")
            unidade_nome.set("")
            preco.set("")
        else:
            messagebox.showerror("Erro", "Erro ao adicionar produto ao estoque.")
    except Exception as e:
        print(f"Erro ao adicionar produto: {e}")
        messagebox.showerror("Erro", "Erro inesperado ao adicionar produto.")

# Função para remover um produto do estoque
def remover_produto_estoque(nome_produto_entry):
    nome_produto = nome_produto_entry.get().strip()
    if not nome_produto:
        messagebox.showerror("Erro", "Digite o nome do produto a ser removido.")
        return

    sucesso = remover_produto(nome_produto)
    if sucesso:
        messagebox.showinfo("Sucesso", "Produto removido do estoque com sucesso!")
        nome_produto_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Erro ao remover produto do estoque ou produto não encontrado.")

# Função principal para a tela do Estoquista
def tela_estoquista(nome_estoquista, id_estoquista, root, tela_login, abrir_tela_perfil):
    janela_estoquista = tk.Toplevel()
    janela_estoquista.title("Estoquista - Quase-Tudo")
    janela_estoquista.geometry("1000x700")
    janela_estoquista.configure(bg="#f4f4f4")
    janela_estoquista.attributes("-fullscreen", True)



    # Variável para controlar a área de conteúdo atual
    conteudo_atual = None

    #common views
    # Funções para alternar o conteúdo
    def chamar_mostrar_fornecedores():
        nonlocal conteudo_atual
        conteudo_atual = mostrar_fornecedores(conteudo_atual, frame_conteudo, janela_estoquista)

    def chamar_mostrar_estoque():
        nonlocal conteudo_atual
        conteudo_atual = mostrar_estoque(conteudo_atual, frame_conteudo)

    def chamar_mostrar_gestao_produtos():
        nonlocal conteudo_atual
        conteudo_atual = mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_estoquista)

    def chamar_registrar_lote():
        registrar_lote_interface(janela_estoquista)

    # Menu Lateral - fixo à esquerda
    frame_menu = tk.Frame(janela_estoquista, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

    botoes_menu = [
        ("Estoque", chamar_mostrar_estoque),
        ("Fornecedores", chamar_mostrar_fornecedores),
        ("Gestão de Produtos", chamar_mostrar_gestao_produtos),
        ("Registrar Lote", chamar_registrar_lote),
    ]
    for texto, comando in botoes_menu:
        tk.Button(frame_menu, text=texto, font=("Arial", 12), bg="#d3d3d3", fg="black", bd=0, relief="flat",
        activebackground="#a9a9a9", activeforeground="white", command=comando).pack(fill="x", pady=10)


    frame_cabecalho = tk.Frame(janela_estoquista, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    label_nome = tk.Label(frame_cabecalho, text=nome_estoquista, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")

    label_id = tk.Label(frame_cabecalho, text=f"Estoquista ID {id_estoquista}", bg="#e0e0e0", font=("Arial", 10))
    label_id.place(relx=0.85, rely=0.5, anchor="e")

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0").place(relx=0.9, rely=0.5, anchor="e")

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(frame_cabecalho, image=imagem_logout, bg="#e0e0e0", bd=0, command=lambda: logout(janela_estoquista, root, tela_login, abrir_tela_perfil))
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    frame_conteudo = tk.Frame(janela_estoquista, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    chamar_mostrar_estoque()

    janela_estoquista.mainloop()


