from menu import Menu
from usuario import Usuario
usuario = Usuario()
menu_global = Menu(usuario)
def main(): # Sempre começar pelo Menu Incial
    '''
        Essa função é por onde o código inicia e chama o menu_inicial() para iniciar o programa.
    '''

    Menu.LimparTerminal()
    global menu_global
    menu_global.MenuInicial()

if __name__ == '__main__':
    main()  
