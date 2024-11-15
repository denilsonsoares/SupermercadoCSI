import mysql.connector

__cnx = None
def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user='root', password='1234',
        host='localhost',
        database='quase_tudo')

    return __cnx
