import os
import time


def menu_inicial():
    print('Para entrar no Bazar escolha uma opção: \n1. Cadastro \n2. Login')
    opcao_inicial = input('Digite o respectivo número: ')
    if opcao_inicial == '1':
        cadastrar()
    elif opcao_inicial == '2':
        efetuar_login()

def cadastrar():
    os.system('cls')
    # Cadastro do usuario
    email_cd = cadastro_usuario()
    # Cadastro da senha
    senha_cd = cadastro_senha()
    # Escrever todos os cadastros no bancodedados.txt
    with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{email_cd}, {senha_cd}\n')
    # Abrir Menu Principal após cadastro
    efetuar_login()

def efetuar_login():
    os.system('cls')
    # Login de usuario:
    usuario = login_usuario()
    # Login do senha:
    # lendo linhas do banco de dados (arquivo .txt)
    with open('bancodedados.txt', 'r') as arquivo:
        lines = arquivo.readlines()
    # Iterando pelas linhas do txt
    for line in lines:
        # Parar quando encontrar a linha do usuario no arquivo
        if usuario in line:
            break            
            
    # Login da senha:
    while True:
        print('Login: Sua senha tem 8 caracteres')
        senha_log = input('Senha: ').strip()

        # Se a senha for a mesma da linha do usuario no banco de dados
        if line.endswith(f'{senha_log}\n'):
            os.system('cls')
            menu_principal()
            return senha_log
            
        else:
            os.system('cls')
            print('Senha incorreta')

def cadastro_usuario():
    print ('Cadastro : digite o usuário (e-mail)')
    print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
    while True:
        email_cd = input ('Usuário: ').strip().lower()
        email_arroba = email_cd.split('@')
        # Restrição de e-mails para o usuário: @ e terminar com entradas válidas
        if len(email_arroba) == 2 and (email_cd.endswith('@ufrpe.br') or email_cd.endswith('@gmail.com')):
            os.system('cls')
            print('Usuário válido')
            with open('bancodedados.txt', 'r') as arquivo:
                usuarios = arquivo.read()
            if email_cd in usuarios:
                os.system('cls')
                print('Usuário já cadastrado')
            else:
                os.system('cls')
                return email_cd
        else:
            os.system('cls')
            print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

def cadastro_senha():
    while True:
        print('Sua senha precisa ter 8 caracteres')
        senha_cd = input('Senha: ').strip()
        
        # Restrição do tamanho da senha
        if len(senha_cd) != 8:
            os.system('cls')
            print('senha inválida.')
        # Confirmação da senha
        else:
            senha_2 = input ('Confirme a senha: ').strip()
            if senha_cd == senha_2:
                os.system('cls')
                print('Senha cadastrada!') 
                return senha_cd
            else:
                os.system('cls') 
                print('As senhas precisam ser idênticas.')
                
def login_usuario():
    while True:
        print('Login: digite seu e-mail:')
        email_log = input('Usuário: ')

        # Checar se o usuário está presente no arquivo
        with open('bancodedados.txt', 'r') as arquivo:
            txt = arquivo.read()
        if email_log in txt:
            print('Usuário valido')
            return email_log
        else:
            os.system('cls')
            print('Usuário inválido ou esse e-mail não está cadastrado')
    
def menu_principal():
    print(f'🇧‌ 🇪‌ 🇲‌   🇻‌ 🇮‌ 🇳‌ 🇩‌ 🇴‌   🇦‌ 🇴‌   🇧‌ 🇦‌ 🇿‌ 🇦‌ 🇷‌ 🇺‌ 🇷‌ 🇦‌ 🇱‌‌')
    # Exibir opções da página
    print ('\n1. Acessar itens à venda  \n2. Lançar item \n3. Configurações \nX. Sair')
    resposta = input ('\nDigite o número da opção desejada: ')
    if resposta == '1':
        os.system('cls')
        print('Itens disponíveis')
        comprar_itens()
    elif resposta == '2':
        os.system('cls')
        print('Adicionar item')
        lancar_itens()
    elif resposta == '3':
        os.system('cls')
        print('Configurações da conta')
    else:
        # Animação da saída do terminal
        os.system('cls')
        print("Encerrando Programa\nLimpando a tela em:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        os.system('cls')

def comprar_itens():
    with open('listadeitens.txt', 'r') as arquivo:
        lista_completa = arquivo.read()
    print(f'{lista_completa}')

def lancar_itens():
    novo_item = input('Novo item: ')
    descricao_novo_item = input('Descrição do item: ')
    estado_novo_item = input('De 1 a 5 qual o estado do material? ')
    preco_novo_item = input('Preço: R$')
    with open('listadeitens.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'{novo_item}, {descricao_novo_item}, Estado (1 a 5): {estado_novo_item}, R${preco_novo_item} \n\n')
    print(f'Item adicionado: {novo_item}')

def main():
    os.system('cls')
    menu_inicial()

if __name__ == '__main__':
    main()  
