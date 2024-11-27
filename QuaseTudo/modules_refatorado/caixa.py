# caixa.py

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .usuario import Caixa  # Import Caixa class
from .utils import *

def tela_caixa(caixa, root, tela_login, abrir_tela_perfil):
    nome_caixa = caixa.username
    id_caixa = caixa.id_usuario
    # Rest of your code...

    # Update functions to use caixa methods
    def exibir_realizar_venda(frame_conteudo):
        # Existing code...

        def finalizar_venda():
            cliente_id = cliente_entry.get().strip() or None
            itens = []
            for item in tabela.get_children():
                produto, marca, tipo, quantidade, preco, total, id_lote = tabela.item(item, "values")
                produto_id = obter_id_por_nome("produtos", "Produto", produto)
                if not produto_id:
                    messagebox.showerror("Erro", f"Produto '{produto}' não encontrado.")
                    return
                itens.append({
                    "produto_id": produto_id,
                    "quantidade": int(quantidade),
                    "preco": float(preco),
                    "id_lote": int(id_lote),
                })

            forma_pagamento = pagamento_var.get()
            if caixa.registrar_venda(cliente_id, itens, forma_pagamento):
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
                exibir_realizar_venda(frame_conteudo)
            else:
                messagebox.showerror("Erro", "Erro ao registrar venda.")

        # Rest of your code...

    # Update other functions as needed

    # Rest of your code remains the same
