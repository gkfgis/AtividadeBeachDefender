from tkinter import *
from tkinter import ttk


def inicializar_variaveis():
    # Criar janela principal
    root = Tk()
    root.title("Beach Defender")
    root.resizable(width=False, height=False)
    root.geometry("400x300")
    
    # Criar frame principal
    frm = ttk.Frame(root, padding=20)
    frm.pack(expand=True, fill=BOTH)
    
    return root, frm