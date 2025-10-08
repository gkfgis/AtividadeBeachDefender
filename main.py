from variaveis import inicializar_variaveis
from funcoes import criar_menu

# Inicializar a interface
root, bg_photo = inicializar_variaveis()

# Criar o menu com background
criar_menu(root, bg_photo)

# Rodar a janela
root.mainloop()