from sql_connection import get_sql_connection

def get_all_lotes(connection):
    """
    Retorna todos os lotes comprados com detalhes.
    """
    query = """
    SELECT 
        Lotes_comprados.id,
        Produtos.Produto,
        Lotes_comprados.preco_de_compra,
        Lotes_comprados.data_de_fabricacao,
        Lotes_comprados.data_de_vencimento,
        Lotes_comprados.quantidade_por_udm,
        Fornecedores.nome AS fornecedor
    FROM Lotes_comprados
    JOIN Produtos ON Lotes_comprados.produto_id = Produtos.id
    JOIN Fornecedores ON Lotes_comprados.fornecedor = Fornecedores.id;
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    lotes = cursor.fetchall()
    return lotes

def insert_new_lote(connection, lote):
    """
    Insere um novo lote no banco de dados.
    :param lote: Dicionário com os dados do lote:
        {
            'produto_id': 1,
            'preco_de_compra': 100,
            'data_de_fabricacao': '2024-01-01',
            'data_de_vencimento': '2025-01-01',
            'quantidade_por_udm': 50,
            'fornecedor': 1
        }
    """
    query = """
    INSERT INTO Lotes_comprados (produto_id, preco_de_compra, data_de_fabricacao, data_de_vencimento, quantidade_por_udm, fornecedor)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    data = (
        lote['produto_id'],
        lote['preco_de_compra'],
        lote['data_de_fabricacao'],
        lote['data_de_vencimento'],
        lote['quantidade_por_udm'],
        lote['fornecedor']
    )
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid