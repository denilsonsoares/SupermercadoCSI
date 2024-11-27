import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .database import *
from .utils import *
from .common_views import *

# Defina o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

def alternar_tela_cheia(janela):
    # Alterna entre tela cheia e janela normal
    estado_atual = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not estado_atual)

def tela_gerente(gerente, root, tela_login, abrir_tela_perfil):
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
                if gerente.cadastrar_cliente(nome, cpf, telefone):
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
                if gerente.atualizar_cliente(cliente_id, nome, cpf, telefone):
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
                if gerente.excluir_cliente(cliente_id):
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
        clientes = gerente.clientes_compras_recentes(dias=30)
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Nome", "CPF", "Telefone"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("CPF", text="CPF")
        tree.heading("Telefone", text="Telefone")
        tree.pack(fill="both", expand=True)
        for cliente in clientes:
            tree.insert("", "end", values=cliente)

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
                if gerente.adicionar_usuario(username, senha, perfil):
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
                    # Se a senha não foi alterada, mantenha a senha atual
                    senha = None  # Handle this in your `editar_usuario` method
                if gerente.editar_usuario(usuario_id, username, senha, perfil):
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
                if gerente.excluir_usuario(usuario_id):
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
        usuarios = gerente.listar_usuarios()
        tree = ttk.Treeview(conteudo_atual, columns=("ID", "Username", "Perfil"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Username", text="Username")
        tree.heading("Perfil", text="Perfil")
        tree.pack(fill="both", expand=True)
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)

    # Common Views
    def chamar_mostrar_fornecedores():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_fornecedores(conteudo_atual, frame_conteudo, janela_gerente)

    def chamar_mostrar_estoque():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_estoque(conteudo_atual, frame_conteudo)

    def chamar_mostrar_gestao_produtos():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_gerente)

    def chamar_registrar_lote():
        gerente.registrar_lote_interface(janela_gerente)

    # Menu Lateral - fixo à esquerda
    frame_menu = tk.Frame(janela_gerente, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

    botoes_menu = [
        ("Visão Geral", mostrar_visao_geral),
        ("Gestão de Clientes", mostrar_gestao_clientes),
        ("Fornecedores", chamar_mostrar_fornecedores),
        ("Estoque", chamar_mostrar_estoque),
        ("Gestão de Usuários", mostrar_gestao_usuarios),
        ("Gestão de Produtos", chamar_mostrar_gestao_produtos),
        ("Registrar Lote", chamar_registrar_lote),
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
    label_nome = tk.Label(frame_cabecalho, text=gerente.username, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")  # Ajuste relx conforme necessário

    label_id = tk.Label(frame_cabecalho, text=f"Gerente ID {gerente.id_usuario}", bg="#e0e0e0", font=("Arial", 10))
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
