import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .database import *
from .utils import *
from .common_views import *

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

def alternar_tela_cheia(janela):
    # Toggles between fullscreen and windowed mode
    estado_atual = janela.attributes("-fullscreen")
    janela.attributes("-fullscreen", not estado_atual)

def tela_gerente(gerente, root, tela_login, abrir_tela_perfil):
    janela_gerente = tk.Toplevel()
    janela_gerente.title("Gerente - Quase-Tudo")
    janela_gerente.configure(bg="#f4f4f4")

    # Configure the window to open in fullscreen mode
    janela_gerente.attributes("-fullscreen", True)

    # Variable to control the current content area
    conteudo_atual = None

    # Functions to switch content
    def mostrar_visao_geral():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_visao_geral(conteudo_atual, frame_conteudo)

    def mostrar_gestao_clientes():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_gestao_clientes(conteudo_atual, frame_conteudo, janela_gerente)

    def mostrar_gestao_usuarios():
        nonlocal conteudo_atual
        conteudo_atual = gerente.mostrar_gestao_usuarios(conteudo_atual, frame_conteudo, janela_gerente)

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

    # Menu Lateral - fixed on the left
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

    # Header - fixed at the top
    frame_cabecalho = tk.Frame(janela_gerente, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    # Time - centered at the top
    label_data_hora = tk.Label(frame_cabecalho, bg="#e0e0e0", font=("Arial", 12))
    label_data_hora.place(relx=0.5, rely=0.5, anchor="center")  # Centered horizontally
    atualizar_hora(label_data_hora)

    # User information - aligned to the right
    label_nome = tk.Label(frame_cabecalho, text=gerente.username, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")  # Adjust relx as necessary

    label_id = tk.Label(frame_cabecalho, text=f"Gerente ID {gerente.id_usuario}", bg="#e0e0e0", font=("Arial", 10))
    label_id.place(relx=0.85, rely=0.5, anchor="e")  # Adjust relx as necessary

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

    # Main Content - occupies the rest of the screen
    frame_conteudo = tk.Frame(janela_gerente, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    # Show the Overview when starting
    mostrar_visao_geral()

    janela_gerente.mainloop()
