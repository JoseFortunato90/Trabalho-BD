import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def telaExcluirCadastro(cur, conn, id, root):
    
    def excluirCadastro(cur, conn, id, root, senha_entry):
        senha_entry = senha_entry.get()

        cur.execute("""
            SELECT * FROM funcionario WHERE id_funcionario = %s
        """, (id,))
        Gerente = cur.fetchone() 
    
        if Gerente[4] == senha_entry:
            cur.execute("""
             DELETE FROM Gerente WHERE id_funcionario = %s;
            """, (id,))
            cur.execute("DELETE FROM funcionario WHERE id_funcionario = %s AND senha = %s;", (id, senha_entry))
            

            conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso.")
        else:
            messagebox.showerror("Erro", "Senha incorreta")
     
    
    def tela(cur,conn,cpf,root):
        
        root = tk.Tk()
        root.title("Excluir cadastro")
        root.geometry("250x100")

        tk.Label(root, text="Digite sua senha:").pack()
        senha_entry = tk.Entry(root, show="*")
        senha_entry.pack()

        tk.Button(root, text="Excluir Cadastro", command=lambda: (excluirCadastro(cur,conn,cpf,root,senha_entry),root.destroy)).pack()

        root.mainloop()
    
    root.destroy()
    resposta = messagebox.askyesno("Confirmação", "Deseja excluir seu cadastro permanentemente?")
    if resposta:
        tela(cur,conn,id,root)
        root.destroy()
    else:
        return

def telaAlterarDados(cur, conn, id, root):
    root.destroy()
    
    def alterar_dados_gerente():
        campo_selecionado = campo_var.get().strip()
        novo_valor = entrada_valor.get()

        if novo_valor == "":
            messagebox.showerror("Erro", f"Opção inválida! Digite um valor")
            return
        if campo_selecionado == "Nome":
            cur.execute("UPDATE funcionario SET nome = %s WHERE id_funcionario = %s", (novo_valor, id))
        elif campo_selecionado == "Senha":
            cur.execute("UPDATE funcionario SET senha = %s WHERE id_funcionario = %s", (novo_valor, id))
        elif campo_selecionado == "Idade":
            cur.execute("UPDATE funcionario SET idade = %s WHERE id_funcionario = %s", (novo_valor, id))
        elif campo_selecionado == "Salario":
            cur.execute("UPDATE funcionario SET salario = %s WHERE id_funcionario = %s", (novo_valor, id))
        else:
            messagebox.showerror("Erro", f"Opção inválida! Valor recebido: {campo_selecionado}")
            return
        
        conn.commit()
        messagebox.showinfo("Sucesso", f"{campo_selecionado} alterado com sucesso!")
        root.destroy()
    
    root = tk.Tk()
    root.title("Alterar Dados do Gerente")
    root.geometry("300x200")
    
    tk.Label(root, text="Escolha o dado a alterar:").pack()
    
    opcoes = ["Nome", "Idade", "Salario", "Senha"]
    campo_var = tk.StringVar(root)
    campo_var.set(opcoes[0])  
    
    option_menu = tk.OptionMenu(root, campo_var, *opcoes)
    option_menu.pack()
    
    tk.Label(root, text="Novo valor:").pack()
    entrada_valor = tk.Entry(root)
    entrada_valor.pack()
    
    tk.Button(root, text="Confirmar", command = alterar_dados_gerente).pack(pady=10)
    tk.Button(root, text="Cancelar", command = lambda: (telaGerenteAcesso(cur, conn, id, root),root.destroy)).pack(pady=10)
    
    root.mainloop()

def contratarAtendente(cur, conn, id, root):
    
    def contratar(cur, conn, root, nome_entry, idade_entry, salario_entry, senha_entry):
        senha = senha_entry.get()
        nome = nome_entry.get()
        idade = idade_entry.get()
        salario = salario_entry.get()

        if not idade or not salario or not senha or not nome:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        idade = int(idade)
        salario = float(salario)

        cur.execute("""
        INSERT INTO Funcionario (Nome, senha, Idade, Salario)
        VALUES (%s, %s, %s, %s) RETURNING Id_Funcionario;
        """, (nome, senha, idade, salario))

        funcionario = cur.fetchone()

        id_funcionario = funcionario[0]

        cur.execute("""
        INSERT INTO Atendente (Id_Funcionario, numero_vendas_mes)
        VALUES (%s, %s);
        """, (id_funcionario, 0))

        cur.execute("""
        INSERT INTO Atendente_Gerente (Id_atendente, id_gerente)
        VALUES (%s, %s);
        """, (id_funcionario, id))
        
        conn.commit()
        messagebox.showinfo("Atendente", f"Cadastro realizado com sucesso. Id do atendente: {id_funcionario}")
        root.destroy
     
    root = tk.Tk()
    root.title("Cadastro Gerente")
    root.geometry("500x400")
    
    tk.Label(root, text="Nome:").pack()
    nome_entry = tk.Entry(root)
    nome_entry.pack()

    tk.Label(root, text="Idade:").pack()
    idade_entry = tk.Entry(root)
    idade_entry.pack()

    tk.Label(root, text="Salário:").pack()
    salario_entry = tk.Entry(root)
    salario_entry.pack()

    tk.Label(root, text="Senha:").pack()
    senha_entry = tk.Entry(root)
    senha_entry.pack()

    tk.Button(root, text="Cadastrar", command=lambda: (contratar(cur, conn, root, nome_entry, idade_entry, salario_entry, senha_entry), root.destroy())).pack()
    
    root.mainloop()

def adicionarItem(cur, conn, root):

    def repor(cur, conn,nome_entry, preco_entry, quantidade_estoque_entry, tipo_entry):
        nome = nome_entry.get()
        preco = preco_entry.get()
        quantidade_estoque = quantidade_estoque_entry.get()
        tipo = tipo_entry.get()

        if not nome or not quantidade_estoque or not preco or not tipo:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        preco = float(preco)
        quantidade_estoque = int(quantidade_estoque)

        cur.execute("SELECT Id_Produto, Quantidade_Estoque FROM Produto WHERE Nome = %s", (nome,))
        produto = cur.fetchone()

        if produto:
            messagebox.showerror("Erro", "Produto com mesmo nome já cadastrado")
        else:
            cur.execute("""
                INSERT INTO Produto (Nome, Preco, Quantidade_Estoque, Tipo_produto)
                VALUES (%s, %s, %s, %s)
            """, (nome, preco, quantidade_estoque, tipo))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso")

    root = tk.Tk()
    root.title("Adicionar produto")
    root.geometry("500x400")
    
    tk.Label(root, text="Nome:").pack()
    nome_entry = tk.Entry(root)
    nome_entry.pack()

    tk.Label(root, text="Preço:").pack()
    preco_entry = tk.Entry(root)
    preco_entry.pack()

    tk.Label(root, text="Tipo:").pack()
    tipo_entry = tk.Entry(root)
    tipo_entry.pack()

    tk.Label(root, text="Quantidade:").pack()
    quantidade_entry = tk.Entry(root)
    quantidade_entry.pack()

    tk.Button(root, text="Confirmar", command=lambda: (repor(cur, conn,nome_entry, preco_entry, quantidade_entry, tipo_entry), root.destroy())).pack()
    
    root.mainloop()

def adicionarListaItens(cur, conn, root):

    def reporLista(cur, conn, arquivo):
        arquivo = arquivo.get()
        arquivo = arquivo + ".txt"

        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = f.readlines()

            for linha in linhas:
                dados = linha.strip().split(",") 
                if len(dados) == 4:  
                    nome = dados[0]
                    preco = float(dados[1])
                    quantidade_estoque = int(dados[2])
                    tipo_produto = dados[3]  

                    cur.execute("SELECT Id_Produto, Quantidade_Estoque FROM Produto WHERE Nome = %s", (nome,))
                    produto = cur.fetchone()

                    if produto:
                        id_produto, estoque_atual = produto
                        novo_estoque = estoque_atual + quantidade_estoque

                        cur.execute("""
                            UPDATE Produto 
                            SET Quantidade_Estoque = %s, Preco = %s, Tipo_Produto = %s
                            WHERE Id_Produto = %s
                        """, (novo_estoque, preco, tipo_produto, id_produto))
                    else:
                        cur.execute("""
                            INSERT INTO Produto (Nome, Preco, Quantidade_Estoque, Tipo_Produto)
                            VALUES (%s, %s, %s, %s)
                        """, (nome, preco, quantidade_estoque, tipo_produto))

            conn.commit()
            messagebox.showinfo("Sucesso", f"itens adicionados com sucesso.")

        except FileNotFoundError:
            messagebox.showinfo("Erro","Arquivo errado ou não encontrado")

    root = tk.Tk()
    root.title("Adicionar lista de itens")
    root.geometry("300x200")
    
    tk.Label(root, text="Nome do arquivo:").pack()
    arquivo_entry = tk.Entry(root)
    arquivo_entry.pack()
    
    tk.Button(root, text="Confirmar", command=lambda: (reporLista(cur, conn, arquivo_entry), root.destroy)).pack()
    
    root.mainloop()

def reporItem(cur, conn, root, id):
    
    def obter_produtos(cur): 
        cur.execute("SELECT * FROM produto")  

        return cur.fetchall()
    
    def repor(cur, conn, campo_var, entrada_valor):
        produto_selecionado = campo_var.get().strip()
        novo_valor = entrada_valor.get()

        if novo_valor == "":
            messagebox.showerror("Erro", f"Opção inválida! Digite um valor")
            return
        
        cur.execute("SELECT * FROM produto WHERE nome = %s",(produto_selecionado,))
        prod = cur.fetchone()
        novo_valor = int(novo_valor) + prod[3]
        
        cur.execute("UPDATE produto SET quantidade_estoque = %s WHERE nome = %s", (novo_valor, produto_selecionado))
        
        conn.commit()
        messagebox.showinfo("Sucesso", f"{produto_selecionado} alterado com sucesso!")
        root.destroy()
        

    produtos = obter_produtos(cur)
    produtos_nome = []
    for produto in produtos:
        produtos_nome.append(produto[1])

    root = tk.Tk()
    root.title("Repor item")
    root.geometry("300x200")
    
    tk.Label(root, text="Escolha o produto para repor:").pack()
    
    opcoes = produtos_nome
    campo_var = tk.StringVar(root)
    campo_var.set(opcoes[0])  
    
    option_menu = tk.OptionMenu(root, campo_var, *opcoes)
    option_menu.pack()
    
    tk.Label(root, text="Valor a repor:").pack()
    entrada_valor = tk.Entry(root)
    entrada_valor.pack()
    
    tk.Button(root, text="Confirmar", command = lambda: repor(cur, conn, campo_var, entrada_valor)).pack(pady=10)
    tk.Button(root, text="Cancelar", command = lambda: (telaGerenteAcesso(cur, conn, id, root),root.destroy)).pack(pady=10)

def tela_visualizar_produtos(cur):


    def obter_produtos(cur, filtro_tipo=None, filtro_id=None, caros_baratos=False):
        if caros_baratos:
            cur.execute("""
                SELECT * FROM produto 
                WHERE preco = ANY (SELECT MAX(preco) FROM produto)
                OR preco = ANY (SELECT MIN(preco) FROM produto)
            """)
        elif filtro_id:  
            cur.execute("SELECT * FROM produto WHERE id_produto = ANY (%s)", ([filtro_id],))  
        elif filtro_tipo: 
            cur.execute("SELECT * FROM produto WHERE tipo_produto ILIKE %s", (filtro_tipo,))
        else:
            cur.execute("SELECT * FROM produto")  

        return cur.fetchall()

    def atualizar_tabela(cur, tree, filtro_tipo=None, filtro_id=None, caros_baratos=False):
        for item in tree.get_children():
            tree.delete(item)

        produtos = obter_produtos(cur, filtro_tipo, filtro_id, caros_baratos)

        for produto in produtos:
            tree.insert("", "end", values=produto)
   
    root = tk.Tk()
    root.title("Lista de Produtos")
    root.geometry("750x500")

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
    btn_filtrar_id = tk.Button(frame_filtros, text="Pesquisar",command=lambda: atualizar_tabela(cur, tree, filtro_id=int(entrada_filtro_id.get())))
    btn_filtrar_id.grid(row=1, column=2, padx=5)


    btn_caros_baratos = tk.Button(root, text="Mostrar Itens Mais Caros e Mais Baratos",command=lambda: atualizar_tabela(cur, tree, caros_baratos=True))
    btn_caros_baratos.pack(pady=5)


    btn_limpar = tk.Button(root, text="Remover Filtros", command=lambda: atualizar_tabela(cur, tree))
    btn_limpar.pack(pady=5)


    btn_fechar = tk.Button(root, text="Fechar", command=root.destroy)
    btn_fechar.pack(pady=10)

    atualizar_tabela(cur, tree)

    root.mainloop()

def telaEstoque(cur, conn, root, id):

    root.destroy()
    root = tk.Tk()
    root.title("Estoque")
    root.geometry("500x450")

    tk.Label(root, text="Sistema de Estoque", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Ver estoque", width=20, command= lambda: tela_visualizar_produtos(cur)).pack(pady=5)
    tk.Button(root, text="Repor item", width=20, command= lambda: (reporItem(cur, conn, root, id))).pack(pady=5)
    tk.Button(root, text="Adicionar item", width=20, command= lambda: (adicionarItem(cur, conn, root))).pack(pady=5)
    tk.Button(root, text="Adicionar itens", width=20, command= lambda: adicionarListaItens(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=lambda: (telaGerenteAcesso(cur, conn, id, root),root.destroy)).pack(pady=20)

    root.mainloop()

def telaGerenteAcesso(cur, conn, id, root):
    root.destroy()
    root = tk.Tk()
    root.title("Acesso Gerente")
    root.geometry("500x450")

    cur.execute("SELECT * FROM funcionario WHERE id_funcionario = %s", (id,))
    gerente = cur.fetchone()

    tk.Label(root, text=f"Bem-vindo - {gerente[1]}", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Estoque", width=20, command= lambda: telaEstoque(cur, conn, root, id)).pack(pady=5)
    tk.Button(root, text="Contratar atendente", width=20, command= lambda: contratarAtendente(cur, conn, id, root)).pack(pady=5)
    tk.Button(root, text="Alterar Dados", width=20, command= lambda: telaAlterarDados(cur, conn, id, root)).pack(pady=5)
    tk.Button(root, text="Excluir Cadastro", width=20, command= lambda: telaExcluirCadastro(cur,conn,id,root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=lambda: (root.destroy(), telaGerente(cur, conn, root)) ).pack(pady=20)

    root.mainloop()

def acessar(cur, conn, root):

    root.destroy()
    def acesso(cur, conn, id_entry, senha_entry, root):
        id = id_entry.get()
        senha = senha_entry.get()

        if not id or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            root.quit
            return
        
        try:
            id = int(id)
            cur.execute("SELECT * FROM funcionario WHERE id_funcionario = %s", (id,))
            funcionario = cur.fetchone()

            cur.execute("""
                SELECT * FROM Gerente WHERE id_funcionario = %s
            """, (id,))

            gerente = cur.fetchone()
        
            if gerente:
                if funcionario[4] == senha:
                    telaGerenteAcesso(cur, conn, id, root)
                    root.destroy()
                else:
                    messagebox.showerror("Erro", "Senha incorreta!")
                    root.destroy()
            else:
                messagebox.showerror("Erro", "Gerente não encontrado ou o funcionário não é gerente!")
                root.destroy()
        
        except ValueError:
            messagebox.showerror("Erro", "Id deve conter apenas números.")
        root.quit

    root = tk.Tk()
    root.title("Acesso Gerente")
    root.geometry("300x200")
    
    tk.Label(root, text="Id:").pack()
    id_entry = tk.Entry(root)
    id_entry.pack()
    
    tk.Label(root, text="Senha:").pack()
    senha_entry = tk.Entry(root, show="*")
    senha_entry.pack()
    
    tk.Button(root, text="Acessar", command=lambda: acesso(cur, conn, id_entry, senha_entry, root)).pack()
    
    root.mainloop()

def cadastrar(cur, conn, root):

    root.destroy()
    
    def cadastro(cur, conn, nome_entry, idade_entry, salario_entry, senha_entry, id_mercearia_entry, root):
        senha = senha_entry.get()
        nome = nome_entry.get()
        idade = idade_entry.get()
        salario = salario_entry.get()
        id_mercearia = id_mercearia_entry.get()

        if not idade or not id_mercearia or not salario or not senha or not nome:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        idade = int(idade)
        salario = float(salario)
        id_mercearia = int(id_mercearia)

        cur.execute("""
        INSERT INTO Funcionario (Nome, senha, Idade, Salario)
        VALUES (%s, %s, %s, %s) RETURNING Id_Funcionario;
        """, (nome, senha, idade, salario))

        gerente = cur.fetchone()

        id_funcionario = gerente[0]

        cur.execute("""
        INSERT INTO Gerente (Id_Funcionario, Id_Mercearia)
        VALUES (%s, %s);
        """, (id_funcionario, id_mercearia))
        
        conn.commit()
        messagebox.showinfo("gerente", f"Cadastro realizado com sucesso. Seu id: {id_funcionario}")
        root.destroy


    root = tk.Tk()
    root.title("Cadastro Gerente")
    root.geometry("500x400")
    
    tk.Label(root, text="Nome:").pack()
    nome_entry = tk.Entry(root)
    nome_entry.pack()

    tk.Label(root, text="Idade:").pack()
    idade_entry = tk.Entry(root)
    idade_entry.pack()

    tk.Label(root, text="Salário:").pack()
    salario_entry = tk.Entry(root)
    salario_entry.pack()
    
    tk.Label(root, text="Id mercearia:").pack()
    id_mercearia_entry = tk.Entry(root)
    id_mercearia_entry.pack()

    tk.Label(root, text="Senha:").pack()
    senha_entry = tk.Entry(root)
    senha_entry.pack()
    
    tk.Button(root, text="Cadastrar", command=lambda: (cadastro(cur, conn, nome_entry, idade_entry, salario_entry, senha_entry, id_mercearia_entry, root), root.destroy())).pack()
    
    root.mainloop()

def telaGerente(cur, conn, root):
    root = tk.Tk()
    root.title("Sistema de acesso Gerente")
    root.geometry("500x450")

    tk.Label(root, text="Bem-vindo - Gerente", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Acessar", width=20, command= lambda: acessar(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Cadastrar", width=20, command= lambda: cadastrar(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=root.destroy).pack(pady=20)

    root.mainloop()