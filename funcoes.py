from tkinter import *
from tela_jogo import criar_tela_jogo

def abrir_jogo(root):
    root.destroy()  # Fecha a tela inicial
    jogo_window = criar_tela_jogo()  # Cria a tela do jogo
    jogo_window.mainloop()

def criar_menu(root, bg_photo):
    # Configurar o background
    if bg_photo:
        bg_label = Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_photo
    
    # Título do jogo
    title_label = Label(root, text="BEACH DEFENDER", font=("Arial", 16, "bold"), 
                       fg='white', bg='#333333', relief='solid', bd=1)
    title_label.place(relx=0.5, rely=0.25, anchor='center')
    
    # Botão Jogar
    play_button = Button(root, text="JOGAR", width=20, height=2, 
                        font=("Arial", 10, "bold"), 
                        bg='#4CAF50', fg='white',
                        activebackground='#45a049',
                        command=lambda: abrir_jogo(root))
    play_button.place(relx=0.5, rely=0.45, anchor='center')
    
    # Botão Sair
    exit_button = Button(root, text="SAIR", width=20, height=2,
                        font=("Arial", 10, "bold"),
                        bg='#f44336', fg='white',
                        activebackground='#da190b',
                        command=root.destroy)
    exit_button.place(relx=0.5, rely=0.65, anchor='center')
    
    return play_button