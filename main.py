from tkinter import *
from tkinter import ttk

# Criar janela principal
root = Tk()
root.title("Beach Defender")
root.resizable(width=False, height=False)
root.geometry("400x300")  # Definindo tamanho fixo

# Criar frame principal
frm = ttk.Frame(root, padding=20)
frm.pack(expand=True, fill=BOTH)

# Título do jogo
title_label = Label(frm, text="BEACH DEFENDER", font=("Arial", 16), bg="#d3d3d3", width=20, relief="solid", bd=2)
title_label.pack(pady=(20, 40))

# Botão Jogar
play_button = Button(frm, text="JOGAR", width=20, height=2)
play_button.pack(pady=10)

# Botão Sair
exit_button = Button(frm, text="SAIR", width=20, height=2, command=root.destroy)
exit_button.pack(pady=10)

# Rodar a janela
root.mainloop()
