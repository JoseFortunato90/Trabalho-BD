import tkinter as tk
from tkinter import messagebox
import psycopg2
import telasCliente, telasGerente

def conectar_bd():
    try:
        return psycopg2.connect(
            dbname="TrabalhoBD",
            user="postgres",
            password="senha"
        )
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def abrir_tela_atendente():
    messagebox.showinfo("Atendente", "Você entrou como Atendente.")


# Conectar ao banco
conn = conectar_bd()
cur = conn.cursor() if conn else None

# Criar a janela principal

root = tk.Tk()
root.title("Sistema de Gerenciamento")
root.geometry("500x450")

tk.Label(root, text="Bem-vindo ao Sistema", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Cliente", width=20, command= lambda: telasCliente.telaCliente(cur, conn, root)).pack(pady=5)
tk.Button(root, text="Gerente", width=20, command= lambda: telasGerente.telaGerente(cur, conn, root)).pack(pady=5)
tk.Button(root, text="Atendente", width=20, command=abrir_tela_atendente).pack(pady=5)
tk.Button(root, text="Sair", width=20, command=root.quit).pack(pady=20)

root.mainloop()

if cur:
    cur.close()
if conn:
    conn.close()

