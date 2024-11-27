# gerente.py

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .usuario import Gerente  # Import Gerente class
from .utils import *
from .common_views import *

# Defina o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

def tela_gerente(gerente, root, tela_login, abrir_tela_perfil):
    nome_gerente = gerente.username
    id_gerente = gerente.id_usuario
    # Rest of your code...

    # Update functions to use gerente methods
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
                    # Obter a senha atual do banco de dados
                    senha = gerente.senha  # Assumindo que o gerente sabe sua própria senha

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

    # Similarly update other functions to use gerente methods

    # Rest of your code remains the same
