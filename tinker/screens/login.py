import tkinter as tk
from tkinter import font

def on_login():
    username = entry_username.get()
    password = entry_password.get()
    # Aqui você pode adicionar a lógica de validação
    print(f"Usuário: {username}, Senha: {password}")

# Configuração da janela principal
root = tk.Tk()
root.title("Quase-Tudo - Login")
root.geometry("700x600")
root.configure(bg="white")

# Fonte personalizada para o título
title_font = font.Font(family="Helvetica", size=24, weight="bold")
subtitle_font = font.Font(family="Helvetica", size=10)

# Logo e título
label_logo = tk.Label(root, text="QT", font=title_font, fg="black", bg="white")
label_logo.pack(pady=(20, 5))

label_title = tk.Label(root, text="Quase-Tudo", font=("Helvetica", 14), fg="black", bg="white")
label_title.pack()

label_welcome = tk.Label(root, text="Bem-vindo à plataforma Quase-Tudo", font=("Helvetica", 10), fg="black", bg="white")
label_welcome.pack(pady=(10, 20))

# Campo de nome de usuário
entry_username = tk.Entry(root, font=("Helvetica", 10), width=30)
entry_username.insert(0, "Insira seu nome de usuário")
entry_username.pack(pady=5)

# Campo de senha
entry_password = tk.Entry(root, font=("Helvetica", 10), width=30, show="*")
entry_password.insert(0, "Insira sua senha")
entry_password.pack(pady=5)

# Botão de login
button_login = tk.Button(root, text="ENTRAR", font=("Helvetica", 10, "bold"), bg="#007BFF", fg="white", width=20, command=on_login)
button_login.pack(pady=15)

# Informações de suporte
label_support = tk.Label(root, text="Suporte\nE-mail: plataformaquasetudo@gmail.com\nTelefone: (77) 99823-5006", font=subtitle_font, fg="gray", bg="white")
label_support.pack(pady=(20, 0))

root.mainloop()
