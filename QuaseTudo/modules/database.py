import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

# Função para conectar ao banco de dados MySQL
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
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

def buscar_lotes(lote_id, produto_id):
    conexao = conectar_banco()
    if conexao is None:
        return []
    cursor = conexao.cursor()

    try:
        cursor.execute('''
            SELECT id, quantidade, data_de_fabricacao, data_de_vencimento, fornecedor
            FROM lotes
            WHERE id LIKE %s AND produto_id = %s
            ORDER BY data_de_vencimento ASC
        ''', (f"%{lote_id}%", produto_id))
        return cursor.fetchall()
    except Error as e:
        print(f"Erro ao buscar lotes: {e}")
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

def resumo_vendas(periodo='dia'):
    """
    Retorna o total faturado, número de vendas e itens vendidos no período especificado.
    """
    conexao = conectar_banco()
    if not conexao:
        return None

    cursor = conexao.cursor()
    try:
        if periodo == 'dia':
            cursor.execute("""
                SELECT DATE(data_hora) as data,
                       SUM(valor) as total_faturado,
                       COUNT(*) as numero_vendas,
                       SUM((SELECT SUM(quantidade) FROM itens_vendidos WHERE venda_id = vendas.id)) as itens_vendidos
                FROM vendas
                WHERE DATE(data_hora) = CURDATE()
                GROUP BY DATE(data_hora)
            """)
        elif periodo == 'mes':
            cursor.execute("""
                SELECT MONTH(data_hora) as mes,
                       SUM(valor) as total_faturado,
                       COUNT(*) as numero_vendas,
                       SUM((SELECT SUM(quantidade) FROM itens_vendidos WHERE venda_id = vendas.id)) as itens_vendidos
                FROM vendas
                WHERE MONTH(data_hora) = MONTH(CURDATE()) AND YEAR(data_hora) = YEAR(CURDATE())
                GROUP BY MONTH(data_hora)
            """)
        resumo = cursor.fetchone()
        return resumo
    except Error as e:
        print(f"Erro ao obter resumo de vendas: {e}")
        return None
    finally:
        cursor.close()
        conexao.close()

def top_produtos_vendidos(periodo='dia', limite=5):
    """
    Retorna os top produtos mais vendidos no período especificado.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        if periodo == 'dia':
            cursor.execute("""
                SELECT p.Produto, SUM(iv.quantidade) as quantidade_vendida
                FROM itens_vendidos iv
                JOIN produtos p ON iv.produto_id = p.id
                JOIN vendas v ON iv.venda_id = v.id
                WHERE DATE(v.data_hora) = CURDATE()
                GROUP BY p.id
                ORDER BY quantidade_vendida DESC
                LIMIT %s
            """, (limite,))
        elif periodo == 'mes':
            cursor.execute("""
                SELECT p.Produto, SUM(iv.quantidade) as quantidade_vendida
                FROM itens_vendidos iv
                JOIN produtos p ON iv.produto_id = p.id
                JOIN vendas v ON iv.venda_id = v.id
                WHERE MONTH(v.data_hora) = MONTH(CURDATE()) AND YEAR(v.data_hora) = YEAR(CURDATE())
                GROUP BY p.id
                ORDER BY quantidade_vendida DESC
                LIMIT %s
            """, (limite,))
        top_produtos = cursor.fetchall()
        return top_produtos
    except Error as e:
        print(f"Erro ao obter top produtos vendidos: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

# Funções para Gestão de Clientes

def cadastrar_cliente(nome, cpf, telefone):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, cpf, telefone)
            VALUES (%s, %s, %s)
        """, (nome, cpf, telefone))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao cadastrar cliente: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def atualizar_cliente(cliente_id, nome, cpf, telefone):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE clientes
            SET nome = %s, cpf = %s, telefone = %s
            WHERE id = %s
        """, (nome, cpf, telefone, cliente_id))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao atualizar cliente: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def excluir_cliente(cliente_id):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao excluir cliente: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def clientes_compras_recentes(dias=30):
    """
    Retorna os clientes que realizaram compras nos últimos 'dias' dias.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT DISTINCT c.id, c.nome, c.cpf, c.telefone
            FROM clientes c
            JOIN vendas v ON c.id = v.cliente_id
            WHERE v.data_hora >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        """, (dias,))
        clientes = cursor.fetchall()
        return clientes
    except Error as e:
        print(f"Erro ao obter clientes com compras recentes: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

# Funções para Fornecedores

def historico_entregas_fornecedor(fornecedor_id):
    """
    Retorna o histórico de entregas de um fornecedor específico.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT l.id, p.Produto, l.quantidade, l.data_de_fabricacao, l.data_de_vencimento
            FROM lotes l
            JOIN produtos p ON l.produto_id = p.id
            WHERE l.fornecedor = %s
            ORDER BY l.data_de_fabricacao DESC
        """, (fornecedor_id,))
        entregas = cursor.fetchall()
        return entregas
    except Error as e:
        print(f"Erro ao obter histórico de entregas: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

def total_lotes_por_fornecedor():
    """
    Retorna o total de lotes entregues por cada fornecedor.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT f.id, f.nome, COUNT(l.id) as total_lotes
            FROM fornecedores f
            JOIN lotes l ON f.id = l.fornecedor
            GROUP BY f.id
            ORDER BY total_lotes DESC
        """)
        total_lotes = cursor.fetchall()
        return total_lotes
    except Error as e:
        print(f"Erro ao obter total de lotes por fornecedor: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

# Funções para Estoque

def produtos_com_menor_estoque(limite=10):
    """
    Retorna os produtos com menor quantidade em estoque.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT p.id, p.Produto, SUM(l.quantidade) as quantidade_total
            FROM produtos p
            JOIN lotes l ON p.id = l.produto_id
            GROUP BY p.id
            ORDER BY quantidade_total ASC
            LIMIT %s
        """, (limite,))
        produtos = cursor.fetchall()
        return produtos
    except Error as e:
        print(f"Erro ao obter produtos com menor estoque: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

def produtos_proximos_vencimento(dias=30):
    """
    Retorna os produtos com data de vencimento nos próximos 'dias' dias.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT p.id, p.Produto, l.data_de_vencimento, l.quantidade
            FROM produtos p
            JOIN lotes l ON p.id = l.produto_id
            WHERE l.data_de_vencimento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
            ORDER BY l.data_de_vencimento ASC
        """, (dias,))
        produtos = cursor.fetchall()
        return produtos
    except Error as e:
        print(f"Erro ao obter produtos próximos do vencimento: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

def quantidade_inicial_e_restante_lotes():
    """
    Retorna a quantidade inicial e restante de cada lote.
    """
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT l.id, p.Produto, l.quantidade_incial, l.quantidade
            FROM lotes l
            JOIN produtos p ON l.produto_id = p.id
        """)
        lotes = cursor.fetchall()
        return lotes
    except Error as e:
        print(f"Erro ao obter quantidades dos lotes: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

# Funções para Gestão de Usuários

def adicionar_usuario(username, senha, perfil):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (username, senha, perfil)
            VALUES (%s, %s, %s)
        """, (username, senha, perfil))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao adicionar usuário: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def editar_usuario(usuario_id, username, senha, perfil):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE usuarios
            SET username = %s, senha = %s, perfil = %s
            WHERE id = %s
        """, (username, senha, perfil, usuario_id))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao editar usuário: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def excluir_usuario(usuario_id):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao excluir usuário: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def listar_usuarios():
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id, username, perfil FROM usuarios")
        usuarios = cursor.fetchall()
        return usuarios
    except Error as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

# Funções para Gestão de Produtos

def cadastrar_produto(nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade):
    return adicionar_produto(nome_produto, marca_id, tipo_id, unidade_medida_id, preco_por_unidade)

def atualizar_preco_produto(produto_id, novo_preco):
    conexao = conectar_banco()
    if not conexao:
        return False

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            UPDATE produtos
            SET preco_por_unidade = %s
            WHERE id = %s
        """, (novo_preco, produto_id))
        conexao.commit()
        return True
    except Error as e:
        print(f"Erro ao atualizar preço do produto: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()

def consultar_produtos(filtro_marca=None, filtro_tipo=None, filtro_estoque=False):
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        query = """
            SELECT p.id, p.Produto, m.nome_da_marca, t.tipo, p.preco_por_unidade
            FROM produtos p
            JOIN marcas m ON p.Marca_id = m.id
            JOIN tipos_de_produto t ON p.tipo_id = t.id
        """
        params = []

        if filtro_marca or filtro_tipo or filtro_estoque:
            query += " WHERE"
            conditions = []
            if filtro_marca:
                conditions.append(" m.nome_da_marca LIKE %s")
                params.append(f"%{filtro_marca}%")
            if filtro_tipo:
                conditions.append(" t.tipo LIKE %s")
                params.append(f"%{filtro_tipo}%")
            if filtro_estoque:
                conditions.append(" (SELECT SUM(l.quantidade) FROM lotes l WHERE l.produto_id = p.id) > 0")
            query += " AND".join(conditions)

        cursor.execute(query, tuple(params))
        produtos = cursor.fetchall()
        return produtos
    except Error as e:
        print(f"Erro ao consultar produtos: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

def visualizar_lotes_produto(produto_id):
    conexao = conectar_banco()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT l.id, l.data_de_fabricacao, l.data_de_vencimento, l.quantidade
            FROM lotes l
            WHERE l.produto_id = %s
        """, (produto_id,))
        lotes = cursor.fetchall()
        return lotes
    except Error as e:
        print(f"Erro ao visualizar lotes do produto: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()





