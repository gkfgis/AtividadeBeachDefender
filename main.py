from variaveis import inicializar_variaveis
from funcoes import criar_menu

# Inicializar a interface
root, frm = inicializar_variaveis()

# Criar o menu
criar_menu(frm, root)

# Rodar a janela
root.mainloop()