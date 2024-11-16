import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
from .database import *

# Caminho base relativo
base_dir = os.path.dirname(os.path.abspath(__file__))
imagem_usuario_path = os.path.join(base_dir, "../assets/user_icon.png")
imagem_logout_path = os.path.join(base_dir, "../assets/logout_icon.png")

# Função para atualizar o horário
def atualizar_hora(label):
    def atualizar():
        agora = datetime.now()
        label.config(text=agora.strftime("%d / %m / %Y  %H:%M"))
        label.after(1000, atualizar)
    atualizar()

# Função de logout
def logout(janela, root, tela_login, abrir_tela_perfil):
    janela.destroy()
    tela_login(root, abrir_tela_perfil)

# Função para calcular e atualizar o total e o valor à vista
def atualizar_totais(tabela, total_label, avista_label, pagamento_var):
    total = 0
    for item in tabela.get_children():
        valores = tabela.item(item, "values")
        total += float(valores[5])  # Soma o valor total do produto

    if pagamento_var.get() in ["Dinheiro", "Débito"]:
        valor_avista = total * 0.95  # Aplica 5% de desconto
    else:
        valor_avista = total

    total_label.config(text=f"R${total:.2f}")
    avista_label.config(text=f"R${valor_avista:.2f}")

# Função para exibir a interface de "Realizar Venda" no frame de conteúdo principal
def exibir_realizar_venda(frame_conteudo, vendedor_id):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    tabela_frame = tk.Frame(frame_conteudo, bg="white")
    tabela_frame.pack(pady=10, padx=10, fill="x")

    tabela = ttk.Treeview(
        tabela_frame,
        columns=("Produto", "Marca", "Tipo", "Quantidade", "Valor Unitário", "Total"),
        show="headings",
        height=5,
    )
    tabela.heading("Produto", text="Produto")
    tabela.heading("Marca", text="Marca")
    tabela.heading("Tipo", text="Tipo")
    tabela.heading("Quantidade", text="Quantidade")
    tabela.heading("Valor Unitário", text="Valor Unitário")
    tabela.heading("Total", text="Total")
    tabela.pack(side="left", fill="x", expand=True)

    scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def adicionar_produto():
        def atualizar_resultados(event=None):
            nome_produto = entry_produto.get()
            resultados = buscar_produtos(nome_produto)

            for widget in frame_resultados.winfo_children():
                widget.destroy()

            if resultados:
                for produto in resultados:
                    produto_nome = produto[1]
                    produto_marca = buscar_nome_marca_por_id(produto[2])
                    produto_tipo = buscar_nome_tipo_por_id(produto[3])
                    produto_preco = produto[4]

                    resultado_label = tk.Label(
                        frame_resultados,
                        text=f"{produto_nome} - {produto_marca} - {produto_tipo} - R${produto_preco:.2f}",
                        bg="white",
                        anchor="w",
                    )
                    resultado_label.pack(fill="x", padx=5, pady=2)
                    resultado_label.bind(
                        "<Button-1>",
                        lambda e, p=produto: adicionar_produto_selecionado(p),
                    )

        # def adicionar_produto_selecionado(produto):
        #     def confirmar_quantidade():
        #         try:
        #             quantidade = int(quantidade_entry.get())
        #             if quantidade <= 0:
        #                 raise ValueError("Quantidade deve ser maior que zero.")
        #
        #             produto_nome = produto[1]
        #             produto_marca = buscar_nome_marca_por_id(produto[2])
        #             produto_tipo = buscar_nome_tipo_por_id(produto[3])
        #             produto_preco = produto[4]
        #             total = quantidade * produto_preco
        #
        #             tabela.insert(
        #                 "",
        #                 "end",
        #                 values=(produto_nome, produto_marca, produto_tipo, quantidade, f"{produto_preco:.2f}", f"{total:.2f}"),
        #             )
        #
        #             atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
        #             pesquisa_window.destroy()
        #         except ValueError as e:
        #             messagebox.showerror("Erro", f"Quantidade inválida: {e}")
        #
        #     quantidade_window = tk.Toplevel(pesquisa_window)
        #     quantidade_window.title("Quantidade")
        #     quantidade_window.geometry("300x200")
        #     quantidade_window.configure(bg="white")
        #
        #     tk.Label(
        #         quantidade_window, text=f"Produto: {produto[1]}", font=("Arial", 12), bg="white"
        #     ).pack(pady=10)
        #
        #     tk.Label(
        #         quantidade_window, text="Digite a quantidade:", font=("Arial", 12), bg="white"
        #     ).pack(pady=5)
        #
        #     quantidade_entry = tk.Entry(quantidade_window, font=("Arial", 12))
        #     quantidade_entry.pack(pady=10)
        #     quantidade_entry.insert(0, "1")
        #
        #     tk.Button(
        #         quantidade_window,
        #         text="Confirmar",
        #         font=("Arial", 12),
        #         bg="green",
        #         fg="white",
        #         command=confirmar_quantidade,
        #     ).pack(pady=10)

        def adicionar_produto_selecionado(produto):
            def buscar_e_exibir_lotes(event=None):
                lote_id = lote_entry.get().strip()
                produto_id = produto[0]  # ID do produto vindo do banco de dados

                # Buscar lotes mesmo que o ID esteja vazio
                lotes = buscar_lotes(lote_id, produto_id)

                # Limpar a lista
                lotes_lista.delete(0, tk.END)

                if lotes:
                    for lote in lotes:
                        # Formato: ID - Quantidade - Validade - Fornecedor
                        lotes_lista.insert(
                            tk.END,
                            f"{lote[0]} - {lote[1]} unidades - Vence em {lote[3]} - {lote[4]}"
                        )
                else:
                    lotes_lista.insert(tk.END, "Nenhum lote encontrado.")

            def confirmar_quantidade():
                try:
                    # Verificar se há um lote selecionado
                    if not lotes_lista.curselection():
                        raise ValueError("É necessário selecionar um lote.")

                    lote_selecionado = lotes_lista.get(lotes_lista.curselection())
                    lote_id = lote_selecionado.split(" - ")[0]  # Pegar o ID do lote
                    quantidade = int(quantidade_entry.get())

                    if quantidade <= 0:
                        raise ValueError("A quantidade deve ser maior que zero.")

                    # Validar quantidade com o lote
                    lote_quantidade = int(lote_selecionado.split(" - ")[1].split(" ")[0])
                    if quantidade > lote_quantidade:
                        raise ValueError("A quantidade excede o disponível no lote selecionado.")

                    produto_nome = produto[1]
                    produto_marca = buscar_nome_marca_por_id(produto[2])
                    produto_tipo = buscar_nome_tipo_por_id(produto[3])
                    produto_preco = produto[4]
                    total = quantidade * produto_preco

                    # Adicionar o produto à tabela principal
                    tabela.insert(
                        "",
                        "end",
                        values=(
                        produto_nome, produto_marca, produto_tipo, quantidade, f"{produto_preco:.2f}", f"{total:.2f}"),
                    )

                    atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
                    quantidade_window.destroy()
                except ValueError as e:
                    messagebox.showerror("Erro", str(e))
                except IndexError:
                    messagebox.showerror("Erro", "Erro ao selecionar lote ou quantidade.")

            quantidade_window = tk.Toplevel(pesquisa_window)
            quantidade_window.title("Quantidade e Lote")
            quantidade_window.geometry("500x550")  # Aumentar a altura da janela
            quantidade_window.configure(bg="white")

            tk.Label(
                quantidade_window, text=f"Produto: {produto[1]}", font=("Arial", 12), bg="white"
            ).pack(pady=10)

            tk.Label(
                quantidade_window, text="Digite o ID do lote:", font=("Arial", 12), bg="white"
            ).pack(pady=5)

            lote_entry = tk.Entry(quantidade_window, font=("Arial", 12))
            lote_entry.pack(pady=5, padx=10, fill="x")
            lote_entry.bind("<KeyRelease>", buscar_e_exibir_lotes)  # Busca dinâmica ao digitar

            frame_lotes = tk.Frame(quantidade_window, bg="white")
            frame_lotes.pack(pady=10, fill="both", expand=True)

            lotes_lista = tk.Listbox(frame_lotes, font=("Arial", 10), bg="white")
            lotes_lista.pack(side="left", fill="both", expand=True, padx=10)

            scrollbar = ttk.Scrollbar(frame_lotes, orient="vertical", command=lotes_lista.yview)
            lotes_lista.config(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Exibir automaticamente todos os lotes disponíveis ao abrir a janela
            buscar_e_exibir_lotes()

            tk.Label(
                quantidade_window, text="Digite a quantidade:", font=("Arial", 12), bg="white"
            ).pack(pady=10)

            quantidade_entry = tk.Entry(quantidade_window, font=("Arial", 12))
            quantidade_entry.pack(pady=10)
            quantidade_entry.insert(0, "1")

            tk.Button(
                quantidade_window,
                text="Confirmar",
                font=("Arial", 12),
                bg="green",
                fg="white",
                command=confirmar_quantidade,
            ).pack(pady=10)

        pesquisa_window = tk.Toplevel(frame_conteudo)
        pesquisa_window.title("Pesquisar Produto")
        pesquisa_window.geometry("400x300")
        pesquisa_window.configure(bg="white")

        tk.Label(
            pesquisa_window, text="Digite o nome do produto:", font=("Arial", 12), bg="white"
        ).pack(pady=10)

        entry_produto = tk.Entry(pesquisa_window, font=("Arial", 12))
        entry_produto.pack(pady=10, padx=10, fill="x")
        entry_produto.bind("<KeyRelease>", atualizar_resultados)

        frame_resultados = tk.Frame(pesquisa_window, bg="white")
        frame_resultados.pack(pady=10, padx=10, fill="both", expand=True)

    def remover_produto():
        try:
            item_selecionado = tabela.selection()[0]
            tabela.delete(item_selecionado)
            atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
        except IndexError:
            messagebox.showerror("Erro", "Selecione um produto para remover!")
    

    botao_adicionar = tk.Button(frame_conteudo, text="Adicionar Produto", command=adicionar_produto)
    botao_adicionar.pack(pady=5)

    botao_remover = tk.Button(frame_conteudo, text="Remover Produto", command=remover_produto)
    botao_remover.pack(pady=5)

    cliente_frame = tk.Frame(frame_conteudo, bg="white")
    cliente_frame.pack(pady=10)

    cliente_label = tk.Label(
        cliente_frame, text="Identificação do Cliente (Opcional):", font=("Arial", 12), bg="white"
    )
    cliente_label.pack(side="left")

    cliente_entry = tk.Entry(cliente_frame, font=("Arial", 12), width=30)
    cliente_entry.pack(side="left", padx=10)

    pagamento_frame = tk.Frame(frame_conteudo, bg="white")
    pagamento_frame.pack(pady=10)

    tk.Label(pagamento_frame, text="Forma de Pagamento:", font=("Arial", 12), bg="white").pack(anchor="w")

    pagamento_var = tk.StringVar(value="Crédito")

    def atualizar_pagamento(*args):
        atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)

    pagamento_var.trace_add("write", atualizar_pagamento)

    formas_pagamento = [("Dinheiro", "Dinheiro"), ("Débito","Débito"), ("Crédito", "Crédito"), ("Crediário", "Crediário")]
    for texto, valor in formas_pagamento:
        tk.Radiobutton(
            pagamento_frame,
            text=texto,
            variable=pagamento_var,
            value=valor,
            font=("Arial", 12),
            bg="white",
        ).pack(anchor="w")

    total_frame = tk.Frame(frame_conteudo, bg="white")
    total_frame.pack(pady=20)

    total_label = tk.Label(
        total_frame, text="TOTAL", font=("Arial", 14, "bold"), bg="white"
    )
    total_label.grid(row=0, column=0, padx=10)

    total_valor = tk.Label(total_frame, text="R$0.00", font=("Arial", 14), bg="white")
    total_valor.grid(row=1, column=0, padx=10)

    avista_label = tk.Label(
        total_frame, text="À VISTA", font=("Arial", 14, "bold"), bg="white"
    )
    avista_label.grid(row=0, column=1, padx=10)

    avista_valor = tk.Label(total_frame, text="R$0.00", font=("Arial", 14), bg="white")
    avista_valor.grid(row=1, column=1, padx=10)

    botoes_frame = tk.Frame(frame_conteudo, bg="white")
    botoes_frame.pack(pady=20)

    def finalizar_venda():
        cliente_id = cliente_entry.get().strip()
        if pagamento_var.get() == "Crediário" and not cliente_id:
            messagebox.showerror("Erro", "Identificação do cliente é obrigatória para o Crediário!")
            return

        itens = []
        for item in tabela.get_children():
            produto, marca, tipo, quantidade, preco, total = tabela.item(item, "values")
            itens.append(
                {
                    "produto_id": obter_id_por_nome("produtos","produto",produto),
                    "quantidade": int(quantidade),
                    "preco": float(preco),
                }
            )

        forma_pagamento = {
            "Dinheiro": 1,
            "Débito": 2,
            "Crédito": 3,
            "Crediário": 4
        }

        sucesso = registrar_venda(vendedor_id, cliente_id, itens, forma_pagamento[pagamento_var.get()])
        if sucesso:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            exibir_realizar_venda(frame_conteudo, vendedor_id)
        else:
            messagebox.showerror("Erro", "Erro ao registrar a venda.")
    
    def cancelar_venda():
        """Limpa todos os campos e itens da interface de realizar venda."""
        for item in tabela.get_children():
            tabela.delete(item)
        cliente_entry.delete(0, tk.END)
        pagamento_var.set("Crédito")
        atualizar_totais(tabela, total_valor, avista_valor, pagamento_var)
        messagebox.showinfo("Cancelado", "Venda cancelada com sucesso!")

    botao_cancelar = tk.Button(
        botoes_frame, text="CANCELAR", font=("Arial", 12, "bold"), bg="red", fg="white", width=10, command=cancelar_venda
    )
    botao_cancelar.grid(row=0, column=0, padx=10)

    botao_finalizar = tk.Button(
        botoes_frame,
        text="FINALIZAR",
        font=("Arial", 12, "bold"),
        bg="blue",
        fg="white",
        width=10,
        command=finalizar_venda,
    )
    botao_finalizar.grid(row=0, column=1, padx=10)

# Função para exibir o histórico de vendas do usuário
def exibir_historico_vendas(frame_conteudo, vendedor_id):
    # Limpar o conteúdo existente no frame_conteúdo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    tk.Label(frame_conteudo, text="Histórico de Vendas", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    tabela_frame = tk.Frame(frame_conteudo, bg="white")
    tabela_frame.pack(pady=10, padx=10, fill="x")

    tabela = ttk.Treeview(
        tabela_frame,
        columns=("ID Venda", "Data", "Cliente", "Total"),
        show="headings",
        height=10,
    )
    tabela.heading("ID Venda", text="ID Venda")
    tabela.heading("Data", text="Data")
    tabela.heading("Cliente", text="Cliente")
    tabela.heading("Total", text="Total (R$)")
    tabela.pack(side="left", fill="x", expand=True)

    scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Simular busca de dados no banco de dados (substitua com sua lógica de consulta ao MySQL)
    from .database import buscar_historico_vendas
    vendas = buscar_historico_vendas(vendedor_id)

    for venda in vendas:
        tabela.insert("", "end", values=(venda[0], venda[1], venda[2], f"{venda[3]:.2f}"))


# Função principal para a tela do usuário Caixa
def tela_caixa(nome_caixa, id_caixa, root, tela_login, abrir_tela_perfil):
    janela_caixa = tk.Toplevel()
    janela_caixa.title("Caixa - Quase-Tudo")
    janela_caixa.geometry("1000x700")
    janela_caixa.configure(bg="#f4f4f4")
    janela_caixa.attributes("-fullscreen", True)

    frame_menu = tk.Frame(janela_caixa, bg="#d3d3d3", width=200)
    frame_menu.pack(side="left", fill="y")

    tk.Label(
        frame_menu,
        text="QT\nQuase-Tudo",
        bg="#d3d3d3",
        font=("Arial", 16, "bold"),
        fg="black",
    ).pack(pady=20)

    realizar_venda_button = tk.Button(
        frame_menu,
        text="Realizar venda",
        font=("Arial", 12),
        bg="#d3d3d3",
        fg="black",
        bd=0,
        relief="flat",
        activebackground="#a9a9a9",
        activeforeground="white",
        command=lambda: exibir_realizar_venda(frame_conteudo, id_caixa),
    )
    realizar_venda_button.pack(fill="x", pady=10)

    historico_vendas_button = tk.Button(
        frame_menu,
        text="Histórico de Vendas",
        font=("Arial", 12),
        bg="#d3d3d3",
        fg="black",
        bd=0,
        relief="flat",
        activebackground="#a9a9a9",
        activeforeground="white",
        command=lambda: exibir_historico_vendas(frame_conteudo, id_caixa),
    )
    historico_vendas_button.pack(fill="x", pady=10)

    frame_cabecalho = tk.Frame(janela_caixa, bg="#e0e0e0", height=50)
    frame_cabecalho.pack(side="top", fill="x")

    label_data_hora = tk.Label(frame_cabecalho, bg="#e0e0e0", font=("Arial", 12))
    label_data_hora.place(relx=0.5, rely=0.5, anchor="center")
    atualizar_hora(label_data_hora)

    label_nome = tk.Label(
        frame_cabecalho, text=nome_caixa, bg="#e0e0e0", font=("Arial", 12, "bold")
    )
    label_nome.place(relx=0.75, rely=0.5, anchor="e")

    label_id = tk.Label(
        frame_cabecalho,
        text=f"Caixa ID {id_caixa}",
        bg="#e0e0e0",
        font=("Arial", 10),
    )
    label_id.place(relx=0.85, rely=0.5, anchor="e")

    imagem_usuario = Image.open(imagem_usuario_path).resize((30, 30), Image.LANCZOS)
    imagem_usuario = ImageTk.PhotoImage(imagem_usuario)
    tk.Label(frame_cabecalho, image=imagem_usuario, bg="#e0e0e0").place(
        relx=0.9, rely=0.5, anchor="e"
    )

    imagem_logout = Image.open(imagem_logout_path).resize((30, 30), Image.LANCZOS)
    imagem_logout = ImageTk.PhotoImage(imagem_logout)
    botao_logout = tk.Button(
        frame_cabecalho,
        image=imagem_logout,
        bg="#e0e0e0",
        bd=0,
        command=lambda: logout(janela_caixa, root, tela_login, abrir_tela_perfil),
    )
    botao_logout.image = imagem_logout
    botao_logout.place(relx=0.95, rely=0.5, anchor="e")

    frame_conteudo = tk.Frame(janela_caixa, bg="white")
    frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_conteudo, text="Tela de Caixa", font=("Arial", 20, "bold"), bg="white").pack(
        pady=50
    )

    janela_caixa.mainloop()







