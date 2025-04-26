import os
import time


def menu_inicial():
    print('Escolha uma opção: \n1. Cadastro \n2. Login')
    opcao_inicial = input('Digite o respectivo número: ')
    if opcao_inicial == '1':
        cadastrar()
    elif opcao_inicial == '2':
        efetuar_login()


def cadastrar():
    os.system('cls')
    email_cd = cadastro_usuario()
    senha_cd = cadastro_senha()

    with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{email_cd}, {senha_cd}\n')
    menu_principal()

def efetuar_login():
    os.system('cls')
    # Login de usuario:
    usuario = login_usuario()
    # Achando a linha do usuario no banco de dados
    with open('bancodedados.txt', 'r') as arquivo:
        lines = arquivo.readlines()
    for line in lines:
        if line.find(usuario) != -1:
            break            
            
    # Senha:
    while True:
        print('Login: Sua senha tem 8 caractéries')
        senha_log = input('Senha: ').strip()
        
        # Se a senha for a mesma da linha do usuario no banco de dados
        if senha_log in line and len(senha_log) == 8:
            os.system('cls')
            print('LOGIN EFETIVADO')
            menu_principal()
            return senha_log
            
        else:
            os.system('cls')
            print('Senha incorreta')

    
def cadastro_usuario():
    print ('Cadastro : digite o usuário (e-mail)')
    print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
    while True:
        email_cd = input ('Usuário: ').strip()
        # Restrição de e-mails para o usuário
        if ('@ufrpe.br' in email_cd) or ('@gmail.com' in email_cd):
            os.system('cls')
            print('Usuário valido')
            return email_cd
        else:
            os.system('cls')
            print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

def cadastro_senha():
    while True:
        print('Sua senha precisa ter 8 caractéries')
        senha_cd = input('Senha: ').strip()
        
        # Restrições da senha
        if len(senha_cd) != 8:
            os.system('cls')
            print('senha inválida. Sua senha precisa ter 8 caractéries')
        else:
            os.system('cls')
            print('LOGIN EFETIVADO')
            return senha_cd


def login_usuario():
    while True:
        print('Login: digite seu e-mail:')
        email_log = input('Usuário: ')

        with open('bancodedados.txt', 'r') as arquivo:
            txt = arquivo.read()

        if email_log in txt:
            print('Usuário valido')
            return email_log
        else:
            os.system('cls')
            print('Usuário inválido. Esse e-mail não está cadastrado')
    
        




def menu_principal():
    print(f'🇧‌ 🇪‌ 🇲‌  🇻‌ 🇮‌ 🇳‌ 🇩‌ 🇴‌  🇦‌ 🇴‌  🇧‌ 🇦‌ 🇿‌ 🇦‌ 🇷‌')
    # Exibir opções da página
    print ('1. Acessar produtos a venda  \n2. Adicionar produto \n3. Configurações \n0. Sair ')
    resposta = input ('Digite o número para continuar ou sair: ')
    if resposta == '1':
        os.system('cls')
        print('Produtos disponíveis')
    elif resposta == '2':
        os.system('cls')
        print('Adicionar produto')
    elif resposta == '3':
        os.system('cls')
        print('Configurações da conta')
    else:
        os.system('cls')
        print("Encerrando Programa\nLimpando a tela em:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        os.system('cls')


def main():
    os.system('cls')
    menu_inicial()

if __name__ == '__main__':
    main()
    

