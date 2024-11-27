import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .utils import *
from .db_connection import ConexaoSingleton

# Caminho base relativo
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")


def tela_caixa(caixa, root, tela_login, abrir_tela_perfil):
    """
    Tela principal do caixa.
    :param caixa: Instância da classe Caixa.
    """
    janela_caixa = tk.Toplevel()
    janela_caixa.title("Caixa - Quase-Tudo")
    janela_caixa.geometry("1000x700")
    janela_caixa.configure(bg="#f4f4f4")
    janela_caixa.attributes("-fullscreen", True)

    frame_menu = tk.Frame(janela_caixa, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(
        frame_menu,
        text="QT\nQuase-Tudo",
        bg="#d3d3d3",
        font=("Arial", 16, "bold"),
        fg="black",
    ).pack(pady=20)

    # Variável para controlar a área de conteúdo atual
    frame_conteudo = tk.Frame(janela_caixa, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    def exibir_realizar_venda():
        # Limpar o conteúdo existente
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        # Implementar a interface de realizar venda usando métodos da classe Caixa
        caixa.realizar_venda_interface(frame_conteudo)

    def exibir_historico_vendas():
        # Limpar o conteúdo existente
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

        # Implementar a interface de histórico de vendas usando métodos da classe Caixa
        caixa.exibir_historico_vendas(frame_conteudo)

    realizar_venda_button = tk.Button(
        frame_menu,
        text="Realizar venda",
        font=("Arial", 12),
        bg="#d3d3d3",
        fg="black",
        bd=0,
        relief="flat",
        activebackground="#a9a9a9",
        activeforeground="white",
        command=exibir_realizar_venda,
    )
    realizar_venda_button.pack(fill="x", pady=10)

    historico_vendas_button = tk.Button(
        frame_menu,
        text="Histórico de Vendas",
        font=("Arial", 12),
        bg="#d3d3d3",
        fg="black",
        bd=0,
        relief="flat",
        activebackground="#a9a9a9",
        activeforeground="white",
        command=exibir_historico_vendas,
    )
    historico_vendas_button.pack(fill="x", pady=10)

    frame_cabecalho = tk.Frame(janela_caixa, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    label_data_hora = tk.Label(frame_cabecalho, bg="#e0e0e0", font=("Arial", 12))
    label_data_hora.place(relx=0.5, rely=0.5, anchor="center")
    atualizar_hora(label_data_hora)

    label_nome = tk.Label(
        frame_cabecalho, text=caixa.username, bg="#e0e0e0", font=("Arial", 12, "bold")
    )
    label_nome.place(relx=0.75, rely=0.5, anchor="e")

    label_id = tk.Label(
        frame_cabecalho,
        text=f"Caixa ID {caixa.id_usuario}",
        bg="#e0e0e0",
        font=("Arial", 10),
    )
    label_id.place(relx=0.85, rely=0.5, anchor="e")

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0").place(
        relx=0.9, rely=0.5, anchor="e"
    )

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(
        frame_cabecalho,
        image=imagem_logout,
        bg="#e0e0e0",
        bd=0,
        command=lambda: logout(janela_caixa, root, tela_login, abrir_tela_perfil),
    )
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    # Carregar automaticamente a tela de "Realizar Venda"
    exibir_realizar_venda()

    janela_caixa.mainloop()
