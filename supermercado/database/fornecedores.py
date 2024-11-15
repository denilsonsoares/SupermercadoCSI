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


def update_lote(connection, lote_id, updated_data):
    """
    Atualiza os dados de um lote.
    :param updated_data: Dicionário com os campos a serem atualizados:
        Exemplo: {'preco_de_compra': 120.0, 'quantidade_por_udm': 60}
    """
    set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
    query = f"UPDATE Lotes_comprados SET {set_clause} WHERE id = %s;"
    data = list(updated_data.values()) + [lote_id]

    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    return cursor.rowcount

def delete_lote(connection, lote_id):
    """
    Remove um lote pelo ID.
    """
    try:
        query = "DELETE FROM Lotes_comprados WHERE id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (lote_id,))
        connection.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Erro ao deletar lote: {e}")
        return 0

if __name__ == "__main__":
    from sql_connection import get_sql_connection

    connection = get_sql_connection()

    # Testando inserção de novos lotes
    print("\n### INSERINDO NOVOS LOTES ###")
    new_lote1 = {
        'produto_id': 1,  # Certifique-se de que este ID de produto existe
        'preco_de_compra': 100.0,
        'data_de_fabricacao': '2024-01-01',
        'data_de_vencimento': '2025-01-01',
        'quantidade_por_udm': 50,
        'fornecedor': 1  # Certifique-se de que este ID de fornecedor existe
    }
    new_lote2 = {
        'produto_id': 2,  # Certifique-se de que este ID de produto existe
        'preco_de_compra': 200.0,
        'data_de_fabricacao': '2024-06-01',
        'data_de_vencimento': '2026-06-01',
        'quantidade_por_udm': 100,
        'fornecedor': 1
    }
    lote_id1 = insert_new_lote(connection, new_lote1)
    lote_id2 = insert_new_lote(connection, new_lote2)
    print(f"Lotes inseridos com IDs: {lote_id1}, {lote_id2}")

    # Testando listagem de lotes
    print("\n### LISTANDO TODOS OS LOTES ###")
    lotes = get_all_lotes(connection)
    for lote in lotes:
        print(lote)

    # Testando atualização de um lote
    print("\n### ATUALIZANDO UM LOTE ###")
    updated_data = {
        'preco_de_compra': 150.0,
        'quantidade_por_udm': 75
    }
    rows_updated = update_lote(connection, lote_id1, updated_data)
    print(f"Número de lotes atualizados: {rows_updated}")

    # Listando novamente para verificar atualização
    print("\n### LOTES APÓS ATUALIZAÇÃO ###")
    lotes = get_all_lotes(connection)
    for lote in lotes:
        print(lote)

    # Testando exclusão de lotes
    print("\n### EXCLUINDO LOTES ###")
    rows_deleted1 = delete_lote(connection, lote_id1)
    rows_deleted2 = delete_lote(connection, lote_id2)
    print(f"Número de lotes deletados: {rows_deleted1 + rows_deleted2}")

    # Listando novamente para verificar exclusão
    print("\n### LOTES APÓS EXCLUSÃO ###")
    lotes = get_all_lotes(connection)
    for lote in lotes:
        print(lote)