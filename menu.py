from item import Item
import os
import time

class Menu:
    def __init__(self, usuario):
        self.usuario = usuario
    def menu_inicial(self):
        '''
            A primeira tela do programa é esse menu que contem as opções de Cadastro e Login para acessar o bazar.
            Essa função é chamada pela main() para sempre começar por aqui.
            Tem como entrada 1 e 2 que chamam o cadastro e o login respectivamente. 
            Em caso de uma entrada inválida continua até receber 1 ou 2.

        '''
        while True:
            self.limpar_terminal()
            # Exibir opções no Menu
            print('Para entrar no Bazar escolha uma opção: \n1. Cadastro \n2. Login')
            opcao_inicial = input('Digite a opção desejada: ').strip()
            if opcao_inicial == '1':
                self.menu_cadastro()
                break
            elif opcao_inicial == '2':
                self.menu_login() 
                break 
            else:
                self.limpar_terminal()
                print('Escolha 1 ou 2')

    def menu_cadastro(self):
        '''
            Similar ao menu inicial, aqui também são exibidas opções para acessar o Bazar: novo usuário ou voltar
            Recebe as entradas 1, 2 e 3 como opções de cadastrar, voltar para fazer o login e voltar ao menu inicial
            Em caso de uma entrada inválida continua até receber 1, 2 ou 3.
        '''
        while True:
            self.limpar_terminal()
            # Opções do cadastro, ir para login e voltar
            opcao_menu_cadastro = input('Login: Escolha uma opção: \n1. Novo usuário e senha \n2. Já tem conta? Volte e façe o login \n3. Voltar ao menu inicial \n').strip()
            if opcao_menu_cadastro == '1':
                self.usuario.cadastrar()
                break
            elif opcao_menu_cadastro == '2':
                self.menu_inicial()
                break
            elif opcao_menu_cadastro == '3':
                self.menu_inicial()
                break 
            else:
                print('Opção invalid    a')

    def menu_login(self):
        '''
            Nesse menu são exibidas opções para acessar o Bazar ou para voltar. 
            Recebe as entradas 1, 2 e 3 como opções de login, esqueci a senha e voltar ao menu inicial.
            Em caso de uma entrada inválida continua até receber 1, 2 ou 3.
        '''
        while True:
            self.limpar_terminal()
            # Opções do login, esqueci senha e voltar
            opcao_menu_login = input('Login: Escolha uma opção: \n1. Usuário e senha \n2. Esqueci a senha \n3. Voltar ao menu inicial \n').strip()
            if opcao_menu_login == '1':
                self.usuario.efetuar_login()
                break
            elif opcao_menu_login == '2':
                self.usuario.esqueci_senha()
                break
            elif opcao_menu_login == '3':
                self.menu_inicial()
                break 
            else:
                print('Opção inválida')

    
    def menu_principal(self, usuario):
        '''
            Este é o principal local de acesso as funcionalidades do Bazar Brejó.
            Tem 4 opções de entrada para acessar itens à venda, lançar itens, acessar configurações e sair.
            Possui tambem cores no terminal.

            Parâmetros:
                usuario (email_log): o email do login_usuario().

            Se a opção for inválida continuar até receber uma entrada válida.
        '''

        print ('','\033[34m=' * 60, f'\n \033[1;35m    ▁ ▂ ▄ ▅ ▆ ▇ █ BEM VINDO AO BAZAR BREJÓ █ ▇ ▆ ▅ ▄ ▂ ▁\033[m  \n\n      - \033[37mO Bazar/Brechó da UFRPE criado por BREno e JOão -\033[m\n','\033[34m='*60)
        print('\033[m\033[m') # Para não ir em todo comando
        # Exibir opções da página
        print ('1. Acessar itens à venda  \n2. Lançar item \n3. Configurações \nX. Sair')
        resposta_mp = input ('\nDigite a opção desejada: ').strip()
        while True:
            if resposta_mp == '1':
                self.limpar_terminal()
                print('Itens disponíveis')
                Item.comprar_itens(usuario)
                break
            elif resposta_mp == '2':
                self.limpar_terminal()
                print('Adicionar item')
                Item.lancar_item(usuario)
                break
            elif resposta_mp == '3':
                self.limpar_terminal()
                self.menu_config(usuario)
                break
            elif resposta_mp == 'x':
                # Animação da saída do terminal
                self.limpar_terminal()
                print("Encerrando Programa\nLimpando a tela em:")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                self.limpar_terminal()
                break
            else:
                print('Opção inválida')
                self.limpar_terminal()

    def menu_config(self, usuario):
        '''
            Aqui são exibidas as opções das configurações como feedback, mudar nome, mudar senha, excluir conta e voltar.

            Parâmetros:
                usuario (email_log): o email do login_usuario().

            Se a opção for inválida continuar até receber uma entrada válida.
        '''
        from sistema import menu_global

        while True:
            print('=============\nConfigurações\n=============\n')
            print('1. Feedback \n2. Mudar nome \n3. Mudar senha\n4. Exluir conta \n5. Voltar')
            resposta_mc = input('\nDigite a opção desejada: ').strip()
            if resposta_mc == '1':
                self.limpar_terminal()
                print('Feedback')
                self.usuario.feedback(usuario)
                break
            elif resposta_mc == '2':
                self.limpar_terminal()
                print('Mudar nome da conta')
                self.usuario.mudar_nome_config(usuario)
                break
            elif resposta_mc == '3':
                self.limpar_terminal()
                print('Mudar senha da conta')
                self.usuario.mudar_senha_config(usuario)
                break
            elif resposta_mc == '4':
                self.limpar_terminal()
                self.usuario.excluir_conta(usuario)
                break
            elif resposta_mc == '5':
                self.limpar_terminal()
                menu_global.menu_principal(usuario)
                break
            else:
                print('Opção inválida')
                self.limpar_terminal()
    
    @staticmethod
    def limpar_terminal():
        '''
            Aqui está a função mais usada do código.
            Ela limpa o terminal tanto em sistemas Windows quanto Mac e Linux
        '''
        # Para limpar o terminal em qualquer os
        os.system('cls' if os.name == 'nt' else 'clear')
