import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def telaHistoricoVendas(cur, conn, id, root):
    print("...")

def telaAlterarDados(cur, conn, id, root):
    root.destroy()
    
    def alterar_dados_atendente():
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
        else:
            messagebox.showerror("Erro", f"Opção inválida! Valor recebido: {campo_selecionado}")
            return
        
        conn.commit()
        messagebox.showinfo("Sucesso", f"{campo_selecionado} alterado com sucesso!")
        root.destroy()
    
    root = tk.Tk()
    root.title("Alterar Dados do Atendente")
    root.geometry("300x200")
    
    tk.Label(root, text="Escolha o dado a alterar:").pack()
    
    opcoes = ["Nome", "Idade", "Senha"]
    campo_var = tk.StringVar(root)
    campo_var.set(opcoes[0])  
    
    option_menu = tk.OptionMenu(root, campo_var, *opcoes)
    option_menu.pack()
    
    tk.Label(root, text="Novo valor:").pack()
    entrada_valor = tk.Entry(root)
    entrada_valor.pack()
    
    tk.Button(root, text="Confirmar", command = alterar_dados_atendente).pack(pady=10)
    tk.Button(root, text="Cancelar", command = lambda: (telaAtendenteAcesso(cur, conn, id, root),root.destroy)).pack(pady=10)
    
    root.mainloop()

def telaHistorico(cur, id_atendente, root):
    def obter_historico(cur, id_atendente):
        cur.execute("""
            SELECT p.id, c.nome, p.valor_total, p.data_pedido
            FROM Pedido p
            JOIN Cliente c ON p.cpf_cliente = c.cpf
            WHERE p.id_funcionario = %s
            ORDER BY p.data_pedido DESC
        """, (id_atendente,))
        return cur.fetchall()
    
    def atualizar_tabela():
        for item in tree.get_children():
            tree.delete(item)

        historico = obter_historico(cur, id_atendente)
        for pedido in historico:
            tree.insert("", "end", values=pedido)
    
    root = tk.Tk()
    root.title("Histórico de Vendas - Atendente")
    root.geometry("600x400")
    
    colunas = ("ID Pedido", "Cliente", "Valor Total", "Data")
    tree = ttk.Treeview(root, columns=colunas, show="headings")
    
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    
    tree.pack(expand=True, fill="both")
    
    btn_fechar = tk.Button(root, text="Fechar", command=root.destroy)
    btn_fechar.pack(pady=10)
    
    atualizar_tabela()
    root.mainloop()

def telaAtendenteAcesso(cur, conn, id, root):
    root.destroy()
    root = tk.Tk()
    root.title("Acesso Gerente")
    root.geometry("500x450")

    cur.execute("SELECT * FROM funcionario WHERE id_funcionario = %s", (id,))
    gerente = cur.fetchone()

    tk.Label(root, text=f"Bem-vindo - {gerente[1]}", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Histórico de vendas", width=20, command= lambda: telaHistorico(cur, id, root)).pack(pady=5)
    tk.Button(root, text="Alterar Dados", width=20, command= lambda: telaAlterarDados(cur, conn, id, root)).pack(pady=5)
    tk.Button(root, text="Excluir Cadastro", width=20, command= lambda: telaExcluirCadastro(cur,conn,id,root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=lambda: (root.destroy(), telaAtendente(cur, conn, root)) ).pack(pady=20)

    root.mainloop()

def telaExcluirCadastro(cur, conn, id, root):
    
    def excluirCadastro(cur, conn, id, root, senha_entry):
        senha_entry = senha_entry.get()

        cur.execute("""
            SELECT * FROM funcionario WHERE id_funcionario = %s
        """, (id,))
        Atendente = cur.fetchone() 
    
        if Atendente[4] == senha_entry:
            cur.execute("""
             DELETE FROM atendente WHERE id_funcionario = %s;
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

            cur.execute("SELECT * FROM atendente WHERE id_funcionario = %s", (id,))
            atendente = cur.fetchone()
        
            if atendente:
                if funcionario[4] == senha:
                    telaAtendenteAcesso(cur, conn, id, root)
                    root.destroy()
                else:
                    messagebox.showerror("Erro", "Senha incorreta!")
                    root.destroy()
            else:
                messagebox.showerror("Erro", "Atendente não encontrado ou o funcionário não é atendente!")
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

def telaAtendente(cur, conn, root):
    root = tk.Tk()
    root.title("Sistema de acesso Atendente")
    root.geometry("500x450")

    tk.Label(root, text="Bem-vindo - Atendente", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Acessar", width=20, command= lambda: acessar(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=root.destroy).pack(pady=20)

    root.mainloop()