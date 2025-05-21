import os
import time
import sys
import random # Import que possibilita números randomicos
import smtplib # Import para fazer login no meu email
from email.message import EmailMessage # Função python para mensagem de email


def input_senha(prompt = 'Senha: '): # Senha com asteriscos
    try:
        print(prompt, end = '', flush = True)
        senha = ''
        # Se o sistema for windows
        if os.name == 'nt':
            import msvcrt
            while True:
                # Captura teclas pressionadas na senha antes do enter
                char = msvcrt.getch()
                # Tecla enter
                if char in {b'\r', b'\n'}:
                    print()
                    break
                # Tecla backspace
                elif char == b'\x08':
                    if senha:
                        senha = senha[:-1]
                        print('\b \b', end = '', flush = True)
                else:
                    try:
                        # Faz a criptografia da senha com ********
                        senha += char.decode('utf-8')
                        print('*', end = '', flush = True)
                    except UnicodeDecodeError:
                        pass
        else:            
            import termios # Sistema Linux
            import tty # Sistema MacOS
            fd  = sys.stdin.fileno() # Possibilita a criptografia da entrada com as bibliotecas Linus e Mac
            old_settings = termios.tcgetattr(fd) # Salva as configurações do terminal antes da modificação
            try:
                tty.setraw(fd) # Captura teclas e armazena antes do enter
                while True:
                    char = sys.stdin.read(1)
                    # Tecla enter
                    if char in ('\n', '\r'):
                        print()
                        break
                    # Tecla backspace
                    elif char == '\x7f':
                        if senha:
                            senha = senha[:-1]
                            print('\b \b', end = '', flush = True)
                    else:
                        # Faz a criptografia da senha com ********
                        senha += char
                        print('*', end = '', flush = True)
            finally: # Restora as configurações do terminal para voltar ao padrão
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return senha
    except Exception: # Se o terminal não suportar a entrada
        print("\n  Falha ao esconder a senha. Digite normalmente.")
        return input(prompt)

def menu_inicial():
    while True:
        limpar_terminal()
        # Exibir opções no Menu
        print('Para entrar no Bazar escolha uma opção: \n1. Cadastro \n2. Login')
        opcao_inicial = input('Digite o respectivo número: ').strip()
        if opcao_inicial == '1':
            menu_cadastro()
            break
        elif opcao_inicial == '2':
            menu_login() 
            break 
        else:
            limpar_terminal()
            print('Escolha 1 ou 2')
        
def menu_cadastro():
    while True:
        limpar_terminal()
        # Opções do cadastro, ir para login e voltar
        opcao_menu_cadastro = input('Login: Escolha uma opção: \n1. Novo usuário e senha \n2. Já tem conta? Volte e façe o login \n3. Voltar ao menu inicial \n').strip()
        if opcao_menu_cadastro == '1':
            cadastrar()
            break
        elif opcao_menu_cadastro == '2':
            menu_inicial()
            break
        elif opcao_menu_cadastro == '3':
            menu_inicial()
            break 
        else:
            print('Opção invalida')

def menu_login():
    while True:
        limpar_terminal()
        # Opções do login, esqueci senha e voltar
        opcao_menu_login = input('Login: Escolha uma opção: \n1. Usuário e senha \n2. Esqueci a senha \n3. Voltar ao menu inicial \n').strip()
        if opcao_menu_login == '1':
            efetuar_login()
            break
        elif opcao_menu_login == '2':
            esqueci_senha()
            break
        elif opcao_menu_login == '3':
            menu_inicial()
            break 
        else:
            print('Opção inválida')

def cadastrar():
    limpar_terminal()
    nome_cd = cadastro_nome()
    # Cadastro do usuário
    email_cd = cadastro_usuario()
    # Cadastro da senha
    senha_cd = cadastro_senha()
    # Escrever todos os cadastros no bancodedados.txt
    with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{nome_cd},{email_cd},{senha_cd}\n').strip()
    # Abrir Menu Principal após cadastro
    efetuar_login(opcao_menu_login=None)

def efetuar_login(opcao_menu_login=None):
    limpar_terminal() 
    # Login de usuário:
    usuario = login_usuario()
    # Login da senha:
    # lendo linhas do banco de dados como {email: senha} (arquivo .txt)
    with open('bancodedados.txt', 'r') as arquivo:
        usuarios = {}
        for line in arquivo:
            partes = line.strip().split(',') 
            if len(partes) != -1:   # Separa email da senha
                email = partes[1].strip()
                senha = partes[2].strip()
                usuarios[email] = senha

    if usuario not in usuarios: # Se usuário não tiver no banco de dados
        limpar_terminal()
        print('Usuário não encontrado.')
        return                    
            
    # Login da senha:
    while True: 
        print('Login: Sua senha tem 8 caracteres')
        senha_log = input_senha('Senha: ').strip() # Chamar criptografia

        # Se a senha for a mesma da linha do usuário no banco de dados
        if senha_log == usuarios[usuario]:
            limpar_terminal()
            menu_principal(usuario)
            return senha_log and usuario
            
        else:
            limpar_terminal()
            print('Senha incorreta')

def cadastro_nome():
    print('Digite seu nome')
    while True:
        nome_cd = input('Nome: ').strip()
        # Checar se nome já é cadastrado
        with open('bancodedados.txt', 'r') as arquivo:
            usuarios = arquivo.read()
        if nome_cd in usuarios:
            print('Esse nome já foi usado')
        else:
            limpar_terminal()
            return nome_cd

def cadastro_usuario():
    print ('Cadastro : digite o usuário (e-mail)')
    print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
    while True:
        email_cd = input ('Usuário: ').strip().lower()
        email_arroba = email_cd.split('@')
        # Restrição de e-mails para o usuário: @ e terminar com entradas válidas
        if len(email_arroba) == 2 and (email_cd.endswith('@ufrpe.br') or email_cd.endswith('@gmail.com')):
            limpar_terminal()
            print('Usuário válido')
            # Checar se usuário já é cadastrado
            with open('bancodedados.txt', 'r') as arquivo:
                usuarios = arquivo.read()
            if email_cd in usuarios:
                limpar_terminal()
                print('Usuário já cadastrado, Insira outro e-mail!')
            else:
                limpar_terminal()
                return email_cd
        else:
            limpar_terminal()
            print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

def cadastro_senha():
    while True:
        print('Sua senha precisa ter 8 caracteres')
        senha_cd = input_senha('Senha: ').strip()
        
        # Restrição do tamanho da senha
        if len(senha_cd) != 8:
            limpar_terminal()
            print('senha inválida.')
        # Confirmação da senha
        else:
            senha_2 = input_senha('Confirme a senha: ').strip()
            if senha_cd == senha_2:
                limpar_terminal()
                print('Senha cadastrada!') 
                return senha_cd
            else:
                limpar_terminal()
                print('As senhas precisam ser idênticas.')

def login_usuario():
    while True:
        print('Login: digite seu e-mail:')
        email_log = input('Usuário: ').strip()

        # Checar se o usuário está presente no arquivo
        with open('bancodedados.txt', 'r') as arquivo:
            txt = arquivo.read()
        if email_log in txt:
            print('Usuário valido')
            return email_log
        else:
            limpar_terminal()
            print('Usuário inválido ou esse e-mail não está cadastrado')
    
def esqueci_senha():
    while True:
        print('Login: digite seu e-mail para recuperar senha:')
        email_log = input('Usuário: ').strip()

        # Checar se o usuário está presente no arquivo
        with open('bancodedados.txt', 'r') as arquivo:
            txt = arquivo.read()
        if email_log in txt:
            print('Usuário valido')
            codigo =  random.randint(100000,999999) 
            enviar_email(email_log,codigo)
            while True:
                codigo_input = input('digite o código enviado ao seu email: ').strip()
                if codigo_input == str(codigo):
                    print('Código correto. Agora crie uma senha nova')
                    mudar_senha_esqueci(email_log)
                    return codigo_input and email_log
                
        else:
            limpar_terminal()
            print('Usuário inválido ou esse e-mail não está cadastrado')


def enviar_email(destinatario, codigo):
    email_remetente = "brenojaccioly@gmail.com" # Meu email
    senha_app = "hdygauzqbboamert" # Minha senha de app para entrar na conta
    # Conteúdo do email
    msg = EmailMessage()
    msg["Subject"] = "Seu código de verificação"
    msg["From"] = email_remetente
    msg["To"] = destinatario
    msg.set_content(f"Olá! Seu código de verificação é: {codigo}")

    try: # Enviar email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
        print("Código de verificação enviado para o seu email!")
    except Exception as e:
        print("Erro ao enviar email, verifique se o email de fato existe:", e)
        menu_login()

def mudar_senha_esqueci(destinatario):
    limpar_terminal()
    print('Código correto')
    senha_nova = input('Nova senha: ').strip()

    # Lê todas as linhas do arquivo
    with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    nova_lista = []

    # Verifica se foi possível atualizar
    senha_trocada = False

    for linha in linhas:
        partes = linha.strip().split(',')
        if len(partes) == 3:
            nome = partes[0].strip()
            email = partes[1].strip()
            senha = partes[2].strip()
            if email == destinatario:
                nova_linha = f'{nome},{email},{senha_nova}\n'.strip() 
                nova_lista.append(nova_linha)
                senha_trocada = True
            else:
                nova_lista.append(linha)
        else:
            nova_lista.append(linha)

    # Só reescreve o arquivo após o loop completo
    with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(nova_lista)

    if senha_trocada:
        print('Senha atualizada com sucesso!')
        menu_principal()

    else:
        print('Erro: e-mail não encontrado.')


def limpar_terminal():
    # Para limpar o terminal em qualquer os
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal(usuario):
    print ('\033[34m=' * 60, f'\n \033[1;35m   ▁ ▂ ▄ ▅ ▆ ▇ █ BEM VINDO AO BAZAR BREJÓ █ ▇ ▆ ▅ ▄ ▂ ▁\033[m  \n\n    - \033[37mO Bazar/Brechó da UFRPE criado por BREno e JOão -\033[m\n','\033[34m=' * 60)
    # Exibir opções da página
    print ('\n1. Acessar itens à venda  \n2. Lançar item \n3. Configurações \nX. Sair')
    resposta_mp = input ('\nDigite a opção desejada: ').strip()

    if resposta_mp == '1':
        limpar_terminal()
        print('Itens disponíveis')
        comprar_itens()
    elif resposta_mp == '2':
        limpar_terminal()
        print('Adicionar item')
        lancar_itens()
    elif resposta_mp == '3':
        limpar_terminal()
        menu_config(usuario)
    elif resposta_mp == 'x':
        # Animação da saída do terminal
        limpar_terminal()
        print("Encerrando Programa\nLimpando a tela em:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        limpar_terminal()
    else:
        print('Opção inválida')
        limpar_terminal()
        menu_principal()

def comprar_itens():
    # Exibir opções de compra
    with open('listadeitens.txt', 'r') as arquivo:
        lista_completa = arquivo.read()
    print(f'{lista_completa}')

def lancar_itens():
    # Capturar detalhes do novo item e armazenar na lista
    novo_item = input('Novo item: ').strip()
    descricao_novo_item = input('Descrição do item: ').strip()
    estado_novo_item = input('De 1 a 5 qual o estado do material? ').strip()
    preco_novo_item = input('Preço: R$').strip()
    # Escrever descrições no txt dos itens
    with open('listadeitens.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{novo_item},{descricao_novo_item},Estado (1 a 5): {estado_novo_item},R${preco_novo_item} \n\n')
    print(f'Item adicionado: {novo_item}')

def menu_config(usuario):
    print('=============\nConfigurações\n=============\n')
    print('1. Feedback \n2. Mudar nome \n3. Mudar senha\n4. Exluir conta \n5. Voltar')
    resposta_mc = input('\nDigite a opção desejada: ').strip()
    if resposta_mc == '1':
        limpar_terminal()
        print('Feedback')
    elif resposta_mc == '2':
        limpar_terminal()
        print('Mudar nome da conta')
    elif resposta_mc == '3':
        limpar_terminal()
        print('Mudar senha da conta')
    elif resposta_mc == '4':
        limpar_terminal()
        excluir_conta(usuario)
    elif resposta_mc == '5':
        limpar_terminal()
        menu_principal()
    else:
        print('Opção inválida')
        limpar_terminal()
        menu_config()

def excluir_conta(usuario):
    print('Você realmente deseja excluir sua conta? \n1. Sim \n2. Não, voltar')
    resposta_ec = input('Digite a opção desejada: ')
    conta_excluida = False

    if resposta_ec == '1':
    # Lê todas as linhas do arquivo
        email_excluir = str(usuario)
        print(email_excluir)
        with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        nova_lista2 = [linha for linha in linhas if linha.strip().split(',')[1] != email_excluir]
        if len(nova_lista2) == len(linhas):
            print('Usuário não encontrado')
        else:
            conta_excluida = True
            with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
                arquivo.writelines(nova_lista2)
            print("Excluindo conta\nLimpando a tela em:")
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
                limpar_terminal()
           
    if conta_excluida:
        print('Conta exluída com sucesso!')
    else:
        print('Erro ao encontrar email')  

    if resposta_ec == '2':
        limpar_terminal()
        menu_config()

def main(): # Sempre começar pelo Menu Incial
    limpar_terminal()
    menu_inicial()

if __name__ == '__main__':
    main()  
