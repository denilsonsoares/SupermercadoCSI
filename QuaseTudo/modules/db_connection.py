import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class ConexaoSingleton:
    _instancia = None
    _conexao = None

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(ConexaoSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def conectar_banco(self):
        try:
            if self._conexao is None or not self._conexao.is_connected():
                self._conexao = mysql.connector.connect(
                    host="192.168.51.119",
                    user="root",
                    password="Banana33@5",
                    database="quase_tudo"
                )
            return self._conexao
        except Error as err:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {err}")
            return None

    def fechar_conexao(self):
        if self._conexao is not None and self._conexao.is_connected():
            self._conexao.close()
            self._conexao = None
