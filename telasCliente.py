import tkinter as tk
from tkinter import messagebox, ttk
import telasCompras


def telaAlterarDados(cur, conn, cpf, root):
    root.destroy()
    
    def alterar_dados_cliente(cur,conn,root):
        campo_selecionado = campo_var.get().strip()
        novo_valor = entrada_valor.get().strip()

        if not novo_valor:
            messagebox.showerror("Erro", "Opção inválida! Digite um valor.")
            return

        try:
            if campo_selecionado == "Nome":
                cur.execute("UPDATE Cliente SET nome = %s WHERE Cpf = %s", (novo_valor, cpf))
                conn.commit()
                messagebox.showinfo("Sucesso", "Nome atualizado com sucesso!")
            elif campo_selecionado == "Senha":
                cur.execute("UPDATE Cliente SET senha = %s WHERE Cpf = %s", (novo_valor, cpf))
                conn.commit()
                messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")
            else:
                messagebox.showerror("Erro", f"Opção inválida! Valor recebido: {campo_selecionado}")
                return
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar os dados: {e}")
        root.destroy()
        telaCliente(cur,conn,root)
    
    root = tk.Tk()
    root.title("Alterar Dados do Cliente")
    root.geometry("300x200")
    
    tk.Label(root, text="Escolha o dado a alterar:").pack()
    
    opcoes = ["Nome", "Senha"]
    campo_var = tk.StringVar(root)
    campo_var.set(opcoes[0])  
    
    option_menu = tk.OptionMenu(root, campo_var, *opcoes)
    option_menu.pack()
    
    tk.Label(root, text="Novo valor:").pack()
    entrada_valor = tk.Entry(root)
    entrada_valor.pack()
    
    tk.Button(root, text="Confirmar", command = lambda: alterar_dados_cliente(cur, conn,root)).pack(pady=10)
    tk.Button(root, text="Cancelar", command = lambda: (telaClienteAcesso(cur, conn, cpf, root),root.destroy)).pack(pady=10)
    
    root.mainloop()

def telaExcluirCadastro(cur, conn, cpf, root):
    
    def excluirCadastro(cur, conn, cpf, root, senha_entry):
        senha_entry = senha_entry.get()

        cur.execute("""
            SELECT * FROM Cliente WHERE Cpf = %s
        """, (cpf,))
        cliente = cur.fetchone() 
    
        if cliente[2] == senha_entry:
            cur.execute("DELETE FROM Cliente WHERE Cpf = %s AND senha = %s;", (cpf, senha_entry))
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

        tk.Button(root, text="Excluir Cadastro", command=lambda: excluirCadastro(cur,conn,cpf,root,senha_entry)).pack()

        root.mainloop()
    root.destroy()
    resposta = messagebox.askyesno("Confirmação", "Deseja excluir seu cadastro permanentemente?")
    if resposta:
        tela(cur,conn,cpf,root)
        root.destroy()
    else:
        return

def telaClienteAcesso(cur, conn, cpf, root):
    root.destroy()
    root = tk.Tk()
    root.title("Acesso Cliente")
    root.geometry("500x450")

    cur.execute("SELECT * FROM Cliente WHERE Cpf = %s", (cpf,))
    cliente = cur.fetchone()

    tk.Label(root, text=f"Bem-vindo - {cliente[1]}", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Comprar", width=20, command= lambda: telasCompras.telaCompra(cur, conn, cpf, root)).pack(pady=5)
    tk.Button(root, text="Histórico de compras", width=20, command= lambda: telasCompras.telaHistoricoCompras(cur, cpf)).pack(pady=5)
    tk.Button(root, text="Alterar Dados", width=20, command= lambda: telaAlterarDados(cur, conn, cpf, root)).pack(pady=5)
    tk.Button(root, text="Excluir Cadastro", width=20, command= lambda: telaExcluirCadastro(cur,conn,cpf,root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=lambda: (root.destroy(), telaCliente(cur, conn, root)) ).pack(pady=20)

    root.mainloop()

def acessar(cur, conn, root):

    root.destroy()
    def acesso(cur, conn, cpf_entry, senha_entry, root):
        cpf = cpf_entry.get()
        senha = senha_entry.get()

        if not cpf or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            root.quit
            return
        
        try:
            cpf = int(cpf)
            cur.execute("SELECT * FROM Cliente WHERE Cpf = %s", (cpf,))
            cliente = cur.fetchone()
        
            if cliente:
                if cliente[2] == senha:
                    telaClienteAcesso(cur, conn, cpf, root)
                    root.destroy()
                else:
                    messagebox.showerror("Erro", "Senha incorreta!")
                    root.destroy()
            else:
                messagebox.showerror("Erro", "Cliente não encontrado!")
                root.destroy()
        
        except ValueError:
            messagebox.showerror("Erro", "CPF deve conter apenas números.")
        root.quit

    root = tk.Tk()
    root.title("Acesso Cliente")
    root.geometry("300x200")
    
    tk.Label(root, text="CPF:").pack()
    cpf_entry = tk.Entry(root)
    cpf_entry.pack()
    
    tk.Label(root, text="Senha:").pack()
    senha_entry = tk.Entry(root, show="*")
    senha_entry.pack()
    
    tk.Button(root, text="Acessar", command=lambda: acesso(cur, conn, cpf_entry, senha_entry, root)).pack()
    
    root.mainloop()

def cadastrar(cur, conn, root):
    
    def cadastro(cur, conn, cpf_entry, senha_entry, nome_entry, root):
        cpf = cpf_entry.get()
        senha = senha_entry.get()
        nome = nome_entry.get()

        if not cpf or not senha or not nome:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        cur.execute("""
        SELECT * FROM Cliente WHERE Cpf = %s
        """, (cpf,))

        cliente = cur.fetchone()
        if cliente:
            messagebox.showerror("Erro", "Cliente já cadastrado")
            root.quit
            return

        cur.execute(f"""
        INSERT INTO Cliente (Cpf, nome, senha)
        VALUES ({cpf}, '{nome}', '{senha}')
        """)
        conn.commit()
        messagebox.showinfo("Cliente", "cadastrado com sucesso.")
        root.destroy


    root = tk.Tk()
    root.title("Cadastro Cliente")
    root.geometry("300x200")
    
    tk.Label(root, text="CPF:").pack()
    cpf_entry = tk.Entry(root)
    cpf_entry.pack()

    tk.Label(root, text="Nome:").pack()
    nome_entry = tk.Entry(root)
    nome_entry.pack()
    
    tk.Label(root, text="Senha:").pack()
    senha_entry = tk.Entry(root)
    senha_entry.pack()
    
    tk.Button(root, text="Cadastrar", command=lambda: cadastro(cur, conn, cpf_entry, senha_entry,nome_entry, root)).pack()
    
    root.mainloop()

def telaCliente(cur, conn, root):
    root = tk.Tk()
    root.title("Sistema de acesso Cliente")
    root.geometry("500x450")

    tk.Label(root, text="Bem-vindo - Cliente", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Acessar", width=20, command= lambda: acessar(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Cadastrar", width=20, command= lambda: cadastrar(cur, conn, root)).pack(pady=5)
    tk.Button(root, text="Sair", width=20, command=root.destroy).pack(pady=20)

    root.mainloop()