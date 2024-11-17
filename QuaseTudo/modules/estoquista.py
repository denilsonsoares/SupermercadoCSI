import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from .database import *

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



    # Variável para controlar a área de conteúdo atual
    conteudo_atual = None

    # Funções para alternar o conteúdo
    def mostrar_fornecedores():
        nonlocal conteudo_atual
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Fornecedores", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Total de lotes entregues por fornecedor
        tk.Label(conteudo_atual, text="Total de Lotes por Fornecedor:", bg="white", font=("Arial", 14, "bold")).pack(
            pady=10)

        fornecedores = total_lotes_por_fornecedor()
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Nome", "Total Lotes"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Total Lotes", text="Total Lotes")
        tree.pack(fill="both", expand=True)
        for fornecedor in fornecedores:
            tree.insert("", "end", values=fornecedor)

        def visualizar_historico():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um fornecedor para visualizar o histórico.")
                return
            fornecedor_id = tree.item(selected_item)['values'][0]
            fornecedor_nome = tree.item(selected_item)['values'][1]
            historico = historico_entregas_fornecedor(fornecedor_id)

            janela_historico = tk.Toplevel(janela_estoquista)
            janela_historico.title(f"Histórico de Entregas - {fornecedor_nome}")
            janela_historico.geometry("600x400")

            tk.Label(janela_historico, text=f"Histórico de Entregas - {fornecedor_nome}",
                     font=("Arial", 14, "bold")).pack(pady=10)

            tree_historico = ttk.Treeview(janela_historico, columns=(
            "Lote ID", "Produto", "Quantidade", "Data Fabricação", "Data Vencimento"), show="headings")
            tree_historico.heading("Lote ID", text="Lote ID")
            tree_historico.heading("Produto", text="Produto")
            tree_historico.heading("Quantidade", text="Quantidade")
            tree_historico.heading("Data Fabricação", text="Data Fabricação")
            tree_historico.heading("Data Vencimento", text="Data Vencimento")
            tree_historico.pack(fill="both", expand=True)
            for entrega in historico:
                tree_historico.insert("", "end", values=entrega)

        tk.Button(conteudo_atual, text="Visualizar Histórico de Entregas", command=visualizar_historico).pack(pady=10)

    def mostrar_estoque():
        nonlocal conteudo_atual
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        # Configurar a grade de layout
        conteudo_atual.rowconfigure(0, weight=2)  # Parte superior (40%)
        conteudo_atual.rowconfigure(1, weight=3)  # Parte inferior (60%)
        conteudo_atual.columnconfigure(0, weight=1)

        # Frame superior para as duas tabelas lado a lado
        frame_superior = tk.Frame(conteudo_atual, bg="white")
        frame_superior.grid(row=0, column=0, sticky="nsew")

        # Configurar colunas no frame superior
        frame_superior.columnconfigure(0, weight=1)
        frame_superior.columnconfigure(1, weight=1)

        # Frame esquerdo (Produtos com Menor Quantidade em Estoque)
        frame_esquerdo = tk.Frame(frame_superior, bg="white")
        frame_esquerdo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Frame direito (Lotes Próximos do Vencimento)
        frame_direito = tk.Frame(frame_superior, bg="white")
        frame_direito.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Tabela: Produtos com Menor Quantidade em Estoque
        tk.Label(frame_esquerdo, text="Produtos com Menor Quantidade em Estoque:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        produtos_menor_estoque = produtos_com_menor_estoque()
        tree_menor_estoque = ttk.Treeview(frame_esquerdo, columns=("ID", "Produto", "Quantidade"), show="headings")
        tree_menor_estoque.heading("ID", text="ID")
        tree_menor_estoque.heading("Produto", text="Produto")
        tree_menor_estoque.heading("Quantidade", text="Quantidade")
        tree_menor_estoque.pack(fill="both", expand=True)
        for produto in produtos_menor_estoque:
            tree_menor_estoque.insert("", "end", values=produto)

        # Tabela: Lotes Próximos do Vencimento
        tk.Label(frame_direito, text="Lotes Próximos do Vencimento:", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
        lotes_vencimento = lotes_proximos_vencimento()
        tree_vencimento = ttk.Treeview(frame_direito, columns=("Lote ID", "Produto", "Marca", "Data de Vencimento", "Quantidade"),
                                       show="headings")
        tree_vencimento.heading("Lote ID", text="Lote ID")
        tree_vencimento.column("Lote ID", width=50)
        tree_vencimento.heading("Produto", text="Produto")
        tree_vencimento.column("Produto", width=120)
        tree_vencimento.heading("Marca", text="Marca")
        tree_vencimento.column("Marca", width=120)
        tree_vencimento.heading("Data de Vencimento", text="Data de Vencimento")
        tree_vencimento.heading("Quantidade", text="Quantidade")
        tree_vencimento.pack(fill="both", expand=True)
        for lote in lotes_vencimento:
            tree_vencimento.insert("", "end", values=lote)

        # Frame inferior para a tabela de Quantidade Inicial e Restante dos Lotes
        frame_inferior = tk.Frame(conteudo_atual, bg="white")
        frame_inferior.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Filtros
        frame_filtros = tk.Frame(frame_inferior, bg="white")
        frame_filtros.pack(pady=5)

        tk.Label(frame_filtros, text="Filtrar por:", bg="white", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Marca:", bg="white").pack(side="left")
        entry_filtro_marca = tk.Entry(frame_filtros)
        entry_filtro_marca.pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Produto:", bg="white").pack(side="left")
        entry_filtro_produto = tk.Entry(frame_filtros)
        entry_filtro_produto.pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Lote ID:", bg="white").pack(side="left")
        entry_filtro_lote_id = tk.Entry(frame_filtros)
        entry_filtro_lote_id.pack(side="left", padx=5)

        def aplicar_filtros_lotes():
            filtro_marca = entry_filtro_marca.get()
            filtro_produto = entry_filtro_produto.get()
            filtro_lote_id = entry_filtro_lote_id.get()
            lotes_quantidades = quantidade_inicial_e_restante_lotes(filtro_marca, filtro_produto, filtro_lote_id)
            # Limpar a treeview
            for item in tree_lotes.get_children():
                tree_lotes.delete(item)
            for lote in lotes_quantidades:
                tree_lotes.insert("", "end", values=lote)

        tk.Button(frame_filtros, text="Aplicar Filtros", command=aplicar_filtros_lotes).pack(side="left", padx=5)

        # Tabela: Quantidade Inicial e Restante dos Lotes
        tk.Label(frame_inferior, text="Quantidade Inicial e Restante dos Lotes:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("Lote ID", "Marca", "Produto", "Quantidade Inicial", "Quantidade Restante",
                   "Data de Vencimento", "Fornecedor")
        tree_lotes = ttk.Treeview(frame_inferior, columns=columns, show="headings")
        for col in columns:
            tree_lotes.heading(col, text=col)
        tree_lotes.pack(fill="both", expand=True)

        # Carregar dados iniciais
        lotes_quantidades = quantidade_inicial_e_restante_lotes()
        for lote in lotes_quantidades:
            tree_lotes.insert("", "end", values=lote)

    def mostrar_gestao_produtos():

        def cadastrar_produto_interface():
            janela_cadastrar = tk.Toplevel(janela_estoquista)
            janela_cadastrar.title("Cadastrar Produto")
            janela_cadastrar.geometry("400x400")

            tk.Label(janela_cadastrar, text="Nome do Produto:").pack()
            entry_nome = tk.Entry(janela_cadastrar)
            entry_nome.pack()

            tk.Label(janela_cadastrar, text="Marca:").pack()
            marcas = [marca[1] for marca in buscar_marcas("")]
            combo_marca = ttk.Combobox(janela_cadastrar, values=marcas)
            combo_marca.pack()

            tk.Label(janela_cadastrar, text="Tipo:").pack()
            tipos = [tipo[1] for tipo in buscar_tipos("")]
            combo_tipo = ttk.Combobox(janela_cadastrar, values=tipos)
            combo_tipo.pack()

            tk.Label(janela_cadastrar, text="Unidade de Medida:").pack()
            unidades = [unidade[1] for unidade in buscar_unidades("")]
            combo_unidade = ttk.Combobox(janela_cadastrar, values=unidades)
            combo_unidade.pack()

            tk.Label(janela_cadastrar, text="Preço por Unidade:").pack()
            entry_preco = tk.Entry(janela_cadastrar)
            entry_preco.pack()

            def salvar_produto():
                nome = entry_nome.get()
                marca = combo_marca.get()
                tipo = combo_tipo.get()
                unidade = combo_unidade.get()
                preco = entry_preco.get()
                try:
                    preco = float(preco)
                except ValueError:
                    messagebox.showerror("Erro", "Preço inválido.")
                    return
                marca_id = obter_id_por_nome("marcas", "nome_da_marca", marca)
                tipo_id = obter_id_por_nome("tipos_de_produto", "tipo", tipo)
                unidade_id = obter_id_por_nome("unidades_de_medida", "unidade", unidade)
                if not (marca_id and tipo_id and unidade_id):
                    messagebox.showerror("Erro", "Marca, tipo ou unidade inválidos.")
                    return
                if cadastrar_produto(nome, marca_id, tipo_id, unidade_id, preco):
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
                    janela_cadastrar.destroy()
                    mostrar_gestao_produtos()
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar produto.")

            tk.Button(janela_cadastrar, text="Salvar", command=salvar_produto).pack(pady=10)

        def atualizar_preco_produto_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um produto para atualizar o preço.")
                return
            produto_id = tree.item(selected_item)['values'][0]
            produto_nome = tree.item(selected_item)['values'][1]
            preco_atual = tree.item(selected_item)['values'][4]

            janela_atualizar = tk.Toplevel(janela_estoquista)
            janela_atualizar.title("Atualizar Preço do Produto")
            janela_atualizar.geometry("300x200")

            tk.Label(janela_atualizar, text=f"Produto: {produto_nome}").pack(pady=5)
            tk.Label(janela_atualizar, text=f"Preço Atual: R$ {preco_atual}").pack(pady=5)

            tk.Label(janela_atualizar, text="Novo Preço:").pack()
            entry_novo_preco = tk.Entry(janela_atualizar)
            entry_novo_preco.pack()

            def salvar_novo_preco():
                novo_preco = entry_novo_preco.get()
                try:
                    novo_preco = float(novo_preco)
                except ValueError:
                    messagebox.showerror("Erro", "Preço inválido.")
                    return
                if atualizar_preco_produto(produto_id, novo_preco):
                    messagebox.showinfo("Sucesso", "Preço atualizado com sucesso!")
                    janela_atualizar.destroy()
                    mostrar_gestao_produtos()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar preço do produto.")

            tk.Button(janela_atualizar, text="Salvar", command=salvar_novo_preco).pack(pady=10)

        def visualizar_lotes_produto_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um produto para visualizar os lotes.")
                return
            produto_id = tree.item(selected_item)['values'][0]
            produto_nome = tree.item(selected_item)['values'][1]
            lotes = visualizar_lotes_produto(produto_id)

            janela_lotes = tk.Toplevel(janela_estoquista)
            janela_lotes.title(f"Lotes do Produto - {produto_nome}")
            janela_lotes.geometry("600x400")

            tk.Label(janela_lotes, text=f"Lotes do Produto - {produto_nome}", font=("Arial", 14, "bold")).pack(pady=10)

            tree_lotes = ttk.Treeview(janela_lotes,
                                      columns=("Lote ID", "Data Fabricação", "Data Vencimento", "Quantidade"),
                                      show="headings")
            tree_lotes.heading("Lote ID", text="Lote ID")
            tree_lotes.heading("Data Fabricação", text="Data Fabricação")
            tree_lotes.heading("Data Vencimento", text="Data Vencimento")
            tree_lotes.heading("Quantidade", text="Quantidade")
            tree_lotes.pack(fill="both", expand=True)
            for lote in lotes:
                tree_lotes.insert("", "end", values=lote)

        nonlocal conteudo_atual
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Produtos", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        frame_acoes = tk.Frame(conteudo_atual, bg="white")
        frame_acoes.pack(pady=10)

        tk.Button(frame_acoes, text="Cadastrar Produto", command=cadastrar_produto_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Atualizar Preço", command=atualizar_preco_produto_interface).pack(side="left",
                                                                                                       padx=5)
        tk.Button(frame_acoes, text="Visualizar Lotes do Produto", command=visualizar_lotes_produto_interface).pack(
            side="left", padx=5)

        # Filtros
        frame_filtros = tk.Frame(conteudo_atual, bg="white")
        frame_filtros.pack(pady=10)

        tk.Label(frame_filtros, text="Filtro Marca:").pack(side="left")
        entry_filtro_marca = tk.Entry(frame_filtros)
        entry_filtro_marca.pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Filtro Tipo:").pack(side="left")
        entry_filtro_tipo = tk.Entry(frame_filtros)
        entry_filtro_tipo.pack(side="left", padx=5)

        var_filtro_estoque = tk.BooleanVar()
        tk.Checkbutton(frame_filtros, text="Com Estoque", variable=var_filtro_estoque, bg="white").pack(side="left",
                                                                                                        padx=5)

        def aplicar_filtros():
            filtro_marca = entry_filtro_marca.get()
            filtro_tipo = entry_filtro_tipo.get()
            filtro_estoque = var_filtro_estoque.get()
            produtos = consultar_produtos(filtro_marca, filtro_tipo, filtro_estoque)
            # Limpar a treeview
            for item in tree.get_children():
                tree.delete(item)
            for produto in produtos:
                tree.insert("", "end", values=produto)

        tk.Button(frame_filtros, text="Aplicar Filtros", command=aplicar_filtros).pack(side="left", padx=5)

        # Lista de produtos
        tk.Label(conteudo_atual, text="Lista de Produtos:", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
        produtos = consultar_produtos()
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Produto", "Marca", "Tipo", "Preço"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Produto", text="Produto")
        tree.heading("Marca", text="Marca")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Preço", text="Preço")
        tree.pack(fill="both", expand=True)
        for produto in produtos:
            tree.insert("", "end", values=produto)

    # Menu Lateral - fixo à esquerda
    frame_menu = tk.Frame(janela_estoquista, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

    botoes_menu = [
        ("Estoque", mostrar_estoque),
        ("Fornecedores", mostrar_fornecedores),
        ("Gestão de Produtos", mostrar_gestao_produtos),
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

    mostrar_estoque()

    janela_estoquista.mainloop()


