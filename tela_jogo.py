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
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ======== FRAME PRINCIPAL TRANSPARENTE ========
    main_frame = Frame(jogo_window, bg="#ffffff", relief="flat")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ======== NOME DO ADVERSÁRIO ========
    adversario_label = Label(main_frame, text="KINGLER", font=("Verdana", 16, "bold"), bg="white")
    adversario_label.pack(pady=(0, 0))

    # ======== BARRA DE VIDA ========
    vida_canvas = Canvas(main_frame, width=300, height=20, bg="white", highlightthickness=1, highlightbackground="#aaa")
    vida_canvas.pack(pady=5)
    vida_barra = vida_canvas.create_rectangle(0, 0, 300, 20, fill="green")

    # ======== FRAME CENTRAL ========
    centro_frame = Frame(main_frame, bg="white")
    centro_frame.pack(fill=BOTH, expand=True, pady=5)

    # ======== POÇÕES (MAIS PARA CIMA) ========
    pocoes_frame = Frame(centro_frame, bg="#f0f0f0", width=200, height=250)
    pocoes_frame.pack(side=LEFT, fill=Y, padx=(0, 10))
    pocoes_frame.pack_propagate(False)

    Label(pocoes_frame, text="POÇÕES", font=("Verdana", 12, "bold"), bg="#f0f0f0").pack(pady=5)

    def criar_pocao(nome, bonus, preco, cor):
        frame = Frame(pocoes_frame, bg=cor, relief="solid", bd=1)
        frame.pack(fill=X, padx=5, pady=3)
        Label(frame, text=nome, font=("Verdana", 9, "bold"), bg=cor).pack(pady=1)
        Label(frame, bg=cor, font=("Verdana", 7)).pack()
        Label(frame, text=bonus, bg=cor, font=("Verdana", 8)).pack()
        Button(frame, text=f"R${preco}", font=("Verdana", 9, "bold"),
               bg="#ffcccc" if "Força" in nome else "#ccffcc" if "Sorte" in nome else "#ccffff",
               command=lambda: print(f"Comprou {nome}")).pack(pady=2)
        Label(frame, text="Tempo: 00:00", bg=cor, font=("Verdana", 7)).pack(pady=(0, 3))

    criar_pocao("Poção Sorte", "+2x Chance Crítica", 200, "#e8f4fd")
    criar_pocao("Poção Força", "+2x Dano", 500, "#fde8e8")
    criar_pocao("Poção Fortuna", "+2x Dinheiro", 300, "#e8fde8")

    # ======== COMBATE ========
    combate_frame = Frame(centro_frame, bg="#ffffff")
    combate_frame.pack(side=LEFT, fill=BOTH, expand=True)

    # Variáveis do jogo
    inimigos = [
        {"nome": "KINGLER", "vida_max": 100, "vida_atual": 100, "imagem": "imgs/kingler.png", "dinheiro_min": 73, "dinheiro_max": 100, "subsample_x": 2, "subsample_y": 3},  # Kingler menor
        {"nome": "SHARPEDO", "vida_max": 150, "vida_atual": 150, "imagem": "imgs/sharpedo.png", "dinheiro_min": 90, "dinheiro_max": 130, "subsample_x": 2, "subsample_y": 1},  # Sharpedo maior
        {"nome": "GYARADOS", "vida_max": 250, "vida_atual": 250, "imagem": "imgs/gyarados.png", "dinheiro_min": 100, "dinheiro_max": 200, "subsample_x": 2, "subsample_y": 3}   # Gyarados menor
    ]
    inimigo_atual = 0
    dano_jogador = 5
    dinheiro = 0

    def trocar_inimigo():
        nonlocal inimigo_atual
        if inimigo_atual < len(inimigos) - 1:
            inimigo_atual += 1
        else:
            # Volta para o primeiro inimigo (ciclo infinito)
            inimigo_atual = 0
        
        # Resetar vida do inimigo
        inimigos[inimigo_atual]["vida_atual"] = inimigos[inimigo_atual]["vida_max"]
        
        # Atualizar nome
        adversario_label.config(text=inimigos[inimigo_atual]["nome"])
        # Atualizar contador
        inimigo_info_label.config(text=f"INIMIGO: {inimigo_atual + 1}/3")
        # Atualizar imagem
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
        
        # Reduzir vida do inimigo atual
        inimigos[inimigo_atual]["vida_atual"] -= dano_jogador
        vida_atual = inimigos[inimigo_atual]["vida_atual"]
        vida_max = inimigos[inimigo_atual]["vida_max"]
        
        # Atualizar barra de vida
        nova_largura = max(0, (vida_atual / vida_max) * 300)
        vida_canvas.coords(vida_barra, 0, 0, nova_largura, 20)
        
        # Mudar cor da barra conforme a vida
        if vida_atual > vida_max * 0.5:
            vida_canvas.itemconfig(vida_barra, fill="green")
        elif vida_atual > vida_max * 0.2:
            vida_canvas.itemconfig(vida_barra, fill="yellow")
        else:
            vida_canvas.itemconfig(vida_barra, fill="red")
        
        print(f"Atacou! Vida do {inimigos[inimigo_atual]['nome']}: {vida_atual}")
        
        # Se inimigo morrer
        if vida_atual <= 0:
            # Calcular dinheiro baseado no inimigo
            dinheiro_min = inimigos[inimigo_atual]["dinheiro_min"]
            dinheiro_max = inimigos[inimigo_atual]["dinheiro_max"]
            dinheiro_ganho = random.randint(dinheiro_min, dinheiro_max)
            
            dinheiro += dinheiro_ganho
            dinheiro_label.config(text=f"R$ {dinheiro}")
            print(f"{inimigos[inimigo_atual]['nome']} derrotado! +R${dinheiro_ganho}")
            
            # Avançar para o próximo inimigo (ciclo infinito)
            trocar_inimigo()

    # Frame para centralizar a imagem do inimigo
    inimigo_container = Frame(combate_frame, bg="#ffffff")
    inimigo_container.pack(expand=True, fill=BOTH)

    # Imagem do inimigo - CLICÁVEL E CENTRALIZADA
    inimigo_label = Label(inimigo_container, bg="#ffffff", cursor="hand2")
    inimigo_label.pack(expand=True)  # Centraliza vertical e horizontalmente
    inimigo_label.bind("<Button-1>", lambda e: atacar_inimigo())
    
    # Carregar primeira imagem
    carregar_imagem_inimigo()

    # ======== INFORMAÇÕES ========
    info_frame = Frame(centro_frame, bg="#f0f0f0", width=150)
    info_frame.pack(side=LEFT, fill=Y)
    info_frame.pack_propagate(False)

    Label(info_frame, text="DINHEIRO", font=("Verdana", 11, "bold"), bg="#f0f0f0").pack(pady=10)
    dinheiro_label = Label(info_frame, text="R$ 0", font=("Verdana", 12, "bold"), bg="gold")
    dinheiro_label.pack(pady=5)
    Label(info_frame, text=f"DANO: {dano_jogador}", font=("Verdana", 9), bg="#f0f0f0").pack(pady=5)
    inimigo_info_label = Label(info_frame, text="INIMIGO: 1/3", font=("Verdana", 9), bg="#f0f0f0")
    inimigo_info_label.pack(pady=5)

    # SQUIRTLE NO FRAME DE INFORMAÇÕES (ENCOSTADO NA PARTE INFERIOR)
    try:
        jogador_img = PhotoImage(file="imgs/squirtle.png")
        jogador_img = jogador_img.subsample(2, 2)
        jogador_label = Label(info_frame, image=jogador_img, bg="#f0f0f0")
        jogador_label.image = jogador_img
        jogador_label.pack(side=BOTTOM, pady=10)
    except:
        jogador_label = Label(info_frame, text="[SQUIRTLE]", font=("Verdana", 10), bg="#f0f0f0")
        jogador_label.pack(side=BOTTOM, pady=10)

    # ======== LOJA ========
    loja_frame = Frame(main_frame, bg="#f8d26d", height=100)
    loja_frame.pack(fill=X, pady=(10, 0))
    loja_frame.pack_propagate(False)

    Label(loja_frame, text="LOJA", font=("Verdana", 12, "bold"), bg="#f8d26d").pack(pady=5)

    itens_frame = Frame(loja_frame, bg="#f8d26d")
    itens_frame.pack()

    def criar_item(nome, preco, cor, comando):
        frame = Frame(itens_frame, bg="#f8d26d")
        frame.pack(side=LEFT, padx=10)
        Label(frame, text=f"[IMAGEM {nome.upper()}]", bg="#f8d26d", font=("Verdana", 7)).pack()
        Label(frame, text=nome, bg="#f8d26d", font=("Verdana", 9)).pack()
        Button(frame, text=f"R${preco}", bg=cor, command=comando).pack(pady=3)

    criar_item("Doce Raro", 200, "lightgreen", lambda: print("Comprou Doce Raro"))
    criar_item("Rede de Pesca", 2000, "lightgreen", lambda: print("Comprou Rede"))
    criar_item("Coco", 400, "lightgreen", lambda: print("Comprou Coco"))
    criar_item("Mega Bracelete", "0,99", "lightblue", None)

    # ======== BOTÃO AJUDA ========
    ajuda_frame = Frame(itens_frame, bg="#f8d26d")
    ajuda_frame.pack(side=LEFT, padx=10)

    # Botão Ajuda separado
    ajuda_btn_frame = Frame(itens_frame, bg="#f8d26d")
    ajuda_btn_frame.pack(side=LEFT, padx=10)
    
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
    
    Button(ajuda_btn_frame, text="AJUDA", bg="lightblue", font=("Verdana", 10, "bold"),
           command=mostrar_ajuda, width=8, height=2).pack()

    jogo_window.mainloop()