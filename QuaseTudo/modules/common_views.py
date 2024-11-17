import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
from .database import *
from .utils import *


# Funções para alternar o conteúdo
def mostrar_fornecedores(conteudo_atual, frame_conteudo, janela_principal):
    if conteudo_atual:
        conteudo_atual.destroy()
    conteudo_atual = tk.Frame(frame_conteudo, bg="white")
    conteudo_atual.pack(fill="both", expand=True)

    tk.Label(conteudo_atual, text="Gestão de Fornecedores", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Total de lotes entregues por fornecedor
    tk.Label(conteudo_atual, text="Total de Lotes por Fornecedor:", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

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

        janela_historico = tk.Toplevel(janela_principal)
        janela_historico.title(f"Histórico de Entregas - {fornecedor_nome}")
        janela_historico.geometry("600x400")

        tk.Label(janela_historico, text=f"Histórico de Entregas - {fornecedor_nome}", font=("Arial", 14, "bold")).pack(pady=10)

        tree_historico = ttk.Treeview(janela_historico, columns=("Lote ID", "Produto", "Quantidade", "Data Fabricação", "Data Vencimento"), show="headings")
        tree_historico.heading("Lote ID", text="Lote ID")
        tree_historico.heading("Produto", text="Produto")
        tree_historico.heading("Quantidade", text="Quantidade")
        tree_historico.heading("Data Fabricação", text="Data Fabricação")
        tree_historico.heading("Data Vencimento", text="Data Vencimento")
        tree_historico.pack(fill="both", expand=True)
        for entrega in historico:
            tree_historico.insert("", "end", values=entrega)

    tk.Button(conteudo_atual, text="Visualizar Histórico de Entregas", command=visualizar_historico).pack(pady=10)

    return conteudo_atual

def mostrar_estoque(conteudo_atual, frame_conteudo):
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

    return conteudo_atual

def mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_principal):
    if conteudo_atual:
        conteudo_atual.destroy()
    conteudo_atual = tk.Frame(frame_conteudo, bg="white")
    conteudo_atual.pack(fill="both", expand=True)

    def cadastrar_produto_interface():
        janela_cadastrar = tk.Toplevel(janela_principal)
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

        janela_atualizar = tk.Toplevel(janela_principal)
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

        janela_lotes = tk.Toplevel(janela_principal)
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

    return conteudo_atual

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from .database import listar_produtos, listar_fornecedores, cadastrar_fornecedor, registrar_lote

def registrar_lote_interface(janela_principal):
    # Criar uma nova janela Toplevel
    janela_registrar_lote = tk.Toplevel(janela_principal)
    janela_registrar_lote.title("Registrar Lote")
    janela_registrar_lote.geometry("500x700")

    # Selecionar o produto
    tk.Label(janela_registrar_lote, text="Produto:").pack()
    produtos = listar_produtos()
    if not produtos:
        messagebox.showerror("Erro", "Nenhum produto encontrado. Cadastre um produto antes de registrar um lote.")
        janela_registrar_lote.destroy()
        return
    produto_nomes = [f"{p[0]} - {p[1]}" for p in produtos]
    combo_produto = ttk.Combobox(janela_registrar_lote, values=produto_nomes)
    combo_produto.pack()

    # Preencher os campos do lote
    tk.Label(janela_registrar_lote, text="Quantidade:").pack()
    entry_quantidade = tk.Entry(janela_registrar_lote)
    entry_quantidade.pack()

    tk.Label(janela_registrar_lote, text="Preço de Compra:").pack()
    entry_preco_compra = tk.Entry(janela_registrar_lote)
    entry_preco_compra.pack()

    # Data e Hora de Fabricação
    tk.Label(janela_registrar_lote, text="Data e Hora de Fabricação:").pack()
    frame_data_fabricacao = tk.Frame(janela_registrar_lote)
    frame_data_fabricacao.pack()

    entry_data_fabricacao = DateEntry(frame_data_fabricacao, date_pattern='yyyy-mm-dd')
    entry_data_fabricacao.pack(side='left')

    tk.Label(frame_data_fabricacao, text="Hora (HH:MM:SS):").pack(side='left')
    entry_hora_fabricacao = tk.Entry(frame_data_fabricacao, width=8)
    entry_hora_fabricacao.pack(side='left')

    # Data e Hora de Vencimento
    tk.Label(janela_registrar_lote, text="Data e Hora de Vencimento:").pack()
    frame_data_vencimento = tk.Frame(janela_registrar_lote)
    frame_data_vencimento.pack()

    entry_data_vencimento = DateEntry(frame_data_vencimento, date_pattern='yyyy-mm-dd')
    entry_data_vencimento.pack(side='left')

    tk.Label(frame_data_vencimento, text="Hora (HH:MM:SS):").pack(side='left')
    entry_hora_vencimento = tk.Entry(frame_data_vencimento, width=8)
    entry_hora_vencimento.pack(side='left')

    # Opções para o fornecedor
    tk.Label(janela_registrar_lote, text="Fornecedor:").pack()

    var_fornecedor_option = tk.StringVar(value="existente")
    frame_fornecedor = tk.Frame(janela_registrar_lote)
    frame_fornecedor.pack()

    tk.Radiobutton(frame_fornecedor, text="Existente", variable=var_fornecedor_option, value="existente").pack(side="left")
    tk.Radiobutton(frame_fornecedor, text="Novo", variable=var_fornecedor_option, value="novo").pack(side="left")

    # Fornecedor existente
    frame_fornecedor_existente = tk.Frame(janela_registrar_lote)
    frame_fornecedor_existente.pack()

    tk.Label(frame_fornecedor_existente, text="Selecionar Fornecedor:").pack()
    fornecedores = listar_fornecedores()
    fornecedor_nomes = [f"{f[0]} - {f[1]}" for f in fornecedores]
    combo_fornecedor_existente = ttk.Combobox(frame_fornecedor_existente, values=fornecedor_nomes)
    combo_fornecedor_existente.pack()

    # Novo fornecedor
    frame_fornecedor_novo = tk.Frame(janela_registrar_lote)

    tk.Label(frame_fornecedor_novo, text="Nome do Novo Fornecedor:").pack()
    entry_nome_fornecedor_novo = tk.Entry(frame_fornecedor_novo)
    entry_nome_fornecedor_novo.pack()

    # Atualizar visibilidade dos frames de fornecedor
    def atualizar_opcao_fornecedor(*args):
        if var_fornecedor_option.get() == "existente":
            frame_fornecedor_existente.pack()
            frame_fornecedor_novo.pack_forget()
        else:
            frame_fornecedor_existente.pack_forget()
            frame_fornecedor_novo.pack()

    var_fornecedor_option.trace("w", atualizar_opcao_fornecedor)
    atualizar_opcao_fornecedor()

    # Função para salvar o lote
    def salvar_lote():
        produto_selecionado = combo_produto.get()
        if not produto_selecionado:
            messagebox.showerror("Erro", "Selecione um produto.")
            return
        try:
            produto_id = int(produto_selecionado.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Erro", "Produto inválido.")
            return

        quantidade = entry_quantidade.get()
        preco_compra = entry_preco_compra.get()
        data_fabricacao = entry_data_fabricacao.get()
        hora_fabricacao = entry_hora_fabricacao.get()
        data_vencimento = entry_data_vencimento.get()
        hora_vencimento = entry_hora_vencimento.get()

        if not (quantidade and preco_compra and data_fabricacao and hora_fabricacao and data_vencimento and hora_vencimento):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser um número inteiro positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return

        try:
            preco_compra = float(preco_compra)
            if preco_compra <= 0:
                messagebox.showerror("Erro", "O preço de compra deve ser um número positivo.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Preço de compra deve ser um número válido.")
            return

        # Validar as datas e horas
        try:
            data_hora_fabricacao_str = f"{data_fabricacao} {hora_fabricacao}"
            data_hora_fabricacao = datetime.strptime(data_hora_fabricacao_str, '%Y-%m-%d %H:%M:%S')

            data_hora_vencimento_str = f"{data_vencimento} {hora_vencimento}"
            data_hora_vencimento = datetime.strptime(data_hora_vencimento_str, '%Y-%m-%d %H:%M:%S')

            if data_hora_fabricacao >= data_hora_vencimento:
                messagebox.showerror("Erro", "A data e hora de fabricação devem ser anteriores à data e hora de vencimento.")
                return
        except ValueError:
            messagebox.showerror("Erro", "Formato de data ou hora inválido. Use o formato HH:MM:SS para as horas.")
            return

        # Tratamento do fornecedor
        if var_fornecedor_option.get() == "existente":
            fornecedor_selecionado = combo_fornecedor_existente.get()
            if not fornecedor_selecionado:
                messagebox.showerror("Erro", "Selecione um fornecedor existente.")
                return
            try:
                fornecedor_id = int(fornecedor_selecionado.split(" - ")[0])
            except ValueError:
                messagebox.showerror("Erro", "Fornecedor inválido.")
                return
        else:
            nome_fornecedor_novo = entry_nome_fornecedor_novo.get()
            if not nome_fornecedor_novo:
                messagebox.showerror("Erro", "Digite o nome do novo fornecedor.")
                return
            fornecedor_id = cadastrar_fornecedor(nome_fornecedor_novo)
            if not fornecedor_id:
                # A função cadastrar_fornecedor já exibe a mensagem de erro
                return

        # Chamar a função registrar_lote com quantidade como inicial e atual
        sucesso = registrar_lote(
            produto_id,
            preco_compra,
            quantidade,
            quantidade,
            data_hora_fabricacao,
            data_hora_vencimento,
            fornecedor_id
        )
        if sucesso:
            messagebox.showinfo("Sucesso", "Lote registrado com sucesso.")
            janela_registrar_lote.destroy()
        else:
            # A função registrar_lote já exibe a mensagem de erro
            pass

    tk.Button(janela_registrar_lote, text="Salvar", command=salvar_lote).pack(pady=10)