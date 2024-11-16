import os
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk

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

    # Menu Lateral - fixo à esquerda
    frame_menu = tk.Frame(janela_gerente, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(frame_menu, text="QT\nQuase-Tudo", bg="#d3d3d3", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

    botoes_menu = ["Visão Geral", "Relatórios", "Clientes", "Gestão Funcionários", "Configurações"]
    for botao in botoes_menu:
        tk.Button(frame_menu, text=botao, font=("Arial", 12), bg="#d3d3d3", fg="black", bd=0, relief="flat", activebackground="#a9a9a9", activeforeground="white").pack(fill="x", pady=10)

    # Cabeçalho - fixo na parte superior
    frame_cabecalho = tk.Frame(janela_gerente, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    # Hora - centralizado na parte superior
    label_data_hora = tk.Label(frame_cabecalho, bg="#e0e0e0", font=("Arial", 12))
    label_data_hora.place(relx=0.5, rely=0.5, anchor="center")  # Centralizado horizontalmente
    atualizar_hora(label_data_hora)

    # Informações do usuário - alinhadas à direita
    label_nome = tk.Label(frame_cabecalho, text=nome_gerente, bg="#e0e0e0", font=("Arial", 12, "bold"))
    label_nome.place(relx=0.75, rely=0.5, anchor="e")  # Ajuste `relx` conforme necessário

    label_id = tk.Label(frame_cabecalho, text=f"Gerente ID {id_gerente}", bg="#e0e0e0", font=("Arial", 10))
    label_id.place(relx=0.85, rely=0.5, anchor="e")  # Ajuste `relx` conforme necessário

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    label_imagem_usuario = tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0")
    label_imagem_usuario.image = imagem_usuario
    label_imagem_usuario.place(relx=0.9, rely=0.5, anchor="e")

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(frame_cabecalho, image=imagem_logout, bg="#e0e0e0", bd=0, command=lambda: logout(janela_gerente, root, tela_login, abrir_tela_perfil))
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    # Conteúdo Principal - ocupa o restante da tela
    frame_conteudo = tk.Frame(janela_gerente, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_conteudo, text="Tela de Gerente", font=("Arial", 20, "bold"), bg="white").pack(pady=50)

    janela_gerente.mainloop()
