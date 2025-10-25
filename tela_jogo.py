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
    dano_jogador = [5,10,20,35,60]
    dinheiro = 0
    coco_ativo = False
    cocos_comprados = 0

    dano_atual = 0
    valor_doce = [100,200,300]  # Só 3 níveis para Doce Raro
    mega_bracelete_comprado = False
    mega_bracelete_disponivel = False
    
    # ======== IMAGEM DO INIMIGO (CENTRO) ========
    inimigo_label = Label(jogo_window, bg="#ffffff", cursor="hand2")
    inimigo_label.place(x=400, y=300, anchor="center")

    def trocar_inimigo():
        nonlocal inimigo_atual, mega_bracelete_disponivel
        
        if inimigo_atual < len(inimigos) - 1:
            inimigo_atual += 1
        else:
            inimigo_atual = 0
            
            # Verificar se derrotou o Gyarados e tem todos os doces comprados
            if dano_atual >= 3 and not mega_bracelete_comprado:
                # 15% de chance de dropar o Mega Bracelete
                if random.random() <= 0.15:
                    mega_bracelete_disponivel = True
                    mega_bracelete_button.config(state="normal")
                    print("🎉 Mega Bracelete disponível para compra!")
        
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
        
        inimigos[inimigo_atual]["vida_atual"] -= dano_jogador[dano_atual]
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
    dano_label = Label(info_bg, text=f"DANO: {dano_jogador[dano_atual]}", font=("Verdana", 9), bg="#f0f0f0")
    dano_label.pack(pady=5)
    coco_label = Label(info_bg, text="COCOS: 0/30", font=("Verdana", 9), bg="#f0f0f0")
    coco_label.pack(pady=2)
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

    # ======== LOJA (PARTE INFERIOR - SUBIDA) ========
    loja_bg = Frame(jogo_window, bg="#f8d26d", relief="raised", bd=2, height=80)
    loja_bg.place(x=0, y=480, relwidth=1)

    Label(loja_bg, text="LOJA", font=("Verdana", 14, "bold"), bg="#f8d26d").pack(pady=3)

    # Container para os itens da loja
    itens_container = Frame(loja_bg, bg="#f8d26d")
    itens_container.pack(expand=True)
    
    # Variáveis para os botões
    doce_rarro_button = None
    mega_bracelete_button = None
    def dano_coco_periodico():
        if coco_ativo:
            inimigos[inimigo_atual]["vida_atual"] -= cocos_comprados*5


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

            if vida_atual <= 0:
                dinheiro_ganho = random.randint(inimigos[inimigo_atual]["dinheiro_min"], inimigos[inimigo_atual]["dinheiro_max"])
                nonlocal dinheiro
                dinheiro += dinheiro_ganho
                dinheiro_label.config(text=f"R$ {dinheiro}")
                trocar_inimigo()

        jogo_window.after(5000, dano_coco_periodico)  # Continua repetindo

    def comprarCoco():
        nonlocal dinheiro, cocos_comprados, coco_ativo

        if cocos_comprados >= 30:
            print("⚠️ Limite de 30 cocos atingido!")
            return

        if dinheiro >= 400:
            dinheiro -= 400
            cocos_comprados += 1
            coco_ativo = True
            dinheiro_label.config(text=f"R$ {dinheiro}")

            # ✅ Atualiza contador na tela
            coco_label.config(text=f"Cocos: {cocos_comprados}/30")

            print(f"🥥 Coco comprado! Total: {cocos_comprados}")
        else:
            print("Dinheiro insuficiente!")

    
    def comprarDoceRaro():
        nonlocal dinheiro, dano_atual
        
        if dano_atual < len(valor_doce) and dinheiro >= valor_doce[dano_atual]:
            dinheiro -= valor_doce[dano_atual]
            dano_atual += 1
            
            # Atualizar displays
            dinheiro_label.config(text=f"R$ {dinheiro}")
            dano_label.config(text=f"DANO: {dano_jogador[dano_atual]}")
            
            if dano_atual < len(valor_doce):
                doce_rarro_button.config(text=f"R${valor_doce[dano_atual]}")
                print(f"Doce Raro comprado! Dano aumentou para {dano_jogador[dano_atual]}")
            else:
                doce_rarro_button.config(text="MAX", state="disabled")
                print("Doce Raro máximo alcançado! Derrote Gyarados para chance de Mega Bracelete")
        else:
            print("Dinheiro insuficiente ou upgrade máximo alcançado")

    def comprarMegaBracelete():
        nonlocal dinheiro, dano_atual, mega_bracelete_comprado
        
        if mega_bracelete_disponivel and dinheiro >= 1000 and not mega_bracelete_comprado:
            dinheiro -= 1000
            mega_bracelete_comprado = True
            dano_atual = 4  # Ativa o nível 4 de dano (35)
            
            # Atualizar displays
            dinheiro_label.config(text=f"R$ {dinheiro}")
            dano_label.config(text=f"DANO: {dano_jogador[dano_atual]}")
            mega_bracelete_button.config(text="COMPRADO", state="disabled")
            
            print("🎉 Mega Bracelete comprado! Dano máximo alcançado: 35")
        else:
            print("Mega Bracelete não disponível, dinheiro insuficiente ou já comprado")

    # ======== FUNÇÃO MOSTRAR AJUDA (AGORA DEFINIDA ANTES DO BOTÃO) ========
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

Sistema de Upgrades:
- Doce Raro: Compre 3 vezes para aumentar dano (5→10→20)
- Mega Bracelete: Desbloqueado após comprar 3 Doces Raros
  e derrotar Gyarados (15% de chance)
- Mega Bracelete custa R$1000 e aumenta dano para 35

Objetivo:
- Derrote todos os inimigos (Kingler → Sharpedo → Gyarados).
- Utilize poções e upgrades estrategicamente para vencer.

Recompensas:
- Kingler: R$73-100
- Sharpedo: R$90-130  
- Gyarados: R$100-200
        """
        Label(ajuda, text=texto, justify=LEFT, font=("Verdana", 9), padx=10, pady=10).pack()
        Button(ajuda, text="Fechar", command=ajuda.destroy).pack(pady=10)

    def criar_item(nome, preco, cor, comando, x_offset):
        nonlocal doce_rarro_button, mega_bracelete_button
        
        item_frame = Frame(itens_container, bg="#f8d26d", width=110, height=100)
        item_frame.pack(side=LEFT, padx=12)
        item_frame.pack_propagate(False)
        
        # Imagem do item
        Label(item_frame, text=f"[{nome.upper()}]", bg="#f8d26d", font=("Verdana", 7)).pack(pady=1)
        
        # Nome do item
        Label(item_frame, text=nome, bg="#f8d26d", font=("Verdana", 8, "bold")).pack()
                
        # Botão de compra
        if comando:
            if nome == "Doce Raro":
                # Para o Doce Raro, usar o preço atual baseado no dano_atual
                if dano_atual < len(valor_doce):
                    preco_atual = valor_doce[dano_atual]
                    doce_rarro_button = Button(item_frame, text=f"R${preco_atual}", bg=cor, font=("Verdana", 7), 
                           command=comprarDoceRaro, width=7)
                else:
                    doce_rarro_button = Button(item_frame, text="MAX", bg=cor, font=("Verdana", 7), 
                           state="disabled", width=7)
                doce_rarro_button.pack()
                
            elif nome == "Mega Bracelete":
                # Mega Bracelete começa desabilitado
                mega_bracelete_button = Button(item_frame, text="R$1000", bg=cor, font=("Verdana", 7), 
                       command=comprarMegaBracelete, width=7, state="disabled")
                mega_bracelete_button.pack()
                
            else:
                Button(item_frame, text=f"R${preco}", bg=cor, font=("Verdana", 7), 
                       command=comando, width=7).pack()

    criar_item("Doce Raro", 200, "lightgreen", comprarDoceRaro, 0)
    criar_item("Rede", 2000, "lightgreen", lambda: print("Comprou Rede"), 1)
    criar_item("Coco", 400, "lightgreen", lambda: comprarCoco(), 2)
    criar_item("Mega Bracelete", "0,99", "lightblue", comprarMegaBracelete, 3)

    # ======== BOTÃO AJUDA ========
    ajuda_frame = Frame(itens_container, bg="#f8d26d", width=110, height=60)
    ajuda_frame.pack(side=LEFT, padx=12)
    ajuda_frame.pack_propagate(False)
    
    Button(ajuda_frame, text="AJUDA", bg="lightblue", font=("Verdana", 9, "bold"),
           command=mostrar_ajuda, width=8, height=1).pack(expand=True)
    dano_coco_periodico()
    jogo_window.mainloop()