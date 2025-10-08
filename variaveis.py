from tkinter import *
import os

def inicializar_variaveis():
    # Criar janela principal
    root = Tk()
    root.title("Beach Defender")
    root.resizable(width=False, height=False)
    root.geometry("400x300")
    
    # Carregar imagem
    bg_photo = None
    image_path = "imgs/imag.png"
    
    if os.path.exists(image_path):
        try:
            bg_photo = PhotoImage(file=image_path)
            print(f"Imagem carregada com sucesso: {image_path}")
        except Exception as e:
            print(f"Erro ao carregar {image_path}: {e}")
    else:
        print(f"Arquivo não encontrado: {image_path}")
    
    return root, bg_photo