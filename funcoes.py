from tkinter import *

def abrir_jogo(root):
    root.destroy()

def criar_menu(frm, root):
    # Título do jogo
    title_label = Label(frm, text="BEACH DEFENDER", font=("Arial", 16), bg="#d3d3d3", width=20, relief="solid", bd=2)
    title_label.pack(pady=(20, 40))
    
    # Botão Jogar
    play_button = Button(frm, text="JOGAR", width=20, height=2,command=lambda:abrir_jogo(root))
    play_button.pack(pady=10)
    
    # Botão Sair
    exit_button = Button(frm, text="SAIR", width=20, height=2, command=root.destroy)
    exit_button.pack(pady=10)
    
    return play_button 
