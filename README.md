# SupermercadoCSI
# pip install -r requirements.txt
# python manage.py runserver

# Executar o servidor de desenvolvimento
Para rodar o servidor local do Django, use:

bash
Copiar código
# python manage.py runserver
O Django iniciará um servidor de desenvolvimento na URL http://127.0.0.1:8000/.
Você pode acessar essa URL no navegador para verificar se o projeto está funcionando.

# Outras opções úteis
a) Criar um aplicativo dentro do projeto
Se você precisa criar um app dentro do seu projeto, use:

bash
Copiar código
# python manage.py startapp <nome_do_app>
Exemplo:

bash
Copiar código
# python manage.py startapp blog
b) Verificar migrações pendentes
Certifique-se de que todas as tabelas do banco de dados estejam criadas:

bash
Copiar código
# python manage.py makemigrations
# python manage.py migrate
c) Criar um superusuário
Para acessar a interface administrativa do Django, crie um superusuário:

bash
Copiar código
# python manage.py createsuperuser
Siga as instruções para definir o nome de usuário, e-mail e senha.

d) Parar o servidor
Se precisar interromper o servidor, pressione Ctrl + C no terminal.