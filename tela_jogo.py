from tkinter import *
from tkinter import messagebox
import os
import random

def criar_tela_jogo():
    jogo_window = Tk()
    jogo_window.title("Beach Defender - Jogo")
    jogo_window.geometry("800x600")
    jogo_window.resizable(False, False)

    # ======== FUNDO COM IMAGEM ========
    bg_image_path = "imgs/praia.png"
    if not os.path.exists(bg_image_path):
        messagebox.showerror("Erro", f"Imagem de fundo não encontrada: {bg_image_path}")
        jogo_window.destroy()
        return

    bg_img = PhotoImage(file=bg_image_path)
    bg_label = Label(jogo_window, image=bg_img)
    bg_label.place(x=0, y=0)

    # ======== NOME DO ADVERSÁRIO ========
    adversario_label = Label(jogo_window, text="KINGLER", font=("Verdana", 16, "bold"), bg="white")
    adversario_label.place(x=400, y=20, anchor="n")

    # ======== BARRA DE VIDA ========
    vida_canvas = Canvas(jogo_window, width=300, height=5, bg="white", highlightthickness=1, highlightbackground="#aaa")
    vida_canvas.place(x=400, y=60, anchor="n")
    vida_barra = vida_canvas.create_rectangle(0, 0, 300, 20, fill="green")

    # ======== POÇÕES (LADO ESQUERDO - MELHORADO) ========
    Label(jogo_window, text="POÇÕES", font=("Verdana", 14, "bold"), bg="#f0f0f0", relief="solid", bd=1).place(x=50, y=100, width=180, height=30)

    def criar_pocao(nome, bonus, preco, cor, y_pos):
        # Frame da poção com borda e fundo
        pocao_frame = Frame(jogo_window, bg=cor, relief="raised", bd=2, width=180, height=80)
        pocao_frame.place(x=50, y=y_pos)
        pocao_frame.pack_propagate(False)
        
        # Nome da poção
        Label(pocao_frame, text=nome, font=("Verdana", 10, "bold"), bg=cor).pack(pady=(5, 0))
        
        # Bônus
        Label(pocao_frame, text=bonus, bg=cor, font=("Verdana", 8)).pack()
        
        # Linha do botão e tempo
        linha_frame = Frame(pocao_frame, bg=cor)
        linha_frame.pack(fill=X, pady=5)
        
        # Botão de compra
        Button(linha_frame, text=f"R${preco}", font=("Verdana", 9, "bold"),
               bg="#ffcccc" if "Força" in nome else "#ccffcc" if "Sorte" in nome else "#ccffff",
               command=lambda: print(f"Comprou {nome}")).pack(side=LEFT, padx=10)
        
        # Tempo
        Label(linha_frame, text="Tempo: 00:00", bg=cor, font=("Verdana", 8)).pack(side=RIGHT, padx=10)

    criar_pocao("Poção Sorte", "+2x Chance Crítica", 200, "#e8f4fd", 140)
    criar_pocao("Poção Força", "+2x Dano", 500, "#fde8e8", 230)
    criar_pocao("Poção Fortuna", "+2x Dinheiro", 300, "#e8fde8", 320)

    # ======== VARIÁVEIS DO JOGO ========
    inimigos = [
        {"nome": "KINGLER", "vida_max": 100, "vida_atual": 100, "imagem": "imgs/kingler.png", "dinheiro_min": 73, "dinheiro_max": 100, "subsample_x": 3, "subsample_y": 2},
        {"nome": "SHARPEDO", "vida_max": 150, "vida_atual": 150, "imagem": "imgs/sharpedo.png", "dinheiro_min": 90, "dinheiro_max": 130, "subsample_x": 2, "subsample_y": 1},
        {"nome": "GYARADOS", "vida_max": 250, "vida_atual": 250, "imagem": "imgs/gyarados.png", "dinheiro_min": 100, "dinheiro_max": 200, "subsample_x": 3, "subsample_y": 2}
    ]
    inimigo_atual = 0
    dano_jogador = 5
    dinheiro = 0

    # ======== IMAGEM DO INIMIGO (CENTRO) ========
    inimigo_label = Label(jogo_window, bg="#ffffff", cursor="hand2")
    inimigo_label.place(x=400, y=300, anchor="center")

    def trocar_inimigo():
        nonlocal inimigo_atual
        if inimigo_atual < len(inimigos) - 1:
            inimigo_atual += 1
        else:
            inimigo_atual = 0
        
        inimigos[inimigo_atual]["vida_atual"] = inimigos[inimigo_atual]["vida_max"]
        adversario_label.config(text=inimigos[inimigo_atual]["nome"])
        inimigo_info_label.config(text=f"INIMIGO: {inimigo_atual + 1}/3")
        carregar_imagem_inimigo()
        print(f"Novo inimigo: {inimigos[inimigo_atual]['nome']}")

    def carregar_imagem_inimigo():
        try:
            inimigo_img = PhotoImage(file=inimigos[inimigo_atual]["imagem"])
            subsample_x = inimigos[inimigo_atual]["subsample_x"]
            subsample_y = inimigos[inimigo_atual]["subsample_y"]
            inimigo_img = inimigo_img.subsample(subsample_x, subsample_y)
            inimigo_label.config(image=inimigo_img)
            inimigo_label.image = inimigo_img
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            inimigo_label.config(text="[CLIQUE AQUI PARA ATACAR]", font=("Verdana", 10))

    def atacar_inimigo():
        nonlocal dinheiro
        
        inimigos[inimigo_atual]["vida_atual"] -= dano_jogador
        vida_atual = inimigos[inimigo_atual]["vida_atual"]
        vida_max = inimigos[inimigo_atual]["vida_max"]
        
        nova_largura = max(0, (vida_atual / vida_max) * 300)
        vida_canvas.coords(vida_barra, 0, 0, nova_largura, 20)
        
        if vida_atual > vida_max * 0.5:
            vida_canvas.itemconfig(vida_barra, fill="green")
        elif vida_atual > vida_max * 0.2:
            vida_canvas.itemconfig(vida_barra, fill="yellow")
        else:
            vida_canvas.itemconfig(vida_barra, fill="red")
        
        print(f"Atacou! Vida do {inimigos[inimigo_atual]['nome']}: {vida_atual}")
        
        if vida_atual <= 0:
            dinheiro_min = inimigos[inimigo_atual]["dinheiro_min"]
            dinheiro_max = inimigos[inimigo_atual]["dinheiro_max"]
            dinheiro_ganho = random.randint(dinheiro_min, dinheiro_max)
            
            dinheiro += dinheiro_ganho
            dinheiro_label.config(text=f"R$ {dinheiro}")
            print(f"{inimigos[inimigo_atual]['nome']} derrotado! +R${dinheiro_ganho}")
            trocar_inimigo()

    inimigo_label.bind("<Button-1>", lambda e: atacar_inimigo())
    carregar_imagem_inimigo()

    # ======== INFORMAÇÕES (LADO DIREITO) ========
    info_bg = Frame(jogo_window, bg="#f0f0f0", relief="solid", bd=1, width=150, height=200)
    info_bg.place(x=620, y=100)
    info_bg.pack_propagate(False)

    Label(info_bg, text="INFORMAÇÕES", font=("Verdana", 12, "bold"), bg="#f0f0f0").pack(pady=10)
    Label(info_bg, text="DINHEIRO", font=("Verdana", 10, "bold"), bg="#f0f0f0").pack()
    dinheiro_label = Label(info_bg, text="R$ 0", font=("Verdana", 12, "bold"), bg="gold")
    dinheiro_label.pack(pady=5)
    Label(info_bg, text=f"DANO: {dano_jogador}", font=("Verdana", 9), bg="#f0f0f0").pack(pady=5)
    inimigo_info_label = Label(info_bg, text="INIMIGO: 1/3", font=("Verdana", 9), bg="#f0f0f0")
    inimigo_info_label.pack(pady=5)

    # ======== SQUIRTLE (DIREITA, ACIMA DA LOJA) ========
    try:
        jogador_img = PhotoImage(file="imgs/squirtle.png")
        jogador_img = jogador_img.subsample(2, 2)
        jogador_label = Label(jogo_window, image=jogador_img, bg="#f0f0f0")
        jogador_label.image = jogador_img
        jogador_label.place(x=650, y=320)
    except:
        jogador_label = Label(jogo_window, text="[SQUIRTLE]", font=("Verdana", 10), bg="#f0f0f0")
        jogador_label.place(x=650, y=320)

    # ======== LOJA (PARTE INFERIOR - MELHORADA) ========
    loja_bg = Frame(jogo_window, bg="#f8d26d", relief="raised", bd=2, height=100)
    loja_bg.place(x=0, y=500, relwidth=1)

    Label(loja_bg, text="LOJA", font=("Verdana", 14, "bold"), bg="#f8d26d").pack(pady=5)

    # Container para os itens da loja
    itens_container = Frame(loja_bg, bg="#f8d26d")
    itens_container.pack(expand=True)

    def criar_item(nome, preco, cor, comando, x_offset):
        item_frame = Frame(itens_container, bg="#f8d26d", width=120, height=70)
        item_frame.pack(side=LEFT, padx=15)
        item_frame.pack_propagate(False)
        
        # Imagem do item
        Label(item_frame, text=f"[{nome.upper()}]", bg="#f8d26d", font=("Verdana", 8)).pack(pady=2)
        
        # Nome do item
        Label(item_frame, text=nome, bg="#f8d26d", font=("Verdana", 9, "bold")).pack()
                
        # Botão de compra
        if comando:
            Button(item_frame, text=f"R${preco}", bg=cor, font=("Verdana", 8), 
                   command=comando, width=8).pack()

    criar_item("Doce Raro", 200, "lightgreen", lambda: print("Comprou Doce Raro"), 0)
    criar_item("Rede", 2000, "lightgreen", lambda: print("Comprou Rede"), 1)
    criar_item("Coco", 400, "lightgreen", lambda: print("Comprou Coco"), 2)
    criar_item("Mega Bracelete", "0,99", "lightblue", lambda: print("Comprou o bracelete"), 3)

    # ======== BOTÃO AJUDA ========
    ajuda_frame = Frame(itens_container, bg="#f8d26d", width=120, height=70)
    ajuda_frame.pack(side=LEFT, padx=15)
    ajuda_frame.pack_propagate(False)
    
    Button(ajuda_frame, text="AJUDA", bg="lightblue", font=("Verdana", 10, "bold"),
           command=mostrar_ajuda, width=10, height=2).pack(expand=True)

    def mostrar_ajuda():
        ajuda = Toplevel(jogo_window)
        ajuda.title("Ajuda - Beach Defender")
        ajuda.geometry("600x400")
        texto = """
🎮 Beach Defender - Guia Completo 🎮

Como Atacar:
- Clique na imagem do inimigo para atacar.
- Cada ataque causa dano base ao inimigo.

Poções:
- Poção da Sorte: +2x chance crítica
- Poção da Força: +2x dano nos ataques
- Poção da Fortuna: +2x dinheiro ganho

Mega Bracelete:
- Use para evoluir seu Pokémon.
- Cada compra custa R$0,99.

Objetivo:
- Derrote todos os inimigos (Kingler → Sharpedo → Gyarados).
- Utilize poções e o Mega Bracelete estrategicamente para vencer.

Recompensas:
- Kingler: R$73-100
- Sharpedo: R$90-130  
- Gyarados: R$100-200
        """
        Label(ajuda, text=texto, justify=LEFT, font=("Verdana", 9), padx=10, pady=10).pack()
        Button(ajuda, text="Fechar", command=ajuda.destroy).pack(pady=10)
    
    jogo_window.mainloop()