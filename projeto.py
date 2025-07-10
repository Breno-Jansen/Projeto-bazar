import os # Possibilita a entrada no sistema do terminal (e também para limpá-lo)
import time # Import para permitir uso do tempo no terminal
import sys # Verificar sistema atual
import random # Import que possibilita números randomicos
import smtplib # Import para fazer login no meu email
from email.mime.multipart import MIMEMultipart # Função para criar uma mensagem de e-mail que pode conter texto ou anexos
from email.mime.text import MIMEText # Função para criar o conteúdo de texto que será colocado no e-mail

menu_global = None


def input_senha(prompt = 'Senha: '): # Senha com asteriscos
    
    '''
        Faz a criptografia da senha no terminal, tanto para o sistema windows quanto para Mac e Linux.

        Parâmetros:
            prompt (input) = 'Senha: ': Quando essa fução é chamada, gera um input que esconde a senha escrita.

        Armazena as teclas digitadas e retorna com '********' no terminal.
        Tenta fazer a criptografia e em caso de erro retorna o input.
    '''
    while True:
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
                sistema  = sys.stdin.fileno() # Possibilita a criptografia da entrada com as bibliotecas Linus e Mac
                config_antiga = termios.tcgetattr(sistema) # Salva as configurações do terminal antes da modificação
                try:
                    tty.setraw(sistema) # Captura teclas e armazena antes do enter
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
                    termios.tcsetattr(sistema, termios.TCSADRAIN, config_antiga)
                    

        # Validação da senha            
            if len(senha) != 8:
                Sistema.limpar_terminal()
                print('Senha inválida. Ela deve ter exatamente 8 caracteres')
                continue
            else:
                return senha
            
        except Exception: # Se o terminal não suportar a entrada
            print("\n  Falha ao esconder a senha. Digite normalmente.")
            return input(prompt)



def enviar_email(destinatario1, destinatario2, destinatario3, assunto, conteudo):
    '''
        Aqui o programa envia uma mensagem com o código aleatório para o usuário
        O código  é enviado pelo email brenojaccioly@gmail.com (um dos criadores do Bazar) com a senha_app do google.

        Parâmetros:
            usuario (email_log): o email do login do esqueci a senha.
            codigo (codigo): codigo de 6 dígitos aleatório.
        
        Tenta enviar código pela internet, se não conseguir, exibe mensagem de erro e volta ao menu_login().
    '''
    email_remetente = "brenojaccioly@gmail.com" # Meu email
    senha_app = "hdygauzqbboamert" 
    # Conteúdo do email
    msg = MIMEMultipart()
    msg["Subject"] = f"{assunto}"
    msg["From"] = email_remetente
    if destinatario2 == None and destinatario3 == None:
        msg['To'] = f'{destinatario1}'
    elif destinatario3 == None:
        msg["To"] = f'{destinatario1}, {destinatario2}'     # Definindo a quantidade de destinatários
    else:
        msg["To"] = f'{destinatario1}, {destinatario2}, {destinatario3}'
    msg.attach(MIMEText(conteudo, 'plain'))
    
    try: # Enviar email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar email, verifique acesso à internet ou se o email de fato existe:", e)
        Menu.menu_login()

def mudar_senha_esqueci(usuario):
    '''
        Essa função é iniciada após a confirmação do código, então ela recebe como entrada a nova senha
        Ocorre a leitura do bancodedados.txt para separar a senha do usuário e trocá-la pela senha_nova.
        
        Parâmetros:
            usuario(email_log): o email do login do esqueci a senha.

        Se a senha não for trocada exibe mensagem de erro e volta para menu inicial.
    '''
    Sistema.limpar_terminal()
    print('Código correto')
    senha_nova = input_senha('Nova senha: ').strip()

    # Lê todas as linhas do arquivo
    with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Cria uma lista para armazenar as novas linhas do banco de dados
    nova_lista = []
    # Verifica se foi possível atualizar
    senha_trocada = False

    for linha in linhas:
        partes = linha.strip().split(',')
        if len(partes) == 3:
            nome = partes[0].strip()
            email = partes[1].strip()
            senha = partes[2].strip()
            if email == usuario:
                nova_linha = f'{nome},{email},{senha_nova}\n' 
                nova_lista.append(nova_linha)
                senha_trocada = True # Confirma alteração
            else:
                nova_lista.append(linha)
        else:
            nova_lista.append(linha)

    if senha_trocada:
        # Só reescreve o arquivo após o loop completo
        with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(nova_lista)
        print('Senha atualizada com sucesso!')
        menu_global.menu_principal(usuario)

    else:
        print('Erro: e-mail não encontrado.')
        Menu.menu_inicial()



def comprar_itens(usuario):
    '''
        Mostra outro arquivo txt chamado listadeitens.txt que contém a lista de todos os itens à venda
        Melhorias em breve...
    '''
    with open('listadeitens.txt', 'r', encoding= 'utf-8') as txt:
        linhas = txt.readlines() # Lendo as linhas da listadeitens.txt
    separador = '|'
    todas_as_numeracoes = []
    todos_os_itens = []
    todos_os_precos = []     # Criando o armazenamento dos dados em setores
    todos_estados = []
    todas_descricoes = []
    for linha in linhas:
        separa_numero = linha.split('.')
        setor = linha.split('|')     # Organizando cada linha por setor
        if len(setor) == 5:      # Só lê as linhas que tem 5 setores
            numero = separa_numero[1]
            nome_e_numero = setor[0]
            preco = setor[1]          # Numera cada setor
            estado = setor[2]
            descricao = setor[3]
            todas_as_numeracoes.append(numero)
            todos_os_itens.append(nome_e_numero)
            todos_os_precos.append(preco)        # Insere os elementos numa array por setor
            todos_estados.append(estado)
            todas_descricoes.append(descricao)
    
    for i in range(len(todos_os_itens)):    # Printa todos os itens e seus respectivos preços
        print(f' {str(todos_os_itens[i]).ljust(35)} {separador.ljust(2)}{todos_os_precos[i]}')
    print(' .X. Voltar para o menu principal')

        
    while True: # Possibilita a escolha de um item
        escolha_item = input('Escolha um produto (numeração dele) ou clique X para voltar: ')
        if escolha_item == 'x':
            menu_global.menu_principal(usuario)           # Opção para sair
            break
        elif escolha_item not in todas_as_numeracoes:
            print('Opção inválida')    # Se a opção for inválida não dá o break
        else:
            Sistema.limpar_terminal()
            while True: # Detalhes e opções de compra ou troca
                print(f'Item {todos_os_itens[int(escolha_item)-1]}')
                print('Mais informações:')
                print(f'{todas_descricoes[int(escolha_item)-1]}, {todos_estados[int(escolha_item)-1]}, {todos_os_precos[int(escolha_item)-1]}')            
                opcao_item = input('O que você deseja fazer com o item? \n1. Comprar \n2. Negociar com o vendedor \n3. Voltar \nOpção: ')
                if opcao_item == '1':
                    Sistema.limpar_terminal()
                    while True: # Opção de compra apresenta pix e informa sobre email a ser enviado
                        print(f'Para comprar o item {todos_os_itens[int(escolha_item)-1]}faça o pix de {todos_os_precos[int(escolha_item)-1]}para o pix: 704.514.384-26')
                        print('Com a confirmação um email será enviado aos vendedores e com o pagamento você poderá buscar o item :)')
                        confirmar_compra = input(' Para confirmar digite 1, \n para cancelar digite 2:')
                        if confirmar_compra == '1':
                            print('Email enviado! Venha para o Ceagri II para pegar seu item.')
                            break
                        elif confirmar_compra == '2':
                            Sistema.limpar_terminal()
                            print('Voltando...')
                            comprar_itens()
                            break
                        else:
                            Sistema.limpar_terminal()
                            print('Opção inválida')
                    break
                elif opcao_item == '2': # Para solicitar uma troca envia email para vendedores
                    negociar(usuario)
                    break # Em desenvolvimento

                elif opcao_item == '3':
                    Sistema.limpar_terminal()
                    comprar_itens(usuario)
                    break
                
                else:
                    Sistema.limpar_terminal()
                    print('Opção inválida')
            break

def negociar(usuario):
    print('Para negociar com o cliente você pode conversar com ele por email ou ver o número de telefone dele.')
    print('1. Escrever email aqui para o vendedor.\n2. Ver o contato do vendedor. \n3. Voltar')
    assunto = 'Um cliente do Bazar Brejó quer negociar com você!'
    while True:
        opcao_ngc = input('Escolha uma opção: ')
        if opcao_ngc == '1':
            while True:
                mensagem_ngc = input('Mensagem para o vendedor: ')
                print('1. Editar Feedback\n2. Enviar\n3. Cancelar')
                editar = input('Digite a opção: ') 
                if editar == '1': # Editar e-mail
                    print('Vamos editar')
                    print('Mensagem atual: ', mensagem_ngc) # Continua o texto para edição
                    continue
                elif editar == '2': # Criar e enviar e-mail
                    Sistema.limpar_terminal()
                    print('Enviando email...')
                    try:
                        # EM DESENVOLVIMENTO, o segundo destinatario vai ser o vendedor do item
                        enviar_email(usuario, 'jgsa1502@gmail.com', None, assunto, mensagem_ngc) 
                        print('Mensagem enviada! Uma cópia foi enviada ao seu e-mail também.')
                    except Exception:
                        print('Erro ao enviar mensagem')
                    break
                elif editar == '3':
                    Sistema.limpar_terminal()
                    return menu_global.menu_config(usuario) 
                else:
                    print('Opção Inválida!')
            break
        elif opcao_ngc == '2':
            Sistema.limpar_terminal()    # Em desenvolvimento
            print(f'Número de telefone do vendedor: ')
            opcao_nmr_voltar = input('X. para voltar: ').strip().upper()
            if opcao_nmr_voltar == 'X':
                menu_global.menu_principal(usuario)
                break
            else:
                print('Opção Inválida!')
        elif opcao_ngc == '3':
            Sistema.limpar_terminal()
            menu_global.menu_principal(usuario)
            break
        else:
            print('Opção Inválida!')
        

def lancar_itens(usuario):
    '''
        Nessa função existe a possibilidade de lançar itens à listadeitens.txt.
        Para isso é necessário um nome, descrição, estado do item de 1 a 5 e preço.
        Após as entradas os dados são escritos no txt.
        Melhorias em breve...
    '''
    # Capturar detalhes do novo item e armazenar na lista
    novo_item = input('Novo item: ').strip()
    descricao_novo_item = input('Descrição do item: ').strip()
    estado_novo_item = input('De 1 a 5 qual o estado do material? ').strip()
    preco_novo_item = input('Preço: R$').strip()

    with open('listadeitens.txt', 'r', encoding= 'utf-8') as txt:
        linhas = txt.readlines() # Lendo as linhas da listadeitens.txt
    numeracoes = []
    
    for linha in linhas:
        setor = linha.split('|')     # Organizando cada linha por setor
        separador_numeracao = linha.split('.') # Numeração dos itens
        if len(setor) == 5:      # Só lê as linhas que tem 5 setores
            numeracao = separador_numeracao[1]
            numeracoes.append(numeracao)
    ultima_numeracao = int(numeracoes[-1])      # Verifica quantos itens tem
    nova_numeracao = str(ultima_numeracao + 1)  # Adiciona numeração do próximo item
        

    # Escrever descrições no txt dos itens
    with open('listadeitens.txt', 'a', encoding = 'utf-8') as arquivo:
        arquivo.write(f'.{nova_numeracao}. {novo_item} | R${preco_novo_item} | Estado (1 a 5): {estado_novo_item} | {descricao_novo_item} | \n\n')
    print(f'Item adicionado: {novo_item}')
    menu_global.menu_principal(usuario)

            
def feedback(usuario): 
    '''
        Aqui está a conexão entre o usuário e os desenvolvedores, uma opção de enviar email para os criadores do programa.
        Essa função envia a mensagem (input) para Breno, João e o próprio usuário para mostrar e possibilitar a conversa ao cliente

        Parâmetros:
            usuario (email_log): o email do login_usuario().
    
        Também tem a opção de editar ou cancelar o envio da mensagem
        Se não for possível enviar email retornar.

    '''
    # Achar e-mail do usuario
    email_feedback = None
    with open('bancodedados.txt', 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(',')
            if len(partes) == 3:
                email = partes[1].strip()
                if email == usuario:
                    email_feedback = email
                    break  # achou a linha do e-mail e para
    if email_feedback is None:
        print('Erro tentar novamente')
        return            
    email_suporte1 = 'joao.soaresaraujo@ufrpe.br' # suporte
    email_copia_cliente = email_feedback # email cópia do cliente
    email_suporte2 = 'brenojaccioly@gmail.com' # suporte
    assunto = 'Mensagem enviada dos Feedbacks Bazar Brejó'
    while True:
        # Escrever mensagem
        feed_mensagem = input('Escreva seu feedback: ').strip()
        print('1. Editar Feedback\n2. Enviar\n3. Cancelar')
        editar = input('Digite a opção: ') 
        if editar == '1': # Editar e-mail
            print('Vamos editar')
            print('Feedback atual: ', feed_mensagem) # Continua o texto para edição
            continue
        elif editar == '2': # Criar e enviar e-mail
            Sistema.limpar_terminal()
            print('Enviando email...')
            try:
                enviar_email(email_suporte1, email_suporte2, email_copia_cliente, assunto, feed_mensagem)
                print('Feedback enviado! Uma cópia foi enviada ao seu e-mail também.')
            except Exception:
                print('Erro ao enviar feedback')
            break

        elif editar == '3':
            Sistema.limpar_terminal()
            return menu_global.menu_config(usuario) 
        else:
            print('Opção Inválida!')   

def mudar_nome_config(usuario):
    '''
        Nessa função é possível mudar o nome do usuário nas configurações.
        Ocorre a leitura do bancodedados.txt para separar o nome do email e da senha para conferir os dados e fazer a mudança.
        Antes de mudar o nome, a senha é pedida para confirmar a ação.
        Depois o nome é substituído pelo nome_novo se tudo ocorrer certo.

        Parâmetros:
            usuario (email_log): o email do login_usuario().

        Se a senha ou o nome atual estiverem incorretos, o programa retorna.
        Se o nome não for trocado, exibe a mensagem de erro e retorna.

    '''
    # lendo linhas do banco de dados como {email: senha} (arquivo .txt)
    with open('bancodedados.txt', 'r') as arquivo:
        usuarios = {}
        for line in arquivo:
            partes = line.strip().split(',') 
            if len(partes) == 3:
                nome = partes[0].strip()
                email = partes[1].strip()
                senha = partes[2].strip()
                usuarios[email] = senha

    # confirmação da senha:
    while True: 
        print('Digite sua senha atual: Sua senha tem 8 caracteres')
        senha_cadastrada = input_senha('Sua senha: ').strip()

        # Se a senha for a mesma da linha do usuário no banco de dados
        if senha_cadastrada == usuarios.get(usuario):
            Sistema.limpar_terminal()
            print('Senha correta')
            break            
        else:
            Sistema.limpar_terminal()
            print('Senha incorreta')

    nome_usuario = None

    with open('bancodedados.txt', 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(',')
            if len(partes) == 3:
                nome = partes[0].strip()
                email = partes[1].strip()
                senha = partes[2].strip()
                if email == usuario:
                    nome_usuario = nome
                    break  # achou a linha do usuario e para

    if nome_usuario:
        print(f'nome atual: {nome_usuario}')
    else:
        print('Erro: usuário não encontrado.')

    nome_novo = input('Novo nome: ')
    # Lê todas as linhas do arquivo
    with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Cria uma lista para armazenar as novas linhas do banco de dados
    nova_lista_nome = []
    nome_trocado = False
    for linha in linhas:
        partes = linha.strip().split(',')
        if len(partes) == 3:
            nome = partes[0].strip()
            email = partes[1].strip()
            senha = partes[2].strip()
        
            if email == usuario:
                nova_linha = f'{nome_novo},{email},{senha}\n'
                nova_lista_nome.append(nova_linha)
                nome_trocado = True
            else:
                nova_lista_nome.append(linha)
        else:
            nova_lista_nome.append(linha)

    if nome_trocado:
        with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(nova_lista_nome)
        print('Nome atualizado com sucesso!')
        menu_global.menu_principal(usuario)
    else:
        Sistema.limpar_terminal()
        print('Erro: e-mail não encontrado.')
        menu_global.menu_principal(usuario)

    

def mudar_senha_config(usuario):
    '''
        Muito parecida com mudar_nome_config, essa função é possível mudar a senha do usuário nas configurações.
        Ocorre a leitura do bancodedados.txt para separar a senha do email e do nome para conferir os dados e fazer a mudança.
        Antes de mudar, a senha é pedida para confirmar a ação.
        Depois a senha é substituída pelo senha_nova se tudo ocorrer certo.

        Parâmetros:
            usuario (email_log): o email do login_usuario().

        Se a senha ou o nome atual estiverem incorretos, o programa retorna.
        Se a senha não for trocada, exibe a mensagem de erro e retorna.

    '''
    # lendo linhas do banco de dados como {email: senha} (arquivo .txt)
    with open('bancodedados.txt', 'r') as arquivo:
        usuarios = {}
        for line in arquivo:
            partes = line.strip().split(',') 
            if len(partes) == 3:   # Separa email da senha
                email = partes[1].strip()
                senha = partes[2].strip()
                usuarios[email] = senha                    
            
    # confirmação da senha:
    while True: 
        print('Digite sua senha atual: Sua senha tem 8 caracteres')
        senha_cadastrada = input_senha('Sua senha: ').strip() # Chamar criptografia

        # Se a senha for a mesma da linha do usuário no banco de dados
        if senha_cadastrada == usuarios[usuario]:
            Sistema.limpar_terminal()
            print('Senha correta')
            break            
        else:
            Sistema.limpar_terminal()
            print('Senha incorreta')

    senha_nova = input_senha('Nova senha: ').strip()

    # Lê todas as linhas do arquivo
    with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Cria uma lista para armazenar as novas linhas do banco de dados
    nova_lista_senha = []

    # Verifica se foi possível atualizar
    senha_trocada = False

    for linha in linhas:
        partes = linha.strip().split(',')
        if len(partes) == 3:
            nome = partes[0].strip()
            email = partes[1].strip()
            senha = partes[2].strip()
            if email == usuario:
                nova_linha = f'{nome},{email},{senha_nova}\n' 
                nova_lista_senha.append(nova_linha)
                senha_trocada = True # Confirma alteração
            else:
                nova_lista_senha.append(linha)
        else:
            nova_lista_senha.append(linha)

    if senha_trocada:
        # Só reescreve o arquivo após o loop completo
        with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
            arquivo.writelines(nova_lista_senha)
        print('Senha atualizada com sucesso!')
        menu_global.menu_principal(usuario)
    else:
        print('Erro: e-mail não encontrado.')

def excluir_conta(usuario):
    '''
        Aqui é a parte que se pode deletar a conta do usuário depois da confirmação digitando 1
        Após ler o bancodedados.txt a linha que contem a conta do usuário atual é apagada, excluindo assim o cadastro da pessoa.
        Se digitar 2, volta para o menu_config().
        Se opção inválida, continua até opção válida.
        
        Parâmetros:
            usuario (email_log): o email do login_usuario().

        Se não for possível excluir a conta, exibir mensagem de erro e ir para menu_config()

    '''
    print('Você realmente deseja excluir sua conta? \n1. Sim \n2. Não, voltar')
    resposta_ec = input('Digite a opção desejada: ')
    conta_excluida = False
    while True:
        if resposta_ec == '1':
        # Lê todas as linhas do arquivo
            email_excluir = str(usuario)
            print(email_excluir)
            with open('bancodedados.txt', 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
            

            nova_lista_conta = [linha for linha in linhas if linha.strip().split(',')[1] != email_excluir]
            if len(nova_lista_conta) == len(linhas):
                print('Usuário não encontrado')
            else:
                conta_excluida = True
                with open('bancodedados.txt', 'w', encoding='utf-8') as arquivo:
                    arquivo.writelines(nova_lista_conta)
                print("Excluindo conta\nLimpando a tela em:")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                    Sistema.limpar_terminal()
            
            if conta_excluida:
                print('Conta exluída com sucesso!')
            else:
                print('Erro ao encontrar email. Tente novamente') 
                menu_global.menu_config(usuario)
            break

        elif resposta_ec == '2':
            Sistema.limpar_terminal()
            menu_global.menu_config(usuario)
            break
        else:
            Sistema.limpar_terminal()
            print('Opção inválida')    

class Menu:
    def __init__(self, sistema):
        self.sistema = sistema
    def menu_inicial(self):
        '''
            A primeira tela do programa é esse menu que contem as opções de Cadastro e Login para acessar o bazar.
            Essa função é chamada pela main() para sempre começar por aqui.
            Tem como entrada 1 e 2 que chamam o cadastro e o login respectivamente. 
            Em caso de uma entrada inválida continua até receber 1 ou 2.

        '''
        while True:
            Sistema.limpar_terminal()
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
                Sistema.limpar_terminal()
                print('Escolha 1 ou 2')

    def menu_cadastro(self):
        '''
            Similar ao menu inicial, aqui também são exibidas opções para acessar o Bazar: novo usuário ou voltar
            Recebe as entradas 1, 2 e 3 como opções de cadastrar, voltar para fazer o login e voltar ao menu inicial
            Em caso de uma entrada inválida continua até receber 1, 2 ou 3.
        '''
        while True:
            Sistema.limpar_terminal()
            # Opções do cadastro, ir para login e voltar
            opcao_menu_cadastro = input('Login: Escolha uma opção: \n1. Novo usuário e senha \n2. Já tem conta? Volte e façe o login \n3. Voltar ao menu inicial \n').strip()
            if opcao_menu_cadastro == '1':
                self.sistema.cadastrar()
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
            Sistema.limpar_terminal()
            # Opções do login, esqueci senha e voltar
            opcao_menu_login = input('Login: Escolha uma opção: \n1. Usuário e senha \n2. Esqueci a senha \n3. Voltar ao menu inicial \n').strip()
            if opcao_menu_login == '1':
                self.sistema.efetuar_login()
                break
            elif opcao_menu_login == '2':
                self.sistema.esqueci_senha()
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
                Sistema.limpar_terminal()
                print('Itens disponíveis')
                comprar_itens(usuario)
                break
            elif resposta_mp == '2':
                Sistema.limpar_terminal()
                print('Adicionar item')
                lancar_itens(usuario)
                break
            elif resposta_mp == '3':
                Sistema.limpar_terminal()
                self.menu_config(usuario)
                break
            elif resposta_mp == 'x':
                # Animação da saída do terminal
                Sistema.limpar_terminal()
                print("Encerrando Programa\nLimpando a tela em:")
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                Sistema.limpar_terminal()
                break
            else:
                print('Opção inválida')
                Sistema.limpar_terminal()

    def menu_config(self, usuario):
        '''
            Aqui são exibidas as opções das configurações como feedback, mudar nome, mudar senha, excluir conta e voltar.

            Parâmetros:
                usuario (email_log): o email do login_usuario().

            Se a opção for inválida continuar até receber uma entrada válida.
        '''
        while True:
            print('=============\nConfigurações\n=============\n')
            print('1. Feedback \n2. Mudar nome \n3. Mudar senha\n4. Exluir conta \n5. Voltar')
            resposta_mc = input('\nDigite a opção desejada: ').strip()
            if resposta_mc == '1':
                Sistema.limpar_terminal()
                print('Feedback')
                feedback(usuario)
                break
            elif resposta_mc == '2':
                Sistema.limpar_terminal()
                print('Mudar nome da conta')
                mudar_nome_config(usuario)
                break
            elif resposta_mc == '3':
                Sistema.limpar_terminal()
                print('Mudar senha da conta')
                mudar_senha_config(usuario)
                break
            elif resposta_mc == '4':
                Sistema.limpar_terminal()
                excluir_conta(usuario)
                break
            elif resposta_mc == '5':
                Sistema.limpar_terminal()
                menu_global.menu_principal(usuario)
                break
            else:
                print('Opção inválida')
                Sistema.limpar_terminal()


                

class Sistema:
    def __init__(self):
        pass
        
    def cadastrar(self):
        '''
            Aqui é onde o CRUD começa de fato. Essa função recebe as entradas: nome, email e senha.
            Essas entradas vem de cadastro_nome, cadastro_usuario e cadastro_senha respectivamente.
            Após receber esses dados, os armazena em um arquivo chamado 'bancodedados.txt' e depois chama o login.
        '''
        self.limpar_terminal()
        nome_cd = self.cadastro_nome()
        # Cadastro do usuário
        email_cd = self.cadastro_usuario()
        # Cadastro da senha
        senha_cd = self.cadastro_senha()
        # Cadastro do Whatsapp
        numero_cd = self.cadastro_numero()
        # Escrever todos os cadastros no bancodedados.txt
        with open('bancodedados.txt', 'a', encoding = 'utf-8') as arquivo:
            arquivo.write(f'{nome_cd},{email_cd},{senha_cd},{numero_cd}\n')
        # Ir para o login após cadastro
        self.efetuar_login()

    def efetuar_login(self):
        '''
            Essa função recebe a entrada do usuário pelo login_usuario e o localiza no bancodedados.txt.
            Após a leitura, o email é separado da senha pelo .split(',').
            Depois compara a senha com o input senha_log para verificar se a senha está correta.
            Se o usuário não estiver no banco de dados ele retorna. 
            Se a senha não for encontrada continua até receber a senha correta.
        '''
        self.limpar_terminal() 
        # Login de usuário:
        usuario = self.login_usuario()
        # Login da senha:
        # lendo linhas do banco de dados como {email: senha} (arquivo .txt)
        with open('bancodedados.txt', 'r') as arquivo:
            usuarios = {}
            for line in arquivo:
                partes = line.strip().split(',') 
                if len(partes) == (3 or 4):   # Separa email da senha
                    email = partes[1].strip()
                    senha = partes[2].strip()
                    usuarios[email] = senha

        if usuario not in usuarios: # Se usuário não tiver no banco de dados
            self.limpar_terminal()
            print('Usuário não encontrado.')
            return                    
                
        # Login da senha:
        while True: 
            print('Login: Sua senha tem 8 caracteres')
            senha_log = input_senha('Senha: ').strip() # Chamar criptografia

            # Se a senha for a mesma da linha do usuário no banco de dados
            if senha_log == usuarios[usuario]:
                self.limpar_terminal()
                menu_global.menu_principal(usuario)
                return senha_log and usuario
                
            else:
                self.limpar_terminal()
                print('Senha incorreta')

    def cadastro_nome(self):
        '''
            Nessa função o nome do usuario é a entrada que vai ser retornada ao cadastro.
            Antes de retornar, confere se o nome já está em uso lendo o bancodedados.txt.
            Se nome já está cadastrado repete o input para nova entrada.

        '''
        print('Digite seu nome')
        while True:
            nome_cd = input('Nome: ').strip()
            # Checar se nome já é cadastrado
            with open('bancodedados.txt', 'r') as arquivo:
                usuarios = arquivo.read()
            if nome_cd in usuarios:
                print('Esse nome já foi usado')
            else:
                self.limpar_terminal()
                return nome_cd

    def cadastro_usuario(self):
        '''
            Nessa função o email do usuario é a entrada que vai ser retornada ao cadastro.
            Restringe a entrada para conter um email válido: @ufrpe.br ou @gmail.com
            Antes de retornar, confere se o email já está em uso lendo o bancodedados.txt.
            Se email está inválido continua até receber uma entrada válida.
            Se email já está cadastrado repete o input para nova entrada.
        '''
        print ('Cadastro : digite o usuário (e-mail)')
        print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
        while True:
            email_cd = input ('Usuário: ').strip().lower()
            email_arroba = email_cd.split('@')
            # Restrição de e-mails para o usuário: @ e terminar com entradas válidas
            if len(email_arroba) == 2 and (email_cd.endswith('@ufrpe.br') or email_cd.endswith('@gmail.com')):
                self.limpar_terminal()
                print('Usuário válido')
                # Checar se usuário já é cadastrado
                with open('bancodedados.txt', 'r') as arquivo:
                    usuarios = arquivo.read()
                if email_cd in usuarios:
                    self.limpar_terminal()
                    print('Usuário já cadastrado, Insira outro e-mail!')
                else:
                    self.limpar_terminal()
                    return email_cd
            else:
                self.limpar_terminal()
                print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

    def cadastro_senha(self):
        '''
            Aqui recebe-se a entrada da senha do cadastro com confirmação.
            As restrinções são o tamanho (precisa conter 8 caracteres) e a tecla de espaço.
            Se a senha não obedecer as restrinções continua até receber uma entrada válida.
            Se a senha não for a mesma na confirmação repete o input até ter confimação.
        '''
        while True:
            print('Sua senha precisa ter 8 caracteres')
            senha_cd = input_senha('Senha: ').strip()
            
            # Restrição do tamanho da senha
            if len(senha_cd) != 8:
                self.limpar_terminal()
                print('senha inválida.')
            # Confirmação da senha
            else:
                senha_2 = input_senha('Confirme a senha: ').strip()
                if senha_cd == senha_2:
                    self.limpar_terminal()
                    print('Senha cadastrada!') 
                    return senha_cd
                else:
                    self.limpar_terminal()
                    print('As senhas precisam ser idênticas.')

    def cadastro_numero(self):
        '''
        Fazer a docstring...
        '''

        print('Deseja cadastrar seu Whatsapp?\n1. Sim\n2. Não')
        opcao_cd_numero = input('Digite: ')
        if opcao_cd_numero == '1':
            while True:
                print('Digite seu Whatsapp, apenas números!')
                numero_cd = input('Número: ').strip()
                # Restricões do tamanho do número. Padrão (81) 912341234
                if len(numero_cd) != 11:
                    print('Número inválido. Padrão => 81983548906')
                else:
                    self.limpar_terminal()
                    print('Número Cadastrado')
                    return numero_cd
        elif opcao_cd_numero == '2':
            self.limpar_terminal
            return "" # Precisa retornar o vazio.
        else:
            print('Opção Inválida! Digite 1 ou 2.')
            
        
    def login_usuario(self):
        '''
            Essa função recebe o email e lê o bancodedados.txt para verificar se o usuário é válido.
            Se o email não estiver no txt repete o input até receber uma entrada válida.
        '''
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
                self.limpar_terminal()
                print('Usuário inválido ou esse e-mail não está cadastrado')
        
    def esqueci_senha(self):
        '''
            Aqui está presente a função que consegue mudar a senha do usuário cadastrado antes do login.
            Isso é possível porque após confirmar o usuário o código manda um código para o email do usuário.
            Depois chama as funções enviar_email e mudar_senha_esqueci para a confirmação do código e troca de senha
            Se o email não estiver no txt, repete o input até receber uma entrada válida.
            Se o código não estiver correto, repete o input até confirmar o código.
            
        '''
        while True:
            print('Login: digite seu e-mail para recuperar senha:')
            email_log = input('Usuário: ').strip()

            # Checar se o usuário está presente no arquivo
            with open('bancodedados.txt', 'r') as arquivo:
                txt = arquivo.read()
            if email_log in txt:
                print('Usuário valido')
                print('Enviando email...')
                codigo =  random.randint(100000,999999) 
                conteudo = (f"Olá! Seu código de verificação é: {codigo}")
                enviar_email(email_log, None, None, 'Mensagem do Bazar Brejó!', conteudo)
                while True:
                    codigo_input = input('digite o código enviado ao seu email: ').strip()
                    if codigo_input == str(codigo):
                        print('Código correto. Agora crie uma senha nova')
                        mudar_senha_esqueci(email_log)
                        return codigo_input and email_log
                    else:
                        print('Código incorreto')
                    
            else:
                self.limpar_terminal()
                print('Usuário inválido ou esse e-mail não está cadastrado')
    @staticmethod
    def limpar_terminal():
        '''
            Aqui está a função mais usada do código.
            Ela limpa o terminal tanto em sistemas Windows quanto Mac e Linux
        '''
        # Para limpar o terminal em qualquer os
        os.system('cls' if os.name == 'nt' else 'clear')

def main(): # Sempre começar pelo Menu Incial
    '''
        Essa função é por onde o código inicia e chama o menu_inicial() para iniciar o programa.
    '''

    Sistema.limpar_terminal()
    global menu_global
    sistema = Sistema()
    menu_global = Menu(sistema)
    menu_global.menu_inicial()

if __name__ == '__main__':
    main()  
