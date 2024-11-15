import tkinter as tk
from tkinter import font
from tkinter import ttk

def finalizar_venda():
    # Cria uma nova janela para a mensagem de finalização de venda
    finalizar_window = tk.Toplevel(root)
    finalizar_window.title("Venda Finalizada")
    finalizar_window.geometry("300x200")
    finalizar_window.configure(bg="green")
    
    # Texto de sucesso
    label_sucesso = tk.Label(finalizar_window, text="VENDA\nREALIZADA\nCOM SUCESSO", font=("Helvetica", 16, "bold"), fg="black", bg="green")
    label_sucesso.pack(expand=True)
    
    # Botão de fechar
    close_button = tk.Button(finalizar_window, text="X", command=finalizar_window.destroy, font=("Helvetica", 12), bg="green", fg="black", borderwidth=0)
    close_button.place(x=270, y=10)

def cancelar_venda():
    # Cria uma nova janela para a mensagem de cancelamento de venda
    cancelar_window = tk.Toplevel(root)
    cancelar_window.title("Venda Cancelada")
    cancelar_window.geometry("300x200")
    cancelar_window.configure(bg="red")
    
    # Texto de cancelamento
    label_cancelado = tk.Label(cancelar_window, text="VENDA\nCANCELADA", font=("Helvetica", 16, "bold"), fg="black", bg="red")
    label_cancelado.pack(expand=True)
    
    # Botão de fechar
    close_button = tk.Button(cancelar_window, text="X", command=cancelar_window.destroy, font=("Helvetica", 12), bg="red", fg="black", borderwidth=0)
    close_button.place(x=270, y=10)

# Configuração da janela principal
root = tk.Tk()
root.title("Quase-Tudo - Venda de Produtos")
root.geometry("800x600")
root.configure(bg="white")

# Fonte personalizada
header_font = font.Font(family="Helvetica", size=12, weight="bold")
title_font = font.Font(family="Helvetica", size=24, weight="bold")

# Logo e título
frame_top = tk.Frame(root, bg="white")
frame_top.pack(fill="x", pady=(10, 5))

label_logo = tk.Label(frame_top, text="QT", font=title_font, fg="black", bg="white")
label_logo.pack(side="left", padx=10)

label_title = tk.Label(frame_top, text="Quase-Tudo", font=("Helvetica", 14), fg="black", bg="white")
label_title.pack(side="left")

# Informações do usuário e data
label_user_info = tk.Label(frame_top, text="01 / 01 / 2001       12:12       Fulano da Silva       Caixa ID 985394", font=("Helvetica", 10), fg="gray", bg="white")
label_user_info.pack(side="right", padx=10)

# Tabela de produtos
frame_table = tk.Frame(root, bg="white")
frame_table.pack(fill="x", pady=(20, 10), padx=20)

columns = ("Produto", "Quantidade", "Valor unitário", "Total")
table = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)

table.pack(fill="x")
# Exemplo de dados
produtos = [
    ("Açúcar Refinado UNIÃO Pacote 1kg", 2, "R$3,89", "R$7,98"),
    ("Refrigerante Coca-Cola Sem Açúcar PET 1,5L", 3, "R$7,43", "R$22,29"),
    ("Creme De Leite Piracanjuba 200g", 1, "R$3,59", "R$3,59"),
    ("Filé de Peito de Frango Zip SADIA Pacote 1kg", 1, "R$21,52", "R$21,52"),
    ("Pão de Forma PANCO 500g", 1, "R$8,23", "R$8,23")
]
for produto in produtos:
    table.insert("", "end", values=produto)

# Seção de pagamento
frame_payment = tk.Frame(root, bg="white")
frame_payment.pack(fill="x", pady=(10, 5), padx=20)

label_payment = tk.Label(frame_payment, text="Selecione a forma de pagamento:", font=header_font, bg="white")
label_payment.grid(row=0, column=0, sticky="w")

check_cash = tk.Checkbutton(frame_payment, text="Dinheiro (5% de desconto)", bg="white")
check_cash.grid(row=1, column=0, sticky="w")

check_debit = tk.Checkbutton(frame_payment, text="Débito (5% de desconto)", bg="white")
check_debit.grid(row=2, column=0, sticky="w")

check_credit = tk.Checkbutton(frame_payment, text="Crédito", bg="white")
check_credit.grid(row=3, column=0, sticky="w")

check_crediario = tk.Checkbutton(frame_payment, text="Crediário", bg="white")
check_crediario.grid(row=4, column=0, sticky="w")

# Identificação do cliente
frame_client = tk.Frame(root, bg="white")
frame_client.pack(fill="x", pady=(10, 5), padx=20)

label_client = tk.Label(frame_client, text="Identificação do Cliente:", font=header_font, bg="white")
label_client.grid(row=0, column=0, sticky="w")

entry_client_id = tk.Entry(frame_client, font=("Helvetica", 10), width=30)
entry_client_id.insert(0, "Insira nome ou CPF")
entry_client_id.grid(row=0, column=1, sticky="w", padx=5)

# Totais e botões
frame_footer = tk.Frame(root, bg="white")
frame_footer.pack(fill="x", pady=(10, 20), padx=20)

label_total = tk.Label(frame_footer, text="TOTAL", font=header_font, fg="black", bg="white")
label_total.grid(row=0, column=0, padx=10)

label_total_value = tk.Label(frame_footer, text="R$63,61", font=("Helvetica", 12), fg="black", bg="white")
label_total_value.grid(row=0, column=1)

label_vista = tk.Label(frame_footer, text="À VISTA", font=header_font, fg="black", bg="white")
label_vista.grid(row=1, column=0, padx=10)

label_vista_value = tk.Label(frame_footer, text="R$60,42", font=("Helvetica", 12), fg="black", bg="white")
label_vista_value.grid(row=1, column=1)

button_cancel = tk.Button(frame_footer, text="CANCELAR", font=("Helvetica", 10, "bold"), bg="red", fg="white", width=15, command=cancelar_venda)
button_cancel.grid(row=2, column=0, pady=10)

button_finalize = tk.Button(frame_footer, text="FINALIZAR", font=("Helvetica", 10, "bold"), bg="blue", fg="white", width=15, command=finalizar_venda)
button_finalize.grid(row=2, column=1, pady=10)

root.mainloop()
