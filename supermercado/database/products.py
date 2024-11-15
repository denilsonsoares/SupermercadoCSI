from sql_connection import get_sql_connection
def get_all_products(connection):
    """
    Retorna uma lista de todos os produtos, incluindo os detalhes de marca, tipo e unidade de medida.
    """
    query = """
    SELECT 
        Produtos.id,
        Produtos.Produto,
        Marcas.nome_da_marca,
        Tipos_de_produto.tipo,
        Unidades_de_medida.unidade AS unidade_de_medida,
        Produtos.preco_por_unidade
    FROM Produtos
    JOIN Marcas ON Produtos.Marca_id = Marcas.id
    JOIN Tipos_de_produto ON Produtos.tipo_id = Tipos_de_produto.id
    JOIN Unidades_de_medida ON Produtos.unidade_de_medida_id = Unidades_de_medida.id;
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    products = cursor.fetchall()
    return products

def insert_new_product(connection, product):
    """
    Insere um novo produto no banco de dados.
    :param product: Um dicionário com os dados do produto:
        {
            'Produto': 'Nome do Produto',
            'Marca_id': 1,
            'tipo_id': 2,
            'unidade_de_medida_id': 3,
            'preco_por_unidade': 9.99
        }
    """
    query = """
    INSERT INTO Produtos (Produto, Marca_id, tipo_id, unidade_de_medida_id, preco_por_unidade)
    VALUES (%s, %s, %s, %s, %s);
    """
    data = (
        product['Produto'],
        product['Marca_id'],
        product['tipo_id'],
        product['unidade_de_medida_id'],
        product['preco_por_unidade']
    )
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    return cursor.lastrowid

def delete_product(connection, product_id):
    """
    Remove um produto pelo ID, caso ele não esteja vinculado a lotes ou vendas.
    """
    try:
        query = "DELETE FROM Produtos WHERE id = %s;"
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        connection.commit()
        return cursor.rowcount  # Retorna o número de linhas afetadas
    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
        return 0

def update_product(connection, product_id, updated_data):
    """
    Atualiza os dados de um produto.
    :param updated_data: Um dicionário com os campos a serem atualizados:
        Exemplo: {'Produto': 'Novo Nome', 'preco_por_unidade': 12.99}
    """
    set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
    query = f"UPDATE Produtos SET {set_clause} WHERE id = %s;"
    data = list(updated_data.values()) + [product_id]

    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    return cursor.rowcount


if __name__ == "__main__":

    connection = get_sql_connection()
    #
    print("Lista de Produtos:")
    for product in get_all_products(connection):
        print(product)

    # # Testando insert_new_product
    # new_product = {
    #     'Produto': 'Produto Teste',
    #     'Marca_id': 1,
    #     'tipo_id': 2,
    #     'unidade_de_medida_id': 3,
    #     'preco_por_unidade': 15.99
    # }
    # product_id = insert_new_product(connection, new_product)
    # # print(f"Produto inserido com ID: {product_id}")
    #
    # # Testando update_product
    # update_data = {'Produto': 'Produto Atualizado', 'preco_por_unidade': 19.99}
    # rows_updated = update_product(connection, product_id, update_data)
    # print(f"Número de produtos atualizados: {rows_updated}")
    #
    # # Testando get_all_products
    # print("Lista de Produtos:")
    # for product in get_all_products(connection):
    #     print(product)
    #
    # # Testando delete_product
    # rows_deleted = delete_product(connection, product_id)
    # print(f"Número de produtos deletados: {rows_deleted}")