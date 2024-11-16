import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Banana33@5",
            database="quase_tudo"
        )
        return conexao
    except Error as err:
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
        return None


# Função para adicionar um produto ao estoque
def adicionar_produto(nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade):
    conexao = conectar_banco()
    if conexao is None:
        return False
    cursor = conexao.cursor()

    try:
        cursor.execute('''
            INSERT INTO produtos (Produto, Marca_id, tipo_id, unidade_medida_id, preco_por_unidade)
            VALUES (%s, %s, %s, %s, %s)
        ''', (nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao adicionar produto: {e}")
        return False
    finally:
        conexao.close()


# Função para remover um produto pelo nome
def remover_produto(nome_produto):
    conexao = conectar_banco()
    if conexao is None:
        return False
    cursor = conexao.cursor()

    try:
        cursor.execute('DELETE FROM produtos WHERE Produto = %s', (nome_produto,))
        conexao.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Erro ao remover produto: {e}")
        return False
    finally:
        conexao.close()


# Função para buscar produtos pelo nome
def buscar_produtos(nome_produto):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()

    try:
        cursor.execute('''
            SELECT id, Produto, Marca_id, tipo_id, preco_por_unidade
            FROM produtos
            WHERE Produto LIKE %s
            ORDER BY Produto ASC
        ''', (f"%{nome_produto}%",))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar produtos: {e}")
        return []
    finally:
        conexao.close()


def registrar_venda(vendedor_id, cliente_id, itens):
    """
    Registra uma venda no banco de dados.
    """
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # Se cliente_id estiver vazio, use None para registrar NULL no banco de dados
        cliente_id = cliente_id if cliente_id else None

        # Registrar a venda
        cursor.execute('''
            INSERT INTO vendas (vendedor_id, cliente_id, data_hora)
            VALUES (%s, %s, NOW())
        ''', (vendedor_id, cliente_id))
        venda_id = cursor.lastrowid

        # Registrar os itens vendidos
        for item in itens:
            cursor.execute('''
                INSERT INTO itens_vendidos (venda_id, produto_id, quantidade, preco)
                VALUES (%s, %s, %s, %s)
            ''', (venda_id, item["produto_id"], item["quantidade"], item["preco"]))

        conexao.commit()
        return True
    except mysql.connector.Error as e:
        print(f"Erro ao registrar venda: {e}")
        return False
    finally:
        conexao.close()



# Funções de busca dinâmica
def buscar_marcas(nome_marca):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()

    try:
        cursor.execute('SELECT id, nome_da_marca FROM marcas WHERE nome_da_marca LIKE %s', (f"%{nome_marca}%",))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar marcas: {e}")
        return []
    finally:
        conexao.close()


def buscar_tipos(nome_tipo):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()

    try:
        cursor.execute('SELECT id, tipo FROM tipos_de_produto WHERE tipo LIKE %s', (f"%{nome_tipo}%",))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar tipos: {e}")
        return []
    finally:
        conexao.close()


def buscar_nome_marca_por_id(marca_id):
    conexao = conectar_banco()
    if conexao is None:
        return None
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT nome_da_marca FROM marcas WHERE id = %s", (marca_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Error as e:
        print(f"Erro ao buscar nome da marca: {e}")
        return None
    finally:
        conexao.close()


def buscar_nome_tipo_por_id(tipo_id):
    conexao = conectar_banco()
    if conexao is None:
        return None
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT tipo FROM tipos_de_produto WHERE id = %s", (tipo_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Error as e:
        print(f"Erro ao buscar nome do tipo: {e}")
        return None
    finally:
        conexao.close()


def buscar_unidades(nome_unidade):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()

    try:
        cursor.execute('SELECT id, unidade FROM unidades_de_medida WHERE unidade LIKE %s', (f"%{nome_unidade}%",))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar unidades: {e}")
        return []
    finally:
        conexao.close()


# Função para obter o ID correspondente ao nome
def obter_id_por_nome(tabela, coluna_nome, nome):
    conexao = conectar_banco()
    if conexao is None:
        return None
    cursor = conexao.cursor()

    try:
        cursor.execute(f"SELECT id FROM {tabela} WHERE {coluna_nome} = %s", (nome,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Error as e:
        print(f"Erro ao obter ID por nome: {e}")
        return None
    finally:
        conexao.close()

def buscar_historico_vendas(vendedor_id):
    conexao = conectar_banco()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        cursor.execute('''
            SELECT v.id, v.data_hora, c.nome AS cliente, 
                SUM(iv.quantidade * iv.preco) AS total
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            JOIN itens_vendidos iv ON v.id = iv.venda_id
            WHERE v.vendedor_id = %s
            GROUP BY v.id
            ORDER BY v.data_hora DESC
        ''', (vendedor_id,))
        vendas = cursor.fetchall()
        return vendas
    except mysql.connector.Error as err:
        print(f"Erro ao buscar histórico de vendas: {err}")
        return []
    finally:
        conexao.close()





