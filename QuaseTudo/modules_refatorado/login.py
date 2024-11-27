# login.py

import tkinter as tk
from tkinter import messagebox
from .usuario import Usuario  # Import Usuario class

def verificar_login(callback_login, login_window, event=None):
    username = entry_user.get()
    senha = entry_pass.get()

    usuario = Usuario.autenticar(username, senha)
    if usuario:
        login_window.destroy()
        callback_login(usuario)
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")
