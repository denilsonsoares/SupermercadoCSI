import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from modules.database import adicionar_produto, remover_produto, buscar_produtos, obter_id_por_nome

# Caminho base relativo
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

# Função para atualizar o horário
def atualizar_hora(label):
    def atualizar():
        agora = datetime.now()
        label.config(text=agora.strftime("%d / %m / %Y  %H:%M"))
        label.after(1000, atualizar)
    atualizar()

# Função de logout
def logout(janela, root, tela_login, abrir_tela_perfil):
    janela.destroy()
    tela_login(root, abrir_tela_perfil)

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

    frame_menu = tk.Frame(janela_estoquista, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

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

    # Frame para adicionar novos produtos
    frame_adicionar = tk.LabelFrame(frame_conteudo, text="ADICIONAR NOVOS PRODUTOS", font=("Arial", 12), bg="white")
    frame_adicionar.pack(fill="x", padx=10, pady=10)

    nome_var = tk.StringVar()
    marca_var = tk.StringVar()
    tipo_var = tk.StringVar()
    unidade_var = tk.StringVar()
    preco_var = tk.StringVar()

    tk.Label(frame_adicionar, text="Nome do produto:", bg="white").grid(row=0, column=0, padx=10, pady=5)
    nome_entry = tk.Entry(frame_adicionar, textvariable=nome_var)
    nome_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_adicionar, text="Marca:", bg="white").grid(row=1, column=0, padx=10, pady=5)
    marca_entry = tk.Entry(frame_adicionar, textvariable=marca_var)
    marca_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_adicionar, text="Tipo:", bg="white").grid(row=2, column=0, padx=10, pady=5)
    tipo_entry = tk.Entry(frame_adicionar, textvariable=tipo_var)
    tipo_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_adicionar, text="Unidade de Medida:", bg="white").grid(row=3, column=0, padx=10, pady=5)
    unidade_entry = tk.Entry(frame_adicionar, textvariable=unidade_var)
    unidade_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame_adicionar, text="Preço:", bg="white").grid(row=4, column=0, padx=10, pady=5)
    tk.Entry(frame_adicionar, textvariable=preco_var).grid(row=4, column=1, padx=10, pady=5)

    tk.Button(frame_adicionar, text="Adicionar", bg="green", fg="white", font=("Arial", 12),
          command=lambda: adicionar_produto_estoque(
              nome_var, marca_var, tipo_var, unidade_var, preco_var
          )).grid(row=5, column=0, columnspan=2, pady=10)


    # Frame para remover produtos
    frame_remover = tk.LabelFrame(frame_conteudo, text="REMOVER PRODUTO EXISTENTE", font=("Arial", 12), bg="white")
    frame_remover.pack(fill="x", padx=10, pady=10)

    tk.Label(frame_remover, text="Nome do produto:", bg="white").grid(row=0, column=0, padx=10, pady=5)
    nome_produto_entry = tk.Entry(frame_remover)
    nome_produto_entry.grid(row=0, column=1, padx=10, pady=5)
    adicionar_busca_dinamica(nome_produto_entry, frame_remover, buscar_produtos)

    tk.Button(frame_remover, text="Remover", bg="red", fg="white", font=("Arial", 12), command=lambda: remover_produto_estoque(nome_produto_entry)).grid(row=1, column=0, columnspan=2, pady=10)

    janela_estoquista.mainloop()


