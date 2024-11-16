import tkinter as tk
from tkinter import messagebox
import mysql.connector
from .database import conectar_banco

# Função para verificar login
def verificar_login(callback_login, login_window, event=None):
    username = entry_user.get()
    senha = entry_pass.get()

    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        # Consulta para verificar o login
        cursor.execute("SELECT perfil FROM usuarios WHERE username=%s AND senha=%s", (username, senha))
        result = cursor.fetchone()
    finally:
        cursor.close()
        conexao.close()

    if result:
        perfil = result[0]
        login_window.destroy()  # Fecha a janela de login
        callback_login(perfil, username)  # Passa o perfil e o username para redirecionar
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Funções para manipular o placeholder
def on_entry_click(event, entry, placeholder_text):
    """Função para remover o placeholder quando o campo é clicado"""
    if entry.get() == placeholder_text:
        entry.delete(0, "end")
        entry.config(fg="black")

def on_focusout(event, entry, placeholder_text):
    """Função para recolocar o placeholder se o campo estiver vazio ao perder o foco"""
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")

# Função para a tela de login
def tela_login(root, callback_login):
    global entry_user, entry_pass  # Definindo como globais para serem acessadas na função de login

    # Cria a janela de login em tela cheia
    login_window = tk.Toplevel(root)
    login_window.title("Login - Quase-Tudo")
    login_window.attributes("-fullscreen", True)
    login_window.configure(bg="white")

    # Frame central para posicionar o conteúdo mais para baixo
    frame_central = tk.Frame(login_window, bg="white")
    frame_central.pack(expand=True)  # expand=True centraliza o frame verticalmente

    # Logo e Título
    logo_label = tk.Label(frame_central, text="QT", font=("Arial", 48, "bold"), bg="white")
    logo_label.pack(pady=(0, 10))  # Espaço entre logo e subtítulo

    subtitulo_label = tk.Label(frame_central, text="Quase-Tudo", font=("Arial", 18), bg="white")
    subtitulo_label.pack()

    welcome_label = tk.Label(frame_central, text="Bem-vindo à plataforma Quase-Tudo", font=("Arial", 12), bg="white")
    welcome_label.pack(pady=10)

    # Entrada de Usuário com placeholder
    entry_user = tk.Entry(frame_central, font=("Arial", 12), fg="grey")
    entry_user.insert(0, "Nome de usuário")
    entry_user.bind("<FocusIn>", lambda event: on_entry_click(event, entry_user, "Nome de usuário"))
    entry_user.bind("<FocusOut>", lambda event: on_focusout(event, entry_user, "Nome de usuário"))
    entry_user.pack(pady=10)

    # Entrada de Senha com placeholder
    entry_pass = tk.Entry(frame_central, show="*", font=("Arial", 12), fg="grey")
    entry_pass.insert(0, "Sua senha")
    entry_pass.bind("<FocusIn>", lambda event: on_entry_click(event, entry_pass, "Sua senha"))
    entry_pass.bind("<FocusOut>", lambda event: on_focusout(event, entry_pass, "Sua senha"))
    entry_pass.pack(pady=10)

    # Botão de Login
    login_button = tk.Button(frame_central, text="ENTRAR", font=("Arial", 12, "bold"), bg="#007bff", fg="white",
                              command=lambda: verificar_login(callback_login, login_window))
    login_button.pack(pady=20)

    # Informações de Suporte
    support_label = tk.Label(frame_central,
                             text="Suporte\n e-mail: plataformaquasetudo@gmail.com\n telefone: (77) 99823-5006",
                             font=("Arial", 10), bg="white", justify="center")
    support_label.pack(pady=20)

    # Evento para a tecla Enter
    login_window.bind("<Return>", lambda event: verificar_login(callback_login, login_window, event))

    login_window.mainloop()
