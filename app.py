import os

# Array com os logins efetivados
logins = []
def efetuar_login():
    print ('Login : digite o usuário (e-mail) e a senha')
    print ('O usuário precisa conter @gmail.com ou @ufrpe.br')
    usuario_in = input ('Usuário: ').strip()
    # Restrição de e-mails para o usuário
    if '@ufrpe.br' in usuario_in:
        print('A senha precisa ter 8 caractéries')
        senha = input ('Senha: ').strip()
    elif '@gmail.com' in usuario_in:
        senha = input ('Senha: ').strip()
    else:
        os.system('clear')
        print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')
        efetuar_login()
    # Restrições da senha
    if len(senha) != 8:
        os.system('clear')
        print('senha inválida. Sua senha precisa ter 8 caractéries')
        efetuar_login()
    else:
        os.system('clear')
        print('LOGIN EFETIVADO')
        logins.append(usuario_in)
        logins.append(senha)
        menu_principal()


def menu_principal():
    print(f'Bem vindo!')
    # Exibir opções da página
    print ('1. Jogar Quizz \n2. Jogar mini-game \n3. Pontuação \n4.Sair ')
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
    else:
        os.system('clear')
        print('Saindo...')



def main():
    os.system('clear')
    efetuar_login()

if __name__ == '__main__':
    main()
    

