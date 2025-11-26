from tkinter import *
from tkinter import messagebox
import os
import random
import time

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
    valor_doce = [100,200,300]
    mega_bracelete_comprado = False
    mega_bracelete_disponivel = False
    
    # ======== VARIÁVEIS DAS POÇÕES ========
    pocao_sorte_ativa = False
    pocao_forca_ativa = False
    pocao_fortuna_ativa = False
    tempo_sorte_restante = 0
    tempo_forca_restante = 0
    tempo_fortuna_restante = 0
    chance_critico_base = 0.15
    
    # ======== IMAGEM DO INIMIGO (CENTRO) ========
    inimigo_label = Label(jogo_window, bg="#ffffff", cursor="hand2")
    inimigo_label.place(x=400, y=300, anchor="center")

    def trocar_inimigo():
        nonlocal inimigo_atual, mega_bracelete_disponivel
        
        if inimigo_atual < len(inimigos) - 1:
            inimigo_atual += 1
        else:
            inimigo_atual = 0
            
            if dano_atual >= 3 and not mega_bracelete_comprado:
                if random.random() <= 0.15:
                    mega_bracelete_disponivel = True
                    mega_bracelete_button.config(state="normal")
        
        inimigos[inimigo_atual]["vida_atual"] = inimigos[inimigo_atual]["vida_max"]
        adversario_label.config(text=inimigos[inimigo_atual]["nome"])
        inimigo_info_label.config(text=f"INIMIGO: {inimigo_atual + 1}/3")
        carregar_imagem_inimigo()

    def carregar_imagem_inimigo():
        try:
            inimigo_img = PhotoImage(file=inimigos[inimigo_atual]["imagem"])
            subsample_x = inimigos[inimigo_atual]["subsample_x"]
            subsample_y = inimigos[inimigo_atual]["subsample_y"]
            inimigo_img = inimigo_img.subsample(subsample_x, subsample_y)
            inimigo_label.config(image=inimigo_img)
            inimigo_label.image = inimigo_img
        except Exception as e:
            inimigo_label.config(text="[CLIQUE AQUI PARA ATACAR]", font=("Verdana", 10))
    
    def calcular_dano_com_critico(dano_base):
        chance_critico = chance_critico_base
        if pocao_sorte_ativa:
            chance_critico *= 2
        
        if random.random() <= chance_critico:
            dano_final = dano_base * 2
            return dano_final
        return dano_base
    
    def calcular_dano_final(dano_base):
        dano_com_critico = calcular_dano_com_critico(dano_base)
        
        if pocao_forca_ativa:
            dano_final = dano_com_critico * 2
            return dano_final
        
        return dano_com_critico
    
    def calcular_dinheiro_ganho(dinheiro_base):
        if pocao_fortuna_ativa:
            dinheiro_final = dinheiro_base * 2
            return dinheiro_final
        return dinheiro_base

    def atacar_inimigo():
        nonlocal dinheiro
        
        dano_causado = calcular_dano_final(dano_jogador[dano_atual])
        inimigos[inimigo_atual]["vida_atual"] -= dano_causado
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
            dinheiro_min = inimigos[inimigo_atual]["dinheiro_min"]
            dinheiro_max = inimigos[inimigo_atual]["dinheiro_max"]
            dinheiro_ganho_base = random.randint(dinheiro_min, dinheiro_max)
            
            dinheiro_ganho = calcular_dinheiro_ganho(dinheiro_ganho_base)
            dinheiro += dinheiro_ganho
            dinheiro_label.config(text=f"R$ {dinheiro}")
            trocar_inimigo()
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

    # ======== POÇÕES (LADO ESQUERDO - TAMANHOS ORIGINAIS) ========
    Label(jogo_window, text="POÇÕES", font=("Verdana", 14, "bold"), bg="#f0f0f0", relief="solid", bd=1).place(x=50, y=100, width=180, height=30)

    tempo_sorte_label = None
    tempo_forca_label = None
    tempo_fortuna_label = None
    botao_sorte = None
    botao_forca = None
    botao_fortuna = None

    def formatar_tempo(segundos):
        minutos = segundos // 60
        segundos = segundos % 60
        return f"{minutos:02d}:{segundos:02d}"

    def atualizar_temporizadores():
        nonlocal tempo_sorte_restante, tempo_forca_restante, tempo_fortuna_restante
        nonlocal pocao_sorte_ativa, pocao_forca_ativa, pocao_fortuna_ativa
        
        if pocao_sorte_ativa:
            tempo_sorte_restante -= 1
            if tempo_sorte_restante <= 0:
                pocao_sorte_ativa = False
                tempo_sorte_label.config(text="Tempo: 00:00")
                botao_sorte.config(bg="#ccffcc")
            else:
                tempo_sorte_label.config(text=f"Tempo: {formatar_tempo(tempo_sorte_restante)}")
        
        if pocao_forca_ativa:
            tempo_forca_restante -= 1
            if tempo_forca_restante <= 0:
                pocao_forca_ativa = False
                tempo_forca_label.config(text="Tempo: 00:00")
                botao_forca.config(bg="#ffcccc")
            else:
                tempo_forca_label.config(text=f"Tempo: {formatar_tempo(tempo_forca_restante)}")
        
        if pocao_fortuna_ativa:
            tempo_fortuna_restante -= 1
            if tempo_fortuna_restante <= 0:
                pocao_fortuna_ativa = False
                tempo_fortuna_label.config(text="Tempo: 00:00")
                botao_fortuna.config(bg="#ccffff")
            else:
                tempo_fortuna_label.config(text=f"Tempo: {formatar_tempo(tempo_fortuna_restante)}")
        
        jogo_window.after(1000, atualizar_temporizadores)

    def comprar_pocao_sorte():
        nonlocal dinheiro, pocao_sorte_ativa, tempo_sorte_restante
        
        preco = 200
        if dinheiro >= preco:
            dinheiro -= preco
            dinheiro_label.config(text=f"R$ {dinheiro}")
            
            tempo_sorte_restante += 60
            pocao_sorte_ativa = True
            
            botao_sorte.config(bg="#aaffaa")
            tempo_sorte_label.config(text=f"Tempo: {formatar_tempo(tempo_sorte_restante)}")

    def comprar_pocao_forca():
        nonlocal dinheiro, pocao_forca_ativa, tempo_forca_restante
        
        preco = 500
        if dinheiro >= preco:
            dinheiro -= preco
            dinheiro_label.config(text=f"R$ {dinheiro}")
            
            tempo_forca_restante += 45
            pocao_forca_ativa = True
            
            botao_forca.config(bg="#ffaaaa")
            tempo_forca_label.config(text=f"Tempo: {formatar_tempo(tempo_forca_restante)}")

    def comprar_pocao_fortuna():
        nonlocal dinheiro, pocao_fortuna_ativa, tempo_fortuna_restante
        
        preco = 300
        if dinheiro >= preco:
            dinheiro -= preco
            dinheiro_label.config(text=f"R$ {dinheiro}")
            
            tempo_fortuna_restante += 90
            pocao_fortuna_ativa = True
            
            botao_fortuna.config(bg="#aaffff")
            tempo_fortuna_label.config(text=f"Tempo: {formatar_tempo(tempo_fortuna_restante)}")

    def criar_pocao(nome, bonus, preco, cor, y_pos, comando):
        pocao_frame = Frame(jogo_window, bg=cor, relief="raised", bd=2, width=180, height=80)
        pocao_frame.place(x=50, y=y_pos)
        pocao_frame.pack_propagate(False)
        
        Label(pocao_frame, text=nome, font=("Verdana", 10, "bold"), bg=cor).pack(pady=(5, 0))
        
        Label(pocao_frame, text=bonus, bg=cor, font=("Verdana", 8)).pack()
        
        linha_frame = Frame(pocao_frame, bg=cor)
        linha_frame.pack(fill=X, pady=5)
        
        nonlocal botao_sorte, botao_forca, botao_fortuna
        botao = Button(linha_frame, text=f"R${preco}", font=("Verdana", 9, "bold"),
               bg="#ccffcc" if "Sorte" in nome else "#ffcccc" if "Força" in nome else "#ccffff",
               command=comando, width=6)
        botao.pack(side=LEFT, padx=10)
        
        tempo_label = Label(linha_frame, text="Tempo: 00:00", bg=cor, font=("Verdana", 8))
        tempo_label.pack(side=RIGHT, padx=10)
        
        if "Sorte" in nome:
            nonlocal tempo_sorte_label
            tempo_sorte_label = tempo_label
            botao_sorte = botao
        elif "Força" in nome:
            nonlocal tempo_forca_label
            tempo_forca_label = tempo_label
            botao_forca = botao
        elif "Fortuna" in nome:
            nonlocal tempo_fortuna_label
            tempo_fortuna_label = tempo_label
            botao_fortuna = botao
            
        return botao, tempo_label

    criar_pocao("Poção Sorte", "+2x Chance Crítica", 200, "#e8f4fd", 140, comprar_pocao_sorte)
    criar_pocao("Poção Força", "+2x Dano", 500, "#fde8e8", 230, comprar_pocao_forca)
    criar_pocao("Poção Fortuna", "+2x Dinheiro", 300, "#e8fde8", 320, comprar_pocao_fortuna)

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

    itens_container = Frame(loja_bg, bg="#f8d26d")
    itens_container.pack(expand=True)
    
    doce_rarro_button = None
    mega_bracelete_button = None
    coco_button = None
    
    def dano_coco_periodico():
        if coco_ativo and cocos_comprados > 0:
            dano_base_coco = cocos_comprados * 5
            dano_causado = calcular_dano_final(dano_base_coco)
            
            inimigos[inimigo_atual]["vida_atual"] -= dano_causado
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
                dinheiro_min = inimigos[inimigo_atual]["dinheiro_min"]
                dinheiro_max = inimigos[inimigo_atual]["dinheiro_max"]
                dinheiro_ganho_base = random.randint(dinheiro_min, dinheiro_max)
                dinheiro_ganho = calcular_dinheiro_ganho(dinheiro_ganho_base)
                
                nonlocal dinheiro
                dinheiro += dinheiro_ganho
                dinheiro_label.config(text=f"R$ {dinheiro}")
                trocar_inimigo()

        jogo_window.after(5000, dano_coco_periodico)

    def comprarCoco():
        nonlocal dinheiro, cocos_comprados, coco_ativo

        preco_coco = 400 + (cocos_comprados * 150)

        if cocos_comprados >= 30:
            return

        if dinheiro >= preco_coco:
            dinheiro -= preco_coco
            cocos_comprados += 1
            coco_ativo = True
            dinheiro_label.config(text=f"R$ {dinheiro}")
            coco_label.config(text=f"COCOS: {cocos_comprados}/30")

            if cocos_comprados < 30:
                preco_proximo = 400 + (cocos_comprados * 150)
                coco_button.config(text=f"R${preco_proximo}")
            else:
                coco_button.config(text="MAX", state="disabled")

    
    def comprarDoceRaro():
        nonlocal dinheiro, dano_atual
        
        if dano_atual < len(valor_doce) and dinheiro >= valor_doce[dano_atual]:
            dinheiro -= valor_doce[dano_atual]
            dano_atual += 1
            
            dinheiro_label.config(text=f"R$ {dinheiro}")
            dano_label.config(text=f"DANO: {dano_jogador[dano_atual]}")
            
            if dano_atual < len(valor_doce):
                doce_rarro_button.config(text=f"R${valor_doce[dano_atual]}")
            else:
                doce_rarro_button.config(text="MAX", state="disabled")
    
    def comprarRede():
        nonlocal dinheiro

        if dinheiro >= 2000:
            dinheiro -= 2000
            dinheiro_label.config(text=f"R$ {dinheiro}")

            dano_causado = calcular_dano_final(300)
            inimigos[inimigo_atual]["vida_atual"] -= dano_causado
            vida_atual = inimigos[inimigo_atual]["vida_atual"]
            vida_max = inimigos[inimigo_atual]["vida_max"]

            nova_largura = max(0, (vida_atual / vida_max) * 300)
            vida_canvas.coords(vida_barra, 0, 0, nova_largura, 20)

            if vida_atual <= 0:
                dinheiro_min = inimigos[inimigo_atual]["dinheiro_min"]
                dinheiro_max = inimigos[inimigo_atual]["dinheiro_max"]
                dinheiro_ganho_base = random.randint(dinheiro_min, dinheiro_max)
                dinheiro_ganho = calcular_dinheiro_ganho(dinheiro_ganho_base)
                
                dinheiro += dinheiro_ganho
                dinheiro_label.config(text=f"R$ {dinheiro}")
                trocar_inimigo()
            
    def comprarMegaBracelete():
        nonlocal dinheiro, dano_atual, mega_bracelete_comprado
        
        if mega_bracelete_disponivel and dinheiro >= 1000 and not mega_bracelete_comprado:
            dinheiro -= 1000
            mega_bracelete_comprado = True
            dano_atual = 4
            
            dinheiro_label.config(text=f"R$ {dinheiro}")
            dano_label.config(text=f"DANO: {dano_jogador[dano_atual]}")
            mega_bracelete_button.config(text="COMPRADO", state="disabled")
            

    def mostrar_ajuda():
        ajuda = Toplevel(jogo_window)
        ajuda.title("Ajuda - Beach Defender")
        ajuda.geometry("600x400")
        texto = """
🎮 Beach Defender - Guia Completo 🎮

POÇÕES (ACUMULATIVAS!):
- Poção da Sorte: R$200 - +60 segundos de chance crítica dobrada
- Poção da Força: R$500 - +45 segundos de dano dobrado  
- Poção da Fortuna: R$300 - +90 segundos de dinheiro dobrado
- COMPRE VÁRIAS PARA ACUMULAR TEMPO!

Como Atacar:
- Clique na imagem do inimigo para atacar.
- 15% de chance de ACERTO CRÍTICO (2x dano)!
- Com Poção Sorte: 30% de chance crítica!

Sistema de Upgrades:
- Doce Raro: Compre 3 vezes (R$100→200→300)
- Mega Bracelete: R$1000 (desbloque após 3 Doces + Gyarados)

Itens Especiais:
- Coco: Dano automático (preço aumenta R$150 por compra)
- Rede: 300 de dano fixo (R$2000)

Objetivo:
- Derrote Kingler → Sharpedo → Gyarados
- Use poções estrategicamente!
        """
        Label(ajuda, text=texto, justify=LEFT, font=("Verdana", 9), padx=10, pady=10).pack()
        Button(ajuda, text="Fechar", command=ajuda.destroy).pack(pady=10)

    def carregar_imagem_item(caminho, subsample_x=4, subsample_y=4):
        try:
            img = PhotoImage(file=caminho)
            img = img.subsample(subsample_x, subsample_y)
            return img
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho}: {e}")
            return None

    def criar_item(nome, preco, cor, comando, x_offset, imagem_path=None):
        nonlocal doce_rarro_button, mega_bracelete_button, coco_button
        
        item_frame = Frame(itens_container, bg="#f8d26d", width=110, height=100)
        item_frame.pack(side=LEFT, padx=12)
        item_frame.pack_propagate(False)
        
        if imagem_path and os.path.exists(imagem_path):
            img = carregar_imagem_item(imagem_path)
            if img:
                item_label = Label(item_frame, image=img, bg="#f8d26d")
                item_label.image = img
                item_label.pack(pady=2)
            else:
                Label(item_frame, text=f"[{nome.upper()}]", bg="#f8d26d", font=("Verdana", 7)).pack(pady=1)
        else:
            Label(item_frame, text=f"[{nome.upper()}]", bg="#f8d26d", font=("Verdana", 7)).pack(pady=1)
        
        Label(item_frame, text=nome, bg="#f8d26d", font=("Verdana", 8, "bold")).pack()
                
        if comando:
            if nome == "Doce Raro":
                if dano_atual < len(valor_doce):
                    preco_atual = valor_doce[dano_atual]
                    doce_rarro_button = Button(item_frame, text=f"R${preco_atual}", bg=cor, font=("Verdana", 7), 
                           command=comprarDoceRaro, width=7)
                else:
                    doce_rarro_button = Button(item_frame, text="MAX", bg=cor, font=("Verdana", 7), 
                           state="disabled", width=7)
                doce_rarro_button.pack()
                
            elif nome == "Mega Bracelete":
                mega_bracelete_button = Button(item_frame, text="R$1000", bg=cor, font=("Verdana", 7), 
                       command=comprarMegaBracelete, width=7, state="disabled")
                mega_bracelete_button.pack()
                
            elif nome == "Coco":
                preco_inicial = 400
                coco_button = Button(item_frame, text=f"R${preco_inicial}", bg=cor, font=("Verdana", 7), 
                       command=comprarCoco, width=7)
                coco_button.pack()
                
            else:
                Button(item_frame, text=f"R${preco}", bg=cor, font=("Verdana", 7), 
                       command=comando, width=7).pack()

    criar_item("Doce Raro", 200, "lightgreen", comprarDoceRaro, 0, "imgs/Candy.png")
    criar_item("Rede", 2000, "lightgreen", comprarRede, 1, "imgs/Rede.png")
    criar_item("Coco", 400, "lightgreen", comprarCoco, 2, "imgs/coco.png")
    criar_item("Mega Bracelete", "0,99", "lightblue", comprarMegaBracelete, 3, "imgs/Mega.png")

    # ======== BOTÃO AJUDA ========
    ajuda_frame = Frame(itens_container, bg="#f8d26d", width=110, height=60)
    ajuda_frame.pack(side=LEFT, padx=12)
    ajuda_frame.pack_propagate(False)
    
    Button(ajuda_frame, text="AJUDA", bg="lightblue", font=("Verdana", 9, "bold"),
           command=mostrar_ajuda, width=8, height=1).pack(expand=True)
    
    # ======== INICIAR SISTEMAS ========
    dano_coco_periodico()
    atualizar_temporizadores()
    jogo_window.mainloop()

if __name__ == "__main__":
    criar_tela_jogo()