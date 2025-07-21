from item import Item
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
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
            width = console.size.width
            painel_width = max(40, min(80, width - 10)) # Tamanho do painel

            texto_menu = (
            '[bold cyan]Para entrar no Bazar escolha uma opção:[/bold cyan]\n\n'
            '[bold white]1 - Cadastro[/bold white]\n'
            '[bold white]2 - Login[/bold white]'
            )

            painel = Panel(texto_menu, title= '[bold white]MENU INICIAL[/bold white]', width=painel_width, border_style='purple')
            console.print(painel)

            opcao_inicial = Prompt.ask('[bold white]Digite a opção desejada[/bold white]').strip()
            if opcao_inicial == '1':
                self.menu_cadastro()
                break
            elif opcao_inicial == '2':
                self.menu_login()
                break
            else:
                console.print('[red]Escolha 1 ou 2[/red]')
                input('Pressione Enter para tentar novamente...')
    def menu_cadastro(self):
        '''
            Similar ao menu inicial, aqui também são exibidas opções para acessar o Bazar: novo usuário ou voltar
            Recebe as entradas 1, 2 e X como opções de cadastrar, voltar para fazer o login e voltar ao menu inicial
            Em caso de uma entrada inválida continua até receber 1, 2 ou X.
        '''
        while True:
            self.limpar_terminal()
            # Opções do cadastro, ir para login e voltar
            width = console.size.width
            painel_width = max(40, min(80, width - 10))

            texto_menu = (
            '[bold cyan]Para realizar o cadastro:[/bold cyan]\n\n'
            '[bold white]1 - Novo usuário[/bold white]\n'
            '[bold white]2 - Já tem conta? Faça o login[/bold white]\n'
            '[bold white]X - Voltar ao menu inicial[/bold white]'
            )

            painel = Panel(texto_menu, title="[bold white]CADASTRO[/bold white]", width=painel_width, border_style='purple')
            console.print(painel)

            opcao_menu_cadastro = Prompt.ask('[bold white]Sua escolha[/bold white]').strip().lower()
            if opcao_menu_cadastro == '1':
                self.usuario.cadastrar()
                break
            elif opcao_menu_cadastro == '2':
                self.menu_inicial()
                break
            elif opcao_menu_cadastro == 'x':
                self.menu_inicial()
                break 
            else:
                console.print('[red]Opção inválida[/red]')
                input('Pressione Enter para tentar novamente...')

    def menu_login(self):
        '''
            Nesse menu são exibidas opções para acessar o Bazar ou para voltar. 
            Recebe as entradas 1, 2 e X como opções de login, esqueci a senha e voltar ao menu inicial.
            Em caso de uma entrada inválida continua até receber 1, 2 ou X.
        '''
        while True:
            self.limpar_terminal()
            # Opções do login, esqueci senha e voltar
            width = console.size.width
            painel_width = max(40, min(80, width - 10))

            texto_menu = (
            '[bold cyan]Para realizar o login:[/bold cyan]\n\n'
            '[bold white]1 - Usuário e senha[/bold white]\n'
            '[bold white]2 - Esqueci a senha[/bold white]\n'
            '[bold white]X - Voltar ao menu inicial[/bold white]'
            )

            painel = Panel(texto_menu, title="[bold white]LOGIN[/bold white]", width=painel_width, border_style='purple')
            console.print(painel)
            opcao_menu_login = Prompt.ask('[bold white]Sua escolha[/bold white]').strip().lower()
            if opcao_menu_login == '1':
                self.usuario.efetuar_login()
                break
            elif opcao_menu_login == '2':
                self.usuario.esqueci_senha()
                break
            elif opcao_menu_login == 'x':
                self.menu_inicial()
                break 
            else:
                console.print('[red]Opção inválida[/red]')
                input('Pressione Enter para tentar novamente...')

    
    def menu_principal(self, usuario):
        '''
            Este é o principal local de acesso as funcionalidades do Bazar Brejó.
            Tem 4 opções de entrada para acessar itens à venda, lançar itens, acessar configurações e sair.
            Possui tambem cores no terminal.

            Parâmetros:
                usuario (email_log): o email do login_usuario().

            Se a opção for inválida continuar até receber uma entrada válida.
        '''

        # Exibir opções da página
       
        while True:
            self.limpar_terminal()
            width = console.size.width
            painel_width = max(50, min(80, width - 10)) 

            titulo = '[bold magenta]BAZAR BREJÓ[/bold magenta]'   
            texto = (
                '[bold cyan]BEM-VINDO AO BAZAR BREJÓ[/bold cyan]\n\n'
                '[bold white]1 - Acessar itens à venda[/bold white]\n'
                '[bold white]2 - Lançar item[/bold white]\n'
                '[bold white]3 - Configurações[/bold white]\n'
                '[bold white]X - Sair[/bold white]'
            )
            painel = Panel(texto, title = titulo, width = painel_width, border_style='purple')
            console.print(painel)
            resposta_mp = Prompt.ask('[bold white]Digite a opção desejada: [/bold white]')
            if resposta_mp == '1':
                self.limpar_terminal()
                console.print('[bold green]Itens disponíveis[/bold green]')
                Item.comprar_itens(usuario)
                break
            elif resposta_mp == '2':
                self.limpar_terminal()
                console.print('[green]Adicionar item[/green]')
                Item.lancar_item(usuario)
                break
            elif resposta_mp == '3':
                self.limpar_terminal()
                self.menu_config(usuario)
                break
            elif resposta_mp == 'x':
                # Animação da saída do terminal
                self.limpar_terminal()
                print('Encerrando Programa\nLimpando a tela em:')
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                self.limpar_terminal()
                break
            else:
                console.print('[red]Opção inválida[/red]')
                input('Pressione Enter para tentar novamente...')
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
            self.limpar_terminal()
            width = console.size.width
            painel_width = max(50, min(80, width - 10))

            titulo = '[bold white]CONFIGURAÇÕES[/bold white]'
            texto = (
                '[bold white]1 - Feedback[/bold white]\n'
                '[bold white]2 - Mudar nome[/bold white]\n'
                '[bold white]3 - Mudar senha[/bold white]\n'
                '[bold white]4 - Excluir conta[/bold white]\n'
                '[bold white]5 - Ver extrato[/bold white]\n'
                '[bold white]X - Voltar[/bold white]'
            )
            painel = Panel(texto, title = titulo, width = painel_width, border_style='purple')
            console.print(painel)
            resposta_mc = Prompt.ask('[bold white]Digite a opção desejada: [/bold white]').strip().lower()

            if resposta_mc == '1':
                self.limpar_terminal()
                console.print('[bold green]Feedback[/bold green]')
                self.usuario.feedback(usuario)
                break
            elif resposta_mc == '2':
                self.limpar_terminal()
                console.print('[bold green]Mudar nome da conta[/bold green]')
                self.usuario.mudar_nome_config(usuario)
                break
            elif resposta_mc == '3':
                self.limpar_terminal()
                console.print('[bold green]Mudar senha da conta[/bold green]')
                self.usuario.mudar_senha_config(usuario)
                break
            elif resposta_mc == '4':
                self.limpar_terminal()
                self.usuario.excluir_conta(usuario)
                break
            elif resposta_mc == '5':
                self.limpar_terminal()
                self.usuario.mostrar_extrato(usuario)
            elif resposta_mc == 'x':
                self.limpar_terminal()
                menu_global.menu_principal(usuario)
                break
            else:
                console.print('[red]Opção inválida[/red]')
                input('Pressione Enter para tentar novament...')
                self.limpar_terminal()
    
    @staticmethod
    def limpar_terminal():
        '''
            Aqui está a função mais usada do código.
            Ela limpa o terminal tanto em sistemas Windows quanto Mac e Linux
        '''
        # Para limpar o terminal em qualquer os
        os.system('cls' if os.name == 'nt' else 'clear')
