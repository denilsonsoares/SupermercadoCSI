import tkinter as tk
from modules.login import tela_login
from modules.caixa import tela_caixa
from modules.gerente import tela_gerente
from modules.estoquista import tela_estoquista
from modules.database import conectar_banco

# Função para obter dados do usuário no banco de dados MySQL
def obter_dados_usuario(username, perfil):
    conexao = conectar_banco()
    if conexao is None:
        return ("", "")
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT username, id FROM usuarios WHERE username=%s AND perfil=%s", (username, perfil))
        result = cursor.fetchone()
        return result if result else ("", "")
    finally:
        cursor.close()


# Função para abrir a tela de perfil com base no perfil do usuário
def abrir_tela_perfil(perfil, username):
    nome_usuario, id_usuario = obter_dados_usuario(username, perfil)
    
    if perfil == "Caixa":
        tela_caixa(nome_usuario, id_usuario, root, tela_login, abrir_tela_perfil)
    elif perfil == "Gerente":
        tela_gerente(nome_usuario, id_usuario, root, tela_login, abrir_tela_perfil)
    elif perfil == "Estoquista":
        tela_estoquista(nome_usuario, id_usuario, root, tela_login, abrir_tela_perfil)
    else:
        tk.messagebox.showerror("Erro", "Perfil não encontrado!")

# Função principal
def main():
    global root
    root = tk.Tk()
    root.withdraw()

    tela_login(root, abrir_tela_perfil)

if __name__ == "__main__":
    main()

