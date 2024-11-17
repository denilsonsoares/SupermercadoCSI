import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from .database import *

# Defina o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

def atualizar_hora(label):
    def atualizar():
        agora = datetime.now()
        label.config(text=agora.strftime("%d / %m / %Y  %H:%M"))
        label.after(1000, atualizar)
    atualizar()

def logout(janela, root, tela_login, abrir_tela_perfil):
    janela.destroy()
    tela_login(root, abrir_tela_perfil)

def alternar_tela_cheia(janela):
    # Alterna entre tela cheia e janela normal
    estado_atual = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not estado_atual)

def tela_gerente(nome_gerente, id_gerente, root, tela_login, abrir_tela_perfil):
    janela_gerente = tk.Toplevel()
    janela_gerente.title("Gerente - Quase-Tudo")
    janela_gerente.configure(bg="#f4f4f4")

    # Configurar a janela para abrir em modo de tela cheia
    janela_gerente.attributes("-fullscreen", True)

    # Variável para controlar a área de conteúdo atual
    conteudo_atual = None

    # Funções para alternar o conteúdo
    def mostrar_visao_geral():
        nonlocal conteudo_atual
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

    def mostrar_gestao_clientes():
        def cadastrar_cliente_interface():
            janela_cadastrar = tk.Toplevel(janela_gerente)
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
                if cadastrar_cliente(nome, cpf, telefone):
                    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
                    janela_cadastrar.destroy()
                    mostrar_gestao_clientes()
                else:
                    messagebox.showerror("Erro", "Erro ao cadastrar cliente.")

            tk.Button(janela_cadastrar, text="Salvar", command=salvar_cliente).pack(pady=10)

        def atualizar_cliente_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um cliente para atualizar.")
                return
            cliente_id, nome_atual, cpf_atual, telefone_atual = tree.item(selected_item)['values']

            janela_atualizar = tk.Toplevel(janela_gerente)
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
                if atualizar_cliente(cliente_id, nome, cpf, telefone):
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                    janela_atualizar.destroy()
                    mostrar_gestao_clientes()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar cliente.")

            tk.Button(janela_atualizar, text="Salvar", command=salvar_alteracoes).pack(pady=10)

        def excluir_cliente_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
                return
            cliente_id = tree.item(selected_item)['values'][0]
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?")
            if resposta:
                if excluir_cliente(cliente_id):
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    mostrar_gestao_clientes()
                else:
                    messagebox.showerror("Erro", "Erro ao excluir cliente.")

        nonlocal conteudo_atual
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Clientes", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Implementar as funcionalidades de cadastro, atualização e exclusão de clientes
        frame_acoes = tk.Frame(conteudo_atual, bg="white")
        frame_acoes.pack(pady=10)

        tk.Button(frame_acoes, text="Cadastrar Cliente", command=cadastrar_cliente_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Atualizar Cliente", command=atualizar_cliente_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Excluir Cliente", command=excluir_cliente_interface).pack(side="left", padx=5)

        # Listar clientes que realizaram compras recentemente
        tk.Label(conteudo_atual, text="Clientes com Compras Recentes:", bg="white", font=("Arial", 14, "bold")).pack(
            pady=10)
        clientes = clientes_compras_recentes(dias=30)
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Nome", "CPF", "Telefone"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("CPF", text="CPF")
        tree.heading("Telefone", text="Telefone")
        tree.pack(fill="both", expand=True)
        for cliente in clientes:
            tree.insert("", "end", values=cliente)


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

            janela_historico = tk.Toplevel(janela_gerente)
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

        # Frame direito (Produtos Próximos do Vencimento)
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

        # Tabela: Produtos Próximos do Vencimento
        tk.Label(frame_direito, text="Produtos Próximos do Vencimento:", bg="white", font=("Arial", 14, "bold")).pack(
            pady=10)
        produtos_vencimento = produtos_proximos_vencimento()
        tree_vencimento = ttk.Treeview(frame_direito, columns=("ID", "Produto", "Data de Vencimento", "Quantidade"),
                                       show="headings")
        tree_vencimento.heading("ID", text="ID")
        tree_vencimento.heading("Produto", text="Produto")
        tree_vencimento.heading("Data de Vencimento", text="Data de Vencimento")
        tree_vencimento.heading("Quantidade", text="Quantidade")
        tree_vencimento.pack(fill="both", expand=True)
        for produto in produtos_vencimento:
            tree_vencimento.insert("", "end", values=produto)

        # Frame inferior para a tabela de Quantidade Inicial e Restante dos Lotes
        frame_inferior = tk.Frame(conteudo_atual, bg="white")
        frame_inferior.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Tabela: Quantidade Inicial e Restante dos Lotes
        tk.Label(frame_inferior, text="Quantidade Inicial e Restante dos Lotes:", bg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)
        lotes_quantidades = quantidade_inicial_e_restante_lotes()
        tree_lotes = ttk.Treeview(frame_inferior,
                                  columns=(
                                  "Lote ID", "Produto", "Marca", "Quantidade Inicial", "Quantidade Restante"),
                                  show="headings")
        tree_lotes.heading("Lote ID", text="Lote ID")
        tree_lotes.heading("Produto", text="Produto")
        tree_lotes.heading("Marca", text="Marca")
        tree_lotes.heading("Quantidade Inicial", text="Quantidade Inicial")
        tree_lotes.heading("Quantidade Restante", text="Quantidade Restante")
        tree_lotes.pack(fill="both", expand=True)
        for lote in lotes_quantidades:
            tree_lotes.insert("", "end", values=lote)

    def mostrar_gestao_usuarios():

        def adicionar_usuario_interface():
            janela_adicionar = tk.Toplevel(janela_gerente)
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
                if adicionar_usuario(username, senha, perfil):
                    messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
                    janela_adicionar.destroy()
                    mostrar_gestao_usuarios()
                else:
                    messagebox.showerror("Erro", "Erro ao adicionar usuário.")

            tk.Button(janela_adicionar, text="Salvar", command=salvar_usuario).pack(pady=10)

        def editar_usuario_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
                return
            usuario_id, username_atual, perfil_atual = tree.item(selected_item)['values']

            janela_editar = tk.Toplevel(janela_gerente)
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
                    # Obter a senha atual do banco de dados
                    conexao = conectar_banco()
                    cursor = conexao.cursor()
                    cursor.execute("SELECT senha FROM usuarios WHERE id = %s", (usuario_id,))
                    senha = cursor.fetchone()[0]
                    cursor.close()
                    
                if editar_usuario(usuario_id, username, senha, perfil):
                    messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
                    janela_editar.destroy()
                    mostrar_gestao_usuarios()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar usuário.")

            tk.Button(janela_editar, text="Salvar", command=salvar_alteracoes).pack(pady=10)

        def excluir_usuario_interface():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
                return
            usuario_id = tree.item(selected_item)['values'][0]
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?")
            if resposta:
                if excluir_usuario(usuario_id):
                    messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                    mostrar_gestao_usuarios()
                else:
                    messagebox.showerror("Erro", "Erro ao excluir usuário.")

        nonlocal conteudo_atual
        if conteudo_atual:
            conteudo_atual.destroy()
        conteudo_atual = tk.Frame(frame_conteudo, bg="white")
        conteudo_atual.pack(fill="both", expand=True)

        tk.Label(conteudo_atual, text="Gestão de Usuários", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        frame_acoes = tk.Frame(conteudo_atual, bg="white")
        frame_acoes.pack(pady=10)

        tk.Button(frame_acoes, text="Adicionar Usuário", command=adicionar_usuario_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Editar Usuário", command=editar_usuario_interface).pack(side="left", padx=5)
        tk.Button(frame_acoes, text="Excluir Usuário", command=excluir_usuario_interface).pack(side="left", padx=5)

        # Listar usuários
        tk.Label(conteudo_atual, text="Lista de Usuários:", bg="white", font=("Arial", 14, "bold")).pack(pady=10)
        usuarios = listar_usuarios()
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Username", "Perfil"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Perfil", text="Perfil")
        tree.pack(fill="both", expand=True)
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)



    def mostrar_gestao_produtos():

        def cadastrar_produto_interface():
            janela_cadastrar = tk.Toplevel(janela_gerente)
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

            janela_atualizar = tk.Toplevel(janela_gerente)
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

            janela_lotes = tk.Toplevel(janela_gerente)
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
    frame_menu = tk.Frame(janela_gerente, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

    botoes_menu = [
        ("Visão Geral", mostrar_visao_geral),
        ("Gestão de Clientes", mostrar_gestao_clientes),
        ("Fornecedores", mostrar_fornecedores),
        ("Estoque", mostrar_estoque),
        ("Gestão de Usuários", mostrar_gestao_usuarios),
        ("Gestão de Produtos", mostrar_gestao_produtos),
    ]
    for texto, comando in botoes_menu:
        tk.Button(frame_menu, text=texto, font=("Arial", 12), bg="#d3d3d3", fg="black", bd=0, relief="flat",
                  activebackground="#a9a9a9", activeforeground="white", command=comando).pack(fill="x", pady=10)

    # Cabeçalho - fixo na parte superior
    frame_cabecalho = tk.Frame(janela_gerente, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    # Hora - centralizado na parte superior
    label_data_hora = tk.Label(frame_cabecalho, bg="#e0e0e0", font=("Arial", 12))
    label_data_hora.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado horizontalmente
    atualizar_hora(label_data_hora)

    # Informações do usuário - alinhadas à direita
    label_nome = tk.Label(frame_cabecalho, text=nome_gerente, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")  # Ajuste relx conforme necessário

    label_id = tk.Label(frame_cabecalho, text=f"Gerente ID {id_gerente}", bg="#e0e0e0", font=("Arial", 10))
    label_id.place(relx=0.85, rely=0.5, anchor="e")  # Ajuste relx conforme necessário

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    label_imagem_usuario = tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0")
    label_imagem_usuario.image = imagem_usuario
    label_imagem_usuario.place(relx=0.9, rely=0.5, anchor="e")

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(frame_cabecalho, image=imagem_logout, bg="#e0e0e0", bd=0,
                             command=lambda: logout(janela_gerente, root, tela_login, abrir_tela_perfil))
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    # Conteúdo Principal - ocupa o restante da tela
    frame_conteudo = tk.Frame(janela_gerente, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    # Mostrar a Visão Geral ao iniciar
    mostrar_visao_geral()

    janela_gerente.mainloop()