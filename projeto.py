import os
import time


def menu_inicial():
    print('Escolha uma opção: \n1. Cadastro \n2. Login')
    opcao_inicial = input('Digite o respectivo número: ')
    if opcao_inicial == '1':
        cadastrar()
    elif opcao_inicial == '2':
        ()


def cadastrar():
    email = cadastro_usuario()
    senha = cadastro_senha()

    cadastro_usuario()
    cadastro_senha()
    with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{email}, {senha}')
    menu_principal()

    
def cadastro_usuario():
    os.system('clear')
    print ('Cadastro : digite o usuário (e-mail)')
    print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
    while True:
        email = input ('Usuário: ').strip()
        # Restrição de e-mails para o usuário
        if ('@ufrpe.br' in email) or ('@gmail.com' in email):
            os.system('clear')
            print('Usuário valido')
            return email

        ###elif '@gmail.com' in usuario_in:
            os.system('clear')
            print('Usuário valido')
            return usuario_in
        else:
            os.system('clear')
            print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')
            cadastro_usuario()

def cadastro_senha():
    while True:
        print('Sua senha precisa ter 8 caractéries')
        senha = input('Senha: ').strip()
        
        # Restrições da senha
        if len(senha) != 8:
            os.system('clear')
            print('senha inválida. Sua senha precisa ter 8 caractéries')
            cadastro_usuario()
        else:
            os.system('clear')
            print('LOGIN EFETIVADO')
            return senha



def menu_principal():
    print(f'Bem vindo!')
    # Exibir opções da página
    print ('1. Jogar Quizz \n2. Jogar mini-game \n3. Pontuação \n4. Configurações \n0. Sair ')
    resposta = input ('Digite o número para continuar ou sair: ')
    if resposta == '1':
        os.system('clear')
        print('Quizz')
    elif resposta == '2':
        os.system('clear')
        print('Mini-game')
    elif resposta == '3':
        os.system('clear')
        print('Pontuação')
    elif resposta == '4':
        os.system('clear')
        print('Configurações')
    else:
        os.system('clear')
        print("Encerrando Programa\nLimpando a tela em:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        os.system('clear')



def main():
    os.system('clear')
    menu_inicial()

if __name__ == '__main__':
    main()
    

