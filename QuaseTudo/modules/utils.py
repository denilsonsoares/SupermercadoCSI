from datetime import datetime
# Função para atualizar o horário
def atualizar_hora(label):
    def atualizar():
        agora = datetime.now()
        label.config(text=agora.strftime("%d / %m / %Y  %H:%M"))
        label.after(1000, atualizar)
    atualizar()

# Função de logout
def logout(janela, root, tela_login, abrir_tela_perfil):
    janela.destroy()
    tela_login(root, abrir_tela_perfil)