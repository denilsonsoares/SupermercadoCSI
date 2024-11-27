# usuario.py

from .db_connection import ConexaoSingleton
from .database import *
from .utils import *
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

class Usuario:
    def __init__(self, id_usuario, username, senha, perfil):
        self.id_usuario = id_usuario
        self.username = username
        self.senha = senha
        self.perfil = perfil

    @classmethod
    def autenticar(cls, username, senha):
        conexao = ConexaoSingleton().conectar_banco()
        if not conexao:
            return None
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                SELECT id, username, senha, perfil 
                FROM usuarios 
                WHERE username=%s AND senha=%s
            """, (username, senha))
            result = cursor.fetchone()
            if result:
                id_usuario, username_db, senha_db, perfil = result
                if perfil == "Gerente":
                    return Gerente(id_usuario, username_db, senha_db)
                elif perfil == "Caixa":
                    return Caixa(id_usuario, username_db, senha_db)
                elif perfil == "Estoquista":
                    return Estoquista(id_usuario, username_db, senha_db)
                else:
                    return Usuario(id_usuario, username_db, senha_db, perfil)
            else:
                return None
        finally:
            cursor.close()

    # Métodos compartilhados entre Gerente e Estoquista

    def mostrar_fornecedores(self, conteudo_atual, frame_conteudo, janela_principal):
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Fornecedores", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Total de lotes entregues por fornecedor
        tk.Label(conteudo_atual, text="Total de Lotes por Fornecedor:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)

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

        return conteudo_atual

    def mostrar_estoque(self, conteudo_atual, frame_conteudo):
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
        tk.Label(frame_direito, text="Lotes Próximos do Vencimento:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        lotes_vencimento = lotes_proximos_vencimento()
        tree_vencimento = ttk.Treeview(frame_direito,
                                       columns=("Lote ID", "Produto", "Marca", "Data de Vencimento", "Quantidade"),
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

    def mostrar_gestao_produtos(self, conteudo_atual, frame_conteudo, janela_principal):
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
                    self.mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_principal)
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
                    self.mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_principal)
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

        frame_acoes = tk.Frame(conteudo_atual, bg="white")
        frame_acoes.pack(pady=10)

        tk.Button(frame_acoes, text="Cadastrar Produto", command=cadastrar_produto_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Atualizar Preço", command=atualizar_preco_produto_interface).pack(side="left",
                                                                                                       padx=5)
        tk.Button(frame_acoes, text="Visualizar Lotes do Produto",
                  command=visualizar_lotes_produto_interface).pack(side="left", padx=5)

        return conteudo_atual

    def registrar_lote_interface(self, janela_principal):
        # Método para registrar lote utilizando funções do database.py

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

        tk.Radiobutton(frame_fornecedor, text="Existente", variable=var_fornecedor_option,
                       value="existente").pack(side="left")
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

            if not (
                    quantidade and preco_compra and data_fabricacao and hora_fabricacao and data_vencimento and
                    hora_vencimento):
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
                    messagebox.showerror("Erro",
                                         "A data e hora de fabricação devem ser anteriores à data e hora de vencimento.")
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

class Gerente(Usuario):
    def __init__(self, id_usuario, username, senha):
        super().__init__(id_usuario, username, senha, perfil='Gerente')

    # Methods specific to Gerente

    # User Management Methods
    def adicionar_usuario(self, username, senha, perfil):
        return adicionar_usuario(username, senha, perfil)

    def editar_usuario(self, usuario_id, username, senha, perfil):
        return editar_usuario(usuario_id, username, senha, perfil)

    def excluir_usuario(self, usuario_id):
        return excluir_usuario(usuario_id)

    def listar_usuarios(self):
        return listar_usuarios()

    # Client Management Methods
    def cadastrar_cliente(self, nome, cpf, telefone):
        return cadastrar_cliente(nome, cpf, telefone)

    def atualizar_cliente(self, cliente_id, nome, cpf, telefone):
        return atualizar_cliente(cliente_id, nome, cpf, telefone)

    def excluir_cliente(self, cliente_id):
        return excluir_cliente(cliente_id)

    def clientes_compras_recentes(self, dias=30):
        return clientes_compras_recentes(dias)

    # GUI Methods

    def mostrar_visao_geral(self, conteudo_atual, frame_conteudo):
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Visão Geral", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Resumo de vendas
        resumo = resumo_vendas(periodo='dia')
        if resumo:
            total_faturado, numero_vendas, itens_vendidos = resumo[1], resumo[2], resumo[3]
            tk.Label(conteudo_atual, text=f"Total Faturado Hoje: R$ {total_faturado}", bg="white",
                     font=("Arial", 12)).pack(pady=5)
            tk.Label(conteudo_atual, text=f"Número de Vendas: {numero_vendas}", bg="white", font=("Arial", 12)).pack(
                pady=5)
            tk.Label(conteudo_atual, text=f"Itens Vendidos: {itens_vendidos}", bg="white", font=("Arial", 12)).pack(
                pady=5)
        else:
            tk.Label(conteudo_atual, text="Nenhuma venda registrada hoje.", bg="white", font=("Arial", 12)).pack(pady=5)

        # Top 5 produtos mais vendidos
        tk.Label(conteudo_atual, text="Top 5 Produtos Mais Vendidos Hoje:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        top_produtos = top_produtos_vendidos(periodo='dia')
        for produto in top_produtos:
            produto_nome, quantidade_vendida = produto[0], produto[1]
            tk.Label(conteudo_atual, text=f"{produto_nome}: {quantidade_vendida} unidades", bg="white",
                     font=("Arial", 12)).pack(anchor='w', padx=20)
        return conteudo_atual

    def mostrar_gestao_clientes(self, conteudo_atual, frame_conteudo, janela_principal):
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Clientes", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        frame_acoes = tk.Frame(conteudo_atual, bg="white")
        frame_acoes.pack(pady=10)

        tk.Button(frame_acoes, text="Cadastrar Cliente",
                  command=lambda: self.cadastrar_cliente_interface(janela_principal, conteudo_atual,
                                                                   frame_conteudo)).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Atualizar Cliente",
                  command=lambda: self.atualizar_cliente_interface(conteudo_atual, frame_conteudo)).pack(side="left",
                                                                                                         padx=5)
        tk.Button(frame_acoes, text="Excluir Cliente",
                  command=lambda: self.excluir_cliente_interface(conteudo_atual, frame_conteudo)).pack(side="left",
                                                                                                       padx=5)

        tk.Label(conteudo_atual, text="Clientes com Compras Recentes:", bg="white", font=("Arial", 14, "bold")).pack(
            pady=10)
        clientes = self.clientes_compras_recentes(dias=30)
        self.tree_clientes = ttk.Treeview(conteudo_atual, columns=("ID", "Nome", "CPF", "Telefone"), show="headings")
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nome", text="Nome")
        self.tree_clientes.heading("CPF", text="CPF")
        self.tree_clientes.heading("Telefone", text="Telefone")
        self.tree_clientes.pack(fill="both", expand=True)
        for cliente in clientes:
            self.tree_clientes.insert("", "end", values=cliente)

        return conteudo_atual

    def cadastrar_cliente_interface(self, janela_principal, conteudo_atual, frame_conteudo):
        janela_cadastrar = tk.Toplevel(janela_principal)
        janela_cadastrar.title("Cadastrar Cliente")
        janela_cadastrar.geometry("300x200")

        tk.Label(janela_cadastrar, text="Nome:").pack()
        entry_nome = tk.Entry(janela_cadastrar)
        entry_nome.pack()

        tk.Label(janela_cadastrar, text="CPF:").pack()
        entry_cpf = tk.Entry(janela_cadastrar)
        entry_cpf.pack()

        tk.Label(janela_cadastrar, text="Telefone:").pack()
        entry_telefone = tk.Entry(janela_cadastrar)
        entry_telefone.pack()

        def salvar_cliente():
            nome = entry_nome.get()
            cpf = entry_cpf.get()
            telefone = entry_telefone.get()
            if self.cadastrar_cliente(nome, cpf, telefone):
                messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                janela_cadastrar.destroy()
                # Refresh the client management view
                self.mostrar_gestao_clientes(conteudo_atual, frame_conteudo, janela_principal)
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar cliente.")

        tk.Button(janela_cadastrar, text="Salvar", command=salvar_cliente).pack(pady=10)

    def atualizar_cliente_interface(self, conteudo_atual, frame_conteudo):
        selected_item = self.tree_clientes.focus()  # Use self.tree_clientes
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")
            return
        cliente_id, nome_atual, cpf_atual, telefone_atual = self.tree_clientes.item(selected_item)['values']

        janela_atualizar = tk.Toplevel()
        janela_atualizar.title("Atualizar Cliente")
        janela_atualizar.geometry("300x200")

        tk.Label(janela_atualizar, text="Nome:").pack()
        entry_nome = tk.Entry(janela_atualizar)
        entry_nome.insert(0, nome_atual)
        entry_nome.pack()

        tk.Label(janela_atualizar, text="CPF:").pack()
        entry_cpf = tk.Entry(janela_atualizar)
        entry_cpf.insert(0, cpf_atual)
        entry_cpf.pack()

        tk.Label(janela_atualizar, text="Telefone:").pack()
        entry_telefone = tk.Entry(janela_atualizar)
        entry_telefone.insert(0, telefone_atual)
        entry_telefone.pack()

        def salvar_alteracoes():
            nome = entry_nome.get()
            cpf = entry_cpf.get()
            telefone = entry_telefone.get()
            if self.atualizar_cliente(cliente_id, nome, cpf, telefone):  # Use self
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                janela_atualizar.destroy()
                self.mostrar_gestao_clientes(conteudo_atual, frame_conteudo, None)  # Use self
            else:
                messagebox.showerror("Erro", "Erro ao atualizar cliente.")

        tk.Button(janela_atualizar, text="Salvar", command=salvar_alteracoes).pack(pady=10)

    def excluir_cliente_interface(self, conteudo_atual, frame_conteudo):
        selected_item = self.tree_clientes.focus()  # Use self.tree_clientes
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        cliente_id = self.tree_clientes.item(selected_item)['values'][0]
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?")
        if resposta:
            if self.excluir_cliente(cliente_id):  # Use self
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                self.mostrar_gestao_clientes(conteudo_atual, frame_conteudo, None)  # Use self
            else:
                messagebox.showerror("Erro", "Erro ao excluir cliente.")

    # Additional methods for user interfaces
    def adicionar_usuario_interface(self, janela_principal, conteudo_atual, frame_conteudo):
        janela_adicionar = tk.Toplevel(janela_principal)
        janela_adicionar.title("Adicionar Usuário")
        janela_adicionar.geometry("300x250")

        tk.Label(janela_adicionar, text="Username:").pack()
        entry_username = tk.Entry(janela_adicionar)
        entry_username.pack()

        tk.Label(janela_adicionar, text="Senha:").pack()
        entry_senha = tk.Entry(janela_adicionar, show="*")
        entry_senha.pack()

        tk.Label(janela_adicionar, text="Perfil:").pack()
        combo_perfil = ttk.Combobox(janela_adicionar, values=["Caixa", "Gerente", "Estoquista"])
        combo_perfil.pack()

        def salvar_usuario():
            username = entry_username.get()
            senha = entry_senha.get()
            perfil = combo_perfil.get()
            if self.adicionar_usuario(username, senha, perfil):  # Use self
                messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
                janela_adicionar.destroy()
                self.mostrar_gestao_usuarios(conteudo_atual, frame_conteudo, None)  # Use self
            else:
                messagebox.showerror("Erro", "Erro ao adicionar usuário.")

        tk.Button(janela_adicionar, text="Salvar", command=salvar_usuario).pack(pady=10)

    def editar_usuario_interface(self, conteudo_atual, frame_conteudo):
        selected_item = self.tree_usuarios.focus()  # Use self.tree_usuarios
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return
        usuario_id, username_atual, perfil_atual = self.tree_usuarios.item(selected_item)['values']

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Usuário")
        janela_editar.geometry("300x250")

        tk.Label(janela_editar, text="Username:").pack()
        entry_username = tk.Entry(janela_editar)
        entry_username.insert(0, username_atual)
        entry_username.pack()

        tk.Label(janela_editar, text="Senha (deixe em branco para não alterar):").pack()
        entry_senha = tk.Entry(janela_editar, show="*")
        entry_senha.pack()

        tk.Label(janela_editar, text="Perfil:").pack()
        combo_perfil = ttk.Combobox(janela_editar, values=["Caixa", "Gerente", "Estoquista"])
        combo_perfil.set(perfil_atual)
        combo_perfil.pack()

        def salvar_alteracoes():
            username = entry_username.get()
            senha = entry_senha.get()
            perfil = combo_perfil.get()
            if not senha:
                # Se a senha não foi alterada, mantenha a senha atual
                senha = None
            if self.editar_usuario(usuario_id, username, senha, perfil):  # Use self.editar_usuario
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                janela_editar.destroy()
                self.mostrar_gestao_usuarios(conteudo_atual, frame_conteudo)  # Use self para chamar o método
            else:
                messagebox.showerror("Erro", "Erro ao atualizar usuário.")

        tk.Button(janela_editar, text="Salvar", command=salvar_alteracoes).pack(pady=10)

    def excluir_usuario_interface(self, conteudo_atual, frame_conteudo):
        selected_item = self.tree_usuarios.focus()  # Use self.tree_usuarios
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
            return
        usuario_id = self.tree_usuarios.item(selected_item)['values'][0]
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?")
        if resposta:
            if self.excluir_usuario(usuario_id):  # Use self.excluir_usuario
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                self.mostrar_gestao_usuarios(conteudo_atual, frame_conteudo)  # Use self
            else:
                messagebox.showerror("Erro", "Erro ao excluir usuário.")


class Estoquista(Usuario):
    def __init__(self, id_usuario, username, senha):
        super().__init__(id_usuario, username, senha, perfil='Estoquista')

    # Methods specific to Estoquista

    # Product Management Methods
    def adicionar_produto(self, nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade):
        return cadastrar_produto(nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade)

    def remover_produto(self, produto_id):
        # Assuming there is a function in database.py to remove a product by ID
        return remover_produto_por_id(produto_id)

    def registrar_lote(self, produto_id, preco_de_compra, quantidade_inicial, data_fabricacao, data_vencimento, fornecedor_id):
        return registrar_lote(produto_id, preco_de_compra, quantidade_inicial, quantidade_inicial, data_fabricacao, data_vencimento, fornecedor_id)

    # Additional methods specific to Estoquista can be added here

class Caixa(Usuario):
    def __init__(self, id_usuario, username, senha):
        super().__init__(id_usuario, username, senha, perfil='Caixa')

    # Methods specific to Caixa

    def atualizar_totais(self, tabela, total_label, avista_label, pagamento_var):
        total = 0
        for item in tabela.get_children():
            valores = tabela.item(item, "values")
            total += float(valores[5])  # Soma o valor total do produto

        if pagamento_var.get() in ["Dinheiro", "Débito"]:
            valor_avista = total * 0.95  # Aplica 5% de desconto
        else:
            valor_avista = total

        total_label.config(text=f"R${total:.2f}")
        avista_label.config(text=f"R${valor_avista:.2f}")

    def realizar_venda_interface(self, frame_conteudo):
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        tabela_frame = tk.Frame(frame_conteudo, bg="white")
        tabela_frame.pack(pady=10, padx=10, fill="x")

        tabela = ttk.Treeview(
            tabela_frame,
            columns=("Produto", "Marca", "Tipo", "Quantidade", "Valor Unitário", "Total", "ID_Lote"),
            show="headings",
            height=5,
        )
        tabela.heading("Produto", text="Produto")
        tabela.heading("Marca", text="Marca")
        tabela.heading("Tipo", text="Tipo")
        tabela.heading("Quantidade", text="Quantidade")
        tabela.heading("Valor Unitário", text="Valor Unitário")
        tabela.heading("Total", text="Total")
        tabela.heading("ID_Lote", text="ID_Lote")
        tabela.pack(side="left", fill="x", expand=True)

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        def adicionar_produto():
            def atualizar_resultados(event=None):
                nome_produto = entry_produto.get()
                resultados = buscar_produtos(nome_produto)

                for widget in frame_resultados.winfo_children():
                    widget.destroy()

                if resultados:
                    for produto in resultados:
                        produto_nome = produto[1]
                        produto_marca = buscar_nome_marca_por_id(produto[2])
                        produto_tipo = buscar_nome_tipo_por_id(produto[3])
                        produto_preco = produto[4]

                        resultado_label = tk.Label(
                            frame_resultados,
                            text=f"{produto_nome} - {produto_marca} - {produto_tipo} - R${produto_preco:.2f}",
                            bg="white",
                            anchor="w",
                        )
                        resultado_label.pack(fill="x", padx=5, pady=2)
                        resultado_label.bind(
                            "<Button-1>",
                            lambda e, p=produto: adicionar_produto_selecionado(p),
                        )

            def adicionar_produto_selecionado(produto):
                def buscar_e_exibir_lotes(event=None):
                    lote_id = lote_entry.get().strip()
                    produto_id = produto[0]  # ID do produto vindo do banco de dados

                    # Buscar lotes mesmo que o ID esteja vazio
                    lotes = buscar_lotes(lote_id, produto_id)

                    # Limpar a lista
                    lotes_lista.delete(0, tk.END)

                    if lotes:
                        for lote in lotes:
                            # Formato: ID - Quantidade - Validade - Fornecedor
                            lotes_lista.insert(
                                tk.END,
                                f"{lote[0]} - {lote[1]} unidades - Vence em {lote[3]} - {lote[4]}"
                            )
                    else:
                        lotes_lista.insert(tk.END, "Nenhum lote encontrado.")

                def confirmar_quantidade():
                    try:
                        # Verificar se há um lote selecionado
                        if not lotes_lista.curselection():
                            raise ValueError("É necessário selecionar um lote.")

                        lote_selecionado = lotes_lista.get(lotes_lista.curselection())
                        lote_id = lote_selecionado.split(" - ")[0]  # Pegar o ID do lote
                        quantidade = int(quantidade_entry.get())

                        if quantidade <= 0:
                            raise ValueError("A quantidade deve ser maior que zero.")

                        # Validar quantidade com o lote
                        lote_quantidade = int(lote_selecionado.split(" - ")[1].split(" ")[0])
                        if quantidade > lote_quantidade:
                            raise ValueError("A quantidade excede o disponível no lote selecionado.")

                        produto_nome = produto[1]
                        produto_marca = buscar_nome_marca_por_id(produto[2])
                        produto_tipo = buscar_nome_tipo_por_id(produto[3])
                        produto_preco = produto[4]
                        total = quantidade * produto_preco

                        # Adicionar o produto à tabela principal
                        tabela.insert(
                            "",
                            "end",
                            values=(
                                produto_nome,
                                produto_marca,
                                produto_tipo,
                                quantidade,
                                f"{produto_preco:.2f}",
                                f"{total:.2f}",
                                lote_id,  # Inclui o ID do lote
                            ),
                        )

                        self.atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
                        quantidade_window.destroy()
                    except ValueError as e:
                        messagebox.showerror("Erro", str(e))
                    except IndexError:
                        messagebox.showerror("Erro", "Erro ao selecionar lote ou quantidade.")

                quantidade_window = tk.Toplevel(pesquisa_window)
                quantidade_window.title("Quantidade e Lote")
                quantidade_window.geometry("500x550")  # Aumentar a altura da janela
                quantidade_window.configure(bg="white")

                tk.Label(
                    quantidade_window, text=f"Produto: {produto[1]}", font=("Arial", 12), bg="white"
                ).pack(pady=10)

                tk.Label(
                    quantidade_window, text="Digite o ID do lote:", font=("Arial", 12), bg="white"
                ).pack(pady=5)

                lote_entry = tk.Entry(quantidade_window, font=("Arial", 12))
                lote_entry.pack(pady=5, padx=10, fill="x")
                lote_entry.bind("<KeyRelease>", buscar_e_exibir_lotes)  # Busca dinâmica ao digitar

                frame_lotes = tk.Frame(quantidade_window, bg="white")
                frame_lotes.pack(pady=10, fill="both", expand=True)

                lotes_lista = tk.Listbox(frame_lotes, font=("Arial", 10), bg="white")
                lotes_lista.pack(side="left", fill="both", expand=True, padx=10)

                scrollbar = ttk.Scrollbar(frame_lotes, orient="vertical", command=lotes_lista.yview)
                lotes_lista.config(yscroll=scrollbar.set)
                scrollbar.pack(side="right", fill="y")

                # Exibir automaticamente todos os lotes disponíveis ao abrir a janela
                buscar_e_exibir_lotes()

                tk.Label(
                    quantidade_window, text="Digite a quantidade:", font=("Arial", 12), bg="white"
                ).pack(pady=10)

                quantidade_entry = tk.Entry(quantidade_window, font=("Arial", 12))
                quantidade_entry.pack(pady=10)
                quantidade_entry.insert(0, "1")

                tk.Button(
                    quantidade_window,
                    text="Confirmar",
                    font=("Arial", 12),
                    bg="green",
                    fg="white",
                    command=confirmar_quantidade,
                ).pack(pady=10)

            pesquisa_window = tk.Toplevel(frame_conteudo)
            pesquisa_window.title("Pesquisar Produto")
            pesquisa_window.geometry("400x300")
            pesquisa_window.configure(bg="white")

            tk.Label(
                pesquisa_window, text="Digite o nome do produto:", font=("Arial", 12), bg="white"
            ).pack(pady=10)

            entry_produto = tk.Entry(pesquisa_window, font=("Arial", 12))
            entry_produto.pack(pady=10, padx=10, fill="x")
            entry_produto.bind("<KeyRelease>", atualizar_resultados)

            frame_resultados = tk.Frame(pesquisa_window, bg="white")
            frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

        def remover_produto():
            try:
                item_selecionado = tabela.selection()[0]
                tabela.delete(item_selecionado)
                self.atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
            except IndexError:
                messagebox.showerror("Erro", "Selecione um produto para remover!")

        botao_adicionar = tk.Button(frame_conteudo, text="Adicionar Produto", command=adicionar_produto)
        botao_adicionar.pack(pady=5)

        botao_remover = tk.Button(frame_conteudo, text="Remover Produto", command=remover_produto)
        botao_remover.pack(pady=5)

        cliente_frame = tk.Frame(frame_conteudo, bg="white")
        cliente_frame.pack(pady=10)

        cliente_label = tk.Label(
            cliente_frame, text="Identificação do Cliente (Opcional):", font=("Arial", 12), bg="white"
        )
        cliente_label.pack(side="left")

        cliente_entry = tk.Entry(cliente_frame, font=("Arial", 12), width=30)
        cliente_entry.pack(side="left", padx=10)

        pagamento_frame = tk.Frame(frame_conteudo, bg="white")
        pagamento_frame.pack(pady=10)

        tk.Label(pagamento_frame, text="Forma de Pagamento:", font=("Arial", 12), bg="white").pack(anchor="w")

        pagamento_var = tk.StringVar(value="Crédito")

        def atualizar_pagamento(*args):
            self.atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)

        pagamento_var.trace_add("write", atualizar_pagamento)

        formas_pagamento = [("Dinheiro", "Dinheiro"), ("Débito", "Débito"), ("Crédito", "Crédito"),
                            ("Crediário", "Crediário")]
        for texto, valor in formas_pagamento:
            tk.Radiobutton(
                pagamento_frame,
                text=texto,
                variable=pagamento_var,
                value=valor,
                font=("Arial", 12),
                bg="white",
            ).pack(anchor="w")

        total_frame = tk.Frame(frame_conteudo, bg="white")
        total_frame.pack(pady=20)

        total_label = tk.Label(
            total_frame, text="TOTAL", font=("Arial", 14, "bold"), bg="white"
        )
        total_label.grid(row=0, column=0, padx=10)

        total_valor = tk.Label(total_frame, text="R$0.00", font=("Arial", 14), bg="white")
        total_valor.grid(row=1, column=0, padx=10)

        avista_label = tk.Label(
            total_frame, text="À VISTA", font=("Arial", 14, "bold"), bg="white"
        )
        avista_label.grid(row=0, column=1, padx=10)

        avista_valor = tk.Label(total_frame, text="R$0.00", font=("Arial", 14), bg="white")
        avista_valor.grid(row=1, column=1, padx=10)

        botoes_frame = tk.Frame(frame_conteudo, bg="white")
        botoes_frame.pack(pady=20)

        def finalizar_venda():
            cliente_id = cliente_entry.get().strip()
            if pagamento_var.get() == "Crediário" and not cliente_id:
                messagebox.showerror("Erro", "Identificação do cliente é obrigatória para o Crediário!")
                return

            itens = []
            for item in tabela.get_children():
                produto, marca, tipo, quantidade, preco, total, id_lote = tabela.item(item, "values")
                produto_id = obter_id_por_nome("produtos", "produto", produto)  # Busca o ID do produto pelo nome
                if not produto_id:
                    messagebox.showerror("Erro", f"Produto '{produto}' não encontrado no banco de dados!")
                    return

                itens.append(
                    {
                        "produto_id": produto_id,
                        "quantidade": int(quantidade),
                        "preco": float(preco),
                        "id_lote": int(id_lote),
                    }
                )

            forma_pagamento = {
                "Dinheiro": 1,
                "Débito": 2,
                "Crédito": 3,
                "Crediário": 4
            }

            # Valida a redução de estoque para cada lote antes de registrar a venda
            for item in itens:
                if not reduzir_quantidade_lote(item["id_lote"], item["quantidade"]):
                    messagebox.showerror(
                        "Erro",
                        f"Estoque insuficiente no lote {item['id_lote']} para o produto '{item['produto_id']}'."
                    )
                    return

            sucesso = registrar_venda(self.id_usuario, cliente_id, itens, forma_pagamento[pagamento_var.get()])
            if sucesso:
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
                self.exibir_realizar_venda(frame_conteudo, self.id_usuario)
            else:
                messagebox.showerror("Erro", "Erro ao registrar a venda.")

        def cancelar_venda():
            """Limpa todos os campos e itens da interface de realizar venda."""
            for item in tabela.get_children():
                tabela.delete(item)
            cliente_entry.delete(0, tk.END)
            pagamento_var.set("Crédito")
            self.atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
            messagebox.showinfo("Cancelado", "Venda cancelada com sucesso!")

        botao_cancelar = tk.Button(
            botoes_frame, text="CANCELAR", font=("Arial", 12, "bold"), bg="red", fg="white", width=10,
            command=cancelar_venda
        )
        botao_cancelar.grid(row=0, column=0, padx=10)

        botao_finalizar = tk.Button(
            botoes_frame,
            text="FINALIZAR",
            font=("Arial", 12, "bold"),
            bg="blue",
            fg="white",
            width=10,
            command=finalizar_venda,
        )
        botao_finalizar.grid(row=0, column=1, padx=10)

    def exibir_historico_vendas(self, frame_conteudo):
        # Limpar o conteúdo existente no frame_conteúdo
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        tk.Label(frame_conteudo, text="Histórico de Vendas", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tabela_frame = tk.Frame(frame_conteudo, bg="white")
        tabela_frame.pack(pady=10, padx=10, fill="x")

        tabela = ttk.Treeview(
            tabela_frame,
            columns=("ID Venda", "Data", "Cliente", "Total"),
            show="headings",
            height=10,
        )
        tabela.heading("ID Venda", text="ID Venda")
        tabela.heading("Data", text="Data")
        tabela.heading("Cliente", text="Cliente")
        tabela.heading("Total", text="Total (R$)")
        tabela.pack(side="left", fill="x", expand=True)

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Simular busca de dados no banco de dados (substitua com sua lógica de consulta ao MySQL)
        from .database import buscar_historico_vendas
        vendas = buscar_historico_vendas(self.id_usuario)

        for venda in vendas:
            tabela.insert("", "end", values=(venda[0], venda[1], venda[2], f"{venda[3]:.2f}"))

    def registrar_venda(self, cliente_id, itens, forma_pagamento):
        return registrar_venda(self.id_usuario, cliente_id, itens, forma_pagamento)

    def buscar_historico_vendas(self):
        return buscar_historico_vendas(self.id_usuario)


