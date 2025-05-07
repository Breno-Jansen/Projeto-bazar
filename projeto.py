import os
import time
import sys
import random
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
            import tty # Sistema macOS
            fd  = sys.stdin.fileno() # 
            old_settings = termios.tcgetattr(fd)
            try:
                # Captura teclas e armazena antes do enter
                tty.setraw(fd)
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
        # Exibir opções no Menu
        print('Para entrar no Bazar escolha uma opção: \n1. Cadastro \n2. Login')
        opcao_inicial = input('Digite o respectivo número: ').strip()
        if opcao_inicial == '1':
            cadastrar()
            break
        elif opcao_inicial == '2':
            efetuar_login() 
            break 
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Escolha 1 ou 2')
        
def menu_login():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        opcao_menu_login = input('Escolha uma opção: \n1.Usuario e senha \n2. Esqueci a senha \n3. Voltar ao menu inicial \n').strip()
        if opcao_menu_login == '1':
            login_usuario()
            break
        elif opcao_menu_login == '2':
            esqueci_senha()
            break
        elif opcao_menu_login == '3':
            opcao_menu_login = False
            break 
        else:
            print('Opção invalida')

def cadastrar():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Cadastro do usuario
    email_cd = cadastro_usuario()
    # Cadastro da senha
    senha_cd = cadastro_senha()
    # Escrever todos os cadastros no bancodedados.txt
    with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{email_cd}, {senha_cd}\n')
    # Abrir Menu Principal após cadastro
    efetuar_login(opcao_menu_login=None)

def efetuar_login(opcao_menu_login=None):
    os.system('cls' if os.name == 'nt' else 'clear') # Para limpar qualquer os
    # Login de usuario:
    usuario = menu_login()
    # Login do senha:
    # lendo linhas do banco de dados como {email: senha} (arquivo .txt)
    with open('bancodedados.txt', 'r') as arquivo:
        usuarios = {}
        for line in arquivo:
            partes = line.strip().split(',') 
            if len(partes) == 2:   # Separa email da senha
                email = partes[0].strip()
                senha = partes[1].strip()
                usuarios[email] = senha

    if usuario not in usuarios: # Se usuario não tiver no banco de dados
        print('Usuário não encontrado.')
        os.system('cls' if os.name == 'nt' else 'clear')
        return                    
            
    # Login da senha:
    while True: 
        if opcao_menu_login == False:
            break

        print('Login: Sua senha tem 8 caracteres')
        senha_log = input_senha('Senha: ').strip() # Chamar criptografia

        # Se a senha for a mesma da linha do usuario no banco de dados
        if senha_log == usuarios[usuario]:
            os.system('cls' if os.name == 'nt' else 'clear')
            menu_principal()
            return senha_log
            
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Senha incorreta')

def cadastro_usuario():
    print ('Cadastro : digite o usuário (e-mail)')
    print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
    while True:
        email_cd = input ('Usuário: ').strip().lower()
        email_arroba = email_cd.split('@')
        # Restrição de e-mails para o usuário: @ e terminar com entradas válidas
        if len(email_arroba) == 2 and (email_cd.endswith('@ufrpe.br') or email_cd.endswith('@gmail.com')):
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Usuário válido')
            with open('bancodedados.txt', 'r') as arquivo:
                usuarios = arquivo.read()
            if email_cd in usuarios:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Usuário já cadastrado')
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                return email_cd
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

def cadastro_senha():
    while True:
        print('Sua senha precisa ter 8 caracteres')
        senha_cd = input_senha('Senha: ').strip()
        
        # Restrição do tamanho da senha
        if len(senha_cd) != 8:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('senha inválida.')
        # Confirmação da senha
        else:
            senha_2 = input_senha('Confirme a senha: ').strip()
            if senha_cd == senha_2:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Senha cadastrada!') 
                return senha_cd
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
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
            os.system('cls' if os.name == 'nt' else 'clear')
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
                codigo_input = input('digite o código enviado ao seu email: ')
                if codigo_input == str(codigo):
                    print('Código correto. Agora crie uma senha nova')
                    mudar_senha(email_log)
                    return codigo_input and email_log
                
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Usuário inválido ou esse e-mail não está cadastrado')

def enviar_email(destinatario, codigo):
    email_remetente = "brenojaccioly@gmail.com" # Meu email
    senha_app = "hdygauzqbboamert" # Minha senha de app
    # Coneúdo do email
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
        print("Erro ao enviar email:", e)

def mudar_senha(destinatario):
    with open('bancodedados.txt', 'r') as arquivo:
        for line in arquivo:
            partes = line.strip().split(',') 
            if len(partes) == 2:   # Separa email da senha
                email = partes[0].strip()
                senha = partes[1].strip()
                if email == str(destinatario):
                    input('Nova senha: ')

def menu_principal():
    print(f'🇧‌ 🇪‌ 🇲‌   🇻‌ 🇮‌ 🇳‌ 🇩‌ 🇴‌   🇦‌ 🇴‌   🇧‌ 🇦‌ 🇿‌ 🇦‌ 🇷‌ 🇺‌ 🇷‌ 🇦‌ 🇱‌‌')
    # Exibir opções da página
    print ('\n1. Acessar itens à venda  \n2. Lançar item \n3. Configurações \nX. Sair')
    resposta = input ('\nDigite o número da opção desejada: ').strip()
    if resposta == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Itens disponíveis')
        comprar_itens()
    elif resposta == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Adicionar item')
        lancar_itens()
    elif resposta == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Configurações da conta')
    else:
        # Animação da saída do terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Encerrando Programa\nLimpando a tela em:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

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
    with open('listadeitens.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{novo_item}, {descricao_novo_item}, Estado (1 a 5): {estado_novo_item}, R${preco_novo_item} \n\n')
    print(f'Item adicionado: {novo_item}')

def main(): # Sempre começar pelo Menu Incial
    os.system('cls' if os.name == 'nt' else 'clear')
    menu_inicial()

if __name__ == '__main__':
    main()  
