import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
from .utils import *
from .common_views import *

# Caminho base relativo
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")


# Função principal para a tela do Estoquista
def tela_estoquista(estoquista, root, tela_login, abrir_tela_perfil):
    """
    Tela principal do estoquista.
    :param estoquista: Instância da classe Estoquista.
    """
    janela_estoquista = tk.Toplevel()
    janela_estoquista.title("Estoquista - Quase-Tudo")
    janela_estoquista.geometry("1000x700")
    janela_estoquista.configure(bg="#f4f4f4")
    janela_estoquista.attributes("-fullscreen", True)

    # Variável para controlar a área de conteúdo atual
    conteudo_atual = None

    # Funções para alternar o conteúdo
    def chamar_mostrar_fornecedores():
        nonlocal conteudo_atual
        conteudo_atual = estoquista.mostrar_fornecedores(conteudo_atual, frame_conteudo, janela_estoquista)

    def chamar_mostrar_estoque():
        nonlocal conteudo_atual
        conteudo_atual = estoquista.mostrar_estoque(conteudo_atual, frame_conteudo)

    def chamar_mostrar_gestao_produtos():
        nonlocal conteudo_atual
        conteudo_atual = estoquista.mostrar_gestao_produtos(conteudo_atual, frame_conteudo, janela_estoquista)

    def chamar_registrar_lote():
        estoquista.registrar_lote_interface(janela_estoquista)

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

    # Cabeçalho - fixo na parte superior
    frame_cabecalho = tk.Frame(janela_estoquista, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    label_nome = tk.Label(frame_cabecalho, text=estoquista.username, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")

    label_id = tk.Label(frame_cabecalho, text=f"Estoquista ID {estoquista.id_usuario}", bg="#e0e0e0", font=("Arial", 10))
    label_id.place(relx=0.85, rely=0.5, anchor="e")

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0").place(relx=0.9, rely=0.5, anchor="e")

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(frame_cabecalho, image=imagem_logout, bg="#e0e0e0", bd=0,
                             command=lambda: logout(janela_estoquista, root, tela_login, abrir_tela_perfil))
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    # Conteúdo Principal - ocupa o restante da tela
    frame_conteudo = tk.Frame(janela_estoquista, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    # Mostrar Estoque ao iniciar
    chamar_mostrar_estoque()

    janela_estoquista.mainloop()
