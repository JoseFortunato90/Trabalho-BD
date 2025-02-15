import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import telasCliente

def telaCompra(cur, conn, cpf, root):
    root.destroy()

    def obter_produtos(cur, filtro_tipo=None, filtro_id=None):
        if filtro_id:
            cur.execute("SELECT * FROM produto WHERE id_produto = ANY (%s)", ([filtro_id],))
        elif filtro_tipo:
            cur.execute("SELECT * FROM produto WHERE LOWER(tipo_produto) = LOWER(%s)", (filtro_tipo,))
        else:
            cur.execute("SELECT * FROM produto")
        return cur.fetchall()

    def atualizar_tabela(cur, tree, filtro_tipo=None, filtro_id=None):
        for item in tree.get_children():
            tree.delete(item)
        produtos = obter_produtos(cur, filtro_tipo, filtro_id)
        for produto in produtos:
            tree.insert("", "end", values=produto)

    def adicionar_ao_carrinho():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return

        item = tree.item(selecionado)['values']
        id_produto, nome, preco, estoque, tipo = item

        if estoque <= 0:
            messagebox.showwarning("Erro", "Produto sem estoque!")
            return

        qtd = simpledialog.askinteger("Quantidade", f"Quantos '{nome}' deseja comprar?", minvalue=1, maxvalue=estoque)
        if qtd is None:
            return

        subtotal = float(preco) * int(qtd)
        carrinho.append((id_produto, nome, preco, qtd, subtotal))
        atualizar_valor_total()
        messagebox.showinfo("Sucesso", f"{qtd}x {nome} adicionado ao carrinho!")

    def atualizar_valor_total():
        total = sum(float(item[2]) * int(item[3]) for item in carrinho)
        lbl_total.config(text=f"Valor Total: R$ {total:.2f}")

    def obter_atendentes():
        cur.execute("SELECT id_funcionario, nome FROM funcionario WHERE id_funcionario IN (SELECT id_funcionario FROM atendente)")
        return cur.fetchall()

    def escolher_atendente():
        atendentes = obter_atendentes()
        if not atendentes:
            messagebox.showerror("Erro", "Nenhum atendente disponível!")
            return None
        escolha = simpledialog.askinteger("Escolher Atendente", "Informe o ID do atendente:\n" + "\n".join([f"{id_} - {nome}" for id_, nome in atendentes]))
        ids_validos = [id_ for id_, _ in atendentes]
        return escolha if escolha in ids_validos else None

    def finalizar_compra():
        if not carrinho:
            messagebox.showwarning("Erro", "O carrinho está vazio!")
            return

        id_atendente = escolher_atendente()
        if not id_atendente:
            return

        valor_total = sum(float(item[2]) * int(item[3]) for item in carrinho)

        cur.execute("INSERT INTO Pedido (cpf_cliente, id_funcionario, valor_total) VALUES (%s, %s, %s) RETURNING id", (cpf, id_atendente, valor_total))
        pedido_id = cur.fetchone()[0]

        for id_produto, nome, preco, qtd, subtotal in carrinho:
            cur.execute("INSERT INTO Pedido_Item (pedido_id, id_produto, quantidade, preco_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)", (pedido_id, id_produto, qtd, preco, subtotal))
            cur.execute("UPDATE Produto SET quantidade_estoque = quantidade_estoque - %s WHERE id_produto = %s", (qtd, id_produto))

        cur.execute("UPDATE Atendente SET numero_vendas_mes = numero_vendas_mes + 1 WHERE id_funcionario = %s", (id_atendente,))
        conn.commit()

        messagebox.showinfo("Sucesso", f"Compra realizada!\nTotal: R$ {valor_total:.2f}")
        carrinho.clear()
        atualizar_valor_total()
        atualizar_tabela(cur, tree)

    root = tk.Tk()
    root.title("Lista de Produtos")
    root.geometry("750x550")

    carrinho = []

    colunas = ("ID", "Nome", "Preço", "Quantidade Estoque", "Tipo do Produto")
    tree = ttk.Treeview(root, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=140)

    tree.pack(expand=True, fill="both")

    frame_filtros = tk.Frame(root)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="Filtrar por Tipo:").grid(row=0, column=0)
    entrada_filtro_tipo = tk.Entry(frame_filtros)
    entrada_filtro_tipo.grid(row=0, column=1, padx=5)
    btn_filtrar_tipo = tk.Button(frame_filtros, text="Filtrar", command=lambda: atualizar_tabela(cur, tree, entrada_filtro_tipo.get()))
    btn_filtrar_tipo.grid(row=0, column=2, padx=5)

    tk.Label(frame_filtros, text="Filtrar por ID:").grid(row=1, column=0)
    entrada_filtro_id = tk.Entry(frame_filtros)
    entrada_filtro_id.grid(row=1, column=1, padx=5)
    btn_filtrar_id = tk.Button(frame_filtros, text="Pesquisar", command=lambda: atualizar_tabela(cur, tree, filtro_id=int(entrada_filtro_id.get())))
    btn_filtrar_id.grid(row=1, column=2, padx=5)

    btn_limpar = tk.Button(root, text="Remover Filtros", command=lambda: atualizar_tabela(cur, tree))
    btn_limpar.pack(pady=5)

    btn_adicionar = tk.Button(root, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho)
    btn_adicionar.pack(pady=5)

    lbl_total = tk.Label(root, text="Valor Total: R$ 0.00", font=("Arial", 12, "bold"))
    lbl_total.pack(pady=5)

    btn_finalizar = tk.Button(root, text="Finalizar Compra", command=finalizar_compra)
    btn_finalizar.pack(pady=5)

    btn_fechar = tk.Button(root, text="Fechar", command=lambda: ( telasCliente.telaClienteAcesso(cur, conn, cpf, root), root.destroy()))
    btn_fechar.pack(pady=10)

    atualizar_tabela(cur, tree)

    root.mainloop()

def telaHistoricoCompras(cur, cpf):
    def obter_historico(cur, cpf):
        cur.execute("""
            SELECT p.id, p.valor_total, p.data_pedido, f.nome 
            FROM Pedido p
            JOIN Funcionario f ON p.id_funcionario = f.id_funcionario
            WHERE p.cpf_cliente = %s
            ORDER BY p.data_pedido DESC
        """, (cpf,))
        return cur.fetchall()
    
    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)

        historico = obter_historico(cur, cpf)
        for pedido in historico:
            tree.insert("", "end", values=pedido)
    
    root = tk.Tk()
    root.title("Histórico de Compras")
    root.geometry("600x400")
    
    colunas = ("ID Pedido", "Valor Total", "Data", "Atendente")
    tree = ttk.Treeview(root, columns=colunas, show="headings")
    
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    
    tree.pack(expand=True, fill="both")
    
    btn_fechar = tk.Button(root, text="Fechar", command=root.destroy)
    btn_fechar.pack(pady=10)
    
    atualizar_tabela()
    root.mainloop()
