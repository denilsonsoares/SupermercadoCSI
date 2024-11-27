import tkinter as tk
from modules.login import tela_login
from modules.caixa import tela_caixa
from modules.gerente import tela_gerente
from modules.estoquista import tela_estoquista
from modules.usuario import Gerente, Caixa, Estoquista  # Importar as classes
from modules.db_connection import ConexaoSingleton
from tkinter import messagebox

# Função para autenticar e obter o perfil do usuário
def autenticar_usuario(username, senha):
    """
    Autentica o usuário e retorna uma instância de Gerente, Caixa ou Estoquista, dependendo do perfil.
    """
    conexao = ConexaoSingleton().conectar_banco()
    if not conexao:
        messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")
        return None

    cursor = conexao.cursor()
    try:
        # Busca o usuário pelo nome e senha
        cursor.execute("""
            SELECT id, username, perfil
            FROM usuarios
            WHERE username = %s AND senha = %s
        """, (username, senha))
        usuario = cursor.fetchone()

        if usuario:
            id_usuario, username, perfil = usuario
            if perfil == "Gerente":
                return Gerente(id_usuario, username, None)  # Não armazene a senha para segurança
            elif perfil == "Caixa":
                return Caixa(id_usuario, username, None)
            elif perfil == "Estoquista":
                return Estoquista(id_usuario, username, None)
        return None
    finally:
        cursor.close()


# Função para abrir a tela de perfil com base no perfil do usuário
def abrir_tela_perfil(perfil, username, senha):
    usuario = autenticar_usuario(username, senha)  # Obter instância do usuário
    if not usuario:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")
        return

    if perfil == "Caixa" and isinstance(usuario, Caixa):
        tela_caixa(usuario, root, tela_login, abrir_tela_perfil)
    elif perfil == "Gerente" and isinstance(usuario, Gerente):
        tela_gerente(usuario, root, tela_login, abrir_tela_perfil)
    elif perfil == "Estoquista" and isinstance(usuario, Estoquista):
        tela_estoquista(usuario, root, tela_login, abrir_tela_perfil)
    else:
        messagebox.showerror("Erro", "Perfil não encontrado ou inválido!")


# Função principal
def main():
    global root
    root = tk.Tk()
    root.withdraw()

    tela_login(root, abrir_tela_perfil)  # Passa a função de abertura de perfil para a tela de login


if __name__ == "__main__":
    main()
