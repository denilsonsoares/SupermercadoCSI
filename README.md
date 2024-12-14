
# Seja bem vindo ao códgio do Quase Tudo! Um sistema de gerenciamento de estoque para supermercados. Esse sistema foi desenvolvido empython e possui as seguintes funcionalidades:

# Sistema de Gestão de Perfis

Este é um sistema simples de gestão de usuários, onde o perfil do usuário determina a tela que será exibida. O sistema utiliza a biblioteca `tkinter` para a interface gráfica e realiza a conexão com um banco de dados MySQL para buscar as informações do usuário.

## Funcionalidades

- **Login**: O usuário entra com seu nome de usuário e perfil.
- **Perfil**: Dependendo do perfil do usuário, a tela correspondente é exibida:
  - Caixa
  - Gerente
  - Estoquista
- **Banco de Dados**: Conexão com MySQL para validar o usuário e seu perfil.

## Tecnologias Utilizadas

- [Tkinter](https://docs.python.org/3/library/tkinter.html) para a interface gráfica
- [MySQL](https://www.mysql.com/) para armazenar as informações dos usuários
- [Python](https://www.python.org/) 3.x como linguagem de programação

## Estrutura do Projeto


.
├── modules/
│   ├── login.py        # Tela de Login
│   ├── caixa.py        # Tela de Caixa
│   ├── gerente.py      # Tela de Gerente
│   ├── estoquista.py   # Tela de Estoquista
│   └── db_connection.py # Conexão com o banco de dados
├── main.py             # Arquivo principal que inicia a aplicação
```

## Como Usar

1. Clone o repositório ou faça o download do código.
2. Instale as dependências necessárias:
   ```bash
   pip install mysql-connector-python
   ```
3. Certifique-se de que seu banco de dados MySQL está configurado corretamente com a tabela `usuarios` que deve conter as colunas `username`, `id` e `perfil`.
4. Execute o código principal:
   ```bash
   python main.py
   ```

## Fluxo do Sistema

1. **Tela de Login**: O sistema solicita o nome de usuário e perfil.
2. **Validação**: O sistema consulta o banco de dados para verificar se o usuário e perfil existem.
3. **Tela de Perfil**: Dependendo do perfil, o sistema abre a tela correspondente:
   - Caixa
   - Gerente
   - Estoquista

## Código Principal

```python
import tkinter as tk
from modules.login import tela_login
from modules.caixa import tela_caixa
from modules.gerente import tela_gerente
from modules.estoquista import tela_estoquista
from modules.db_connection import ConexaoSingleton

# Função para obter dados do usuário no banco de dados MySQL
def obter_dados_usuario(username, perfil):
    conexao = ConexaoSingleton().conectar_banco()
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
```

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou correções! Se você encontrar algum erro, por favor, abra um "issue" ou envie um "pull request".

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```

---

Este `README.md` inclui instruções detalhadas sobre como usar o projeto, a estrutura do código e algumas imagens ilustrativas (substituídas pelas figurinhas de exemplo). Você pode substituir os links das imagens pelos links reais ou adicionar as imagens manualmente.
