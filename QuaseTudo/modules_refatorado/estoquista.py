# estoquista.py

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from .usuario import Estoquista  # Import Estoquista class
from .utils import *
from .common_views import *

def tela_estoquista(estoquista, root, tela_login, abrir_tela_perfil):
    nome_estoquista = estoquista.username
    id_estoquista = estoquista.id_usuario
    # Rest of your code...

    # Update functions to use estoquista methods
    def adicionar_produto_estoque():
        # Collect data from GUI inputs
        # Call estoquista.adicionar_produto with collected data

    def remover_produto_estoque():
        # Collect data from GUI inputs
        # Call estoquista.remover_produto with collected data

    # Rest of your code remains the same
