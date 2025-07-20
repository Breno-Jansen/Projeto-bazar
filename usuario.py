import os # Possibilita a entrada no sistema do terminal (e também para limpá-lo)
import time # Import para permitir uso do tempo no terminal
import sys # Verificar sistema atual
import random # Import que possibilita números randomicos
import smtplib # Import para fazer login no meu email
from email.mime.multipart import MIMEMultipart # Função para criar uma mensagem de e-mail que pode conter texto ou anexos
from email.mime.text import MIMEText # Função para criar o conteúdo de texto que será colocado no e-mail
from rich.console import Console
from rich.panel import Panel

class Usuario:

    def __init__(self):
        pass        
    def input_senha(self, prompt = 'Senha: '): # Senha com asteriscos
    
        '''
            Faz a criptografia da senha no terminal, tanto para o sistema windows quanto para Mac e Linux.

            Parâmetros:
                prompt (input) = 'Senha: ': Quando essa fução é chamada, gera um input que esconde a senha escrita.

            Armazena as teclas digitadas e retorna com '********' no terminal.
            Tenta fazer a criptografia e em caso de erro retorna o input.
        '''
        # Não se pôde importar os menus globalmente para não ter um ciclo de erro nos arquivos
        from menu import Menu
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
                    Menu.limpar_terminal()
                    print('Senha inválida. Ela deve ter exatamente 8 caracteres')
                    continue
                else:
                    return senha
                
            except Exception: # Se o terminal não suportar a entrada
                print("\n  Falha ao esconder a senha. Digite normalmente.")
                return input(prompt)



    def enviar_email(self, destinatario1, destinatario2, destinatario3, assunto, conteudo):
        '''
            Aqui o programa envia uma mensagem com o código aleatório para o usuário
            O código  é enviado pelo email brenojaccioly@gmail.com (um dos criadores do Bazar) com a senha_app do google.

            Parâmetros:
                usuario (email_log): o email do login do esqueci a senha.
                codigo (codigo): codigo de 6 dígitos aleatório.
            
            Tenta enviar código pela internet, se não conseguir, exibe mensagem de erro e volta ao menu_login().
        '''
        from menu import Menu

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

    
    def cadastrar(self):
        '''
            Aqui é onde o CRUD começa de fato. Essa função recebe as entradas: nome, email e senha.
            Essas entradas vem de cadastro_nome, cadastro_usuario e cadastro_senha respectivamente.
            Após receber esses dados, os armazena em um arquivo chamado 'bancodedados.txt' e depois chama o login.
        '''
        from menu import Menu
        Menu.limpar_terminal()
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
        from sistema import menu_global # Não pôde ser feito um import global para não dar erro circular entre os arquivos
        from menu import Menu
        Menu.limpar_terminal() 
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
            Menu.limpar_terminal()
            print('Usuário não encontrado.')
            return                    
                
        # Login da senha:
        while True: 
            print('Login: Sua senha tem 8 caracteres')
            senha_log = self.input_senha('Senha: ').strip() # Chamar criptografia

            # Se a senha for a mesma da linha do usuário no banco de dados
            if senha_log == usuarios[usuario]:
                Menu.limpar_terminal()
                menu_global.menu_principal(usuario)
                return senha_log and usuario
                
            else:
                Menu.limpar_terminal()
                print('Senha incorreta')

    def cadastro_nome(self):
        '''
            Nessa função o nome do usuario é a entrada que vai ser retornada ao cadastro.
            Antes de retornar, confere se o nome já está em uso lendo o bancodedados.txt.
            Se nome já está cadastrado repete o input para nova entrada.

        '''
        from menu import Menu
        print('Digite seu nome')
        while True:
            nome_cd = input('Nome: ').strip()
            # Checar se nome já é cadastrado
            with open('bancodedados.txt', 'r') as arquivo:
                usuarios = arquivo.read()
            if nome_cd in usuarios:
                print('Esse nome já foi usado')
            else:
                Menu.limpar_terminal()
                return nome_cd

    def cadastro_usuario(self):
        '''
            Nessa função o email do usuario é a entrada que vai ser retornada ao cadastro.
            Restringe a entrada para conter um email válido: @ufrpe.br ou @gmail.com
            Antes de retornar, confere se o email já está em uso lendo o bancodedados.txt.
            Se email está inválido continua até receber uma entrada válida.
            Se email já está cadastrado repete o input para nova entrada.
        '''
        from menu import Menu
        print ('Cadastro : digite o usuário (e-mail)')
        print ('O usuário precisa terminar com @gmail.com ou @ufrpe.br')
        while True:
            email_cd = input ('Usuário: ').strip().lower()
            email_arroba = email_cd.split('@')
            # Restrição de e-mails para o usuário: @ e terminar com entradas válidas
            if len(email_arroba) == 2 and (email_cd.endswith('@ufrpe.br') or email_cd.endswith('@gmail.com')):
                Menu.limpar_terminal()
                print('Usuário válido')
                # Checar se usuário já é cadastrado
                with open('bancodedados.txt', 'r') as arquivo:
                    usuarios = arquivo.read()
                if email_cd in usuarios:
                    Menu.limpar_terminal()
                    print('Usuário já cadastrado, Insira outro e-mail!')
                else:
                    Menu.limpar_terminal()
                    return email_cd
            else:
                Menu.limpar_terminal()
                print('Usuário inválido. E-mails aceitos: @ufrpe.br ou @gmail.com')

    def cadastro_senha(self):
        '''
            Aqui recebe-se a entrada da senha do cadastro com confirmação.
            As restrinções são o tamanho (precisa conter 8 caracteres) e a tecla de espaço.
            Se a senha não obedecer as restrinções continua até receber uma entrada válida.
            Se a senha não for a mesma na confirmação repete o input até ter confimação.
        '''
        from menu import Menu
        while True:
            print('Sua senha precisa ter 8 caracteres')
            senha_cd = self.input_senha('Senha: ').strip()
            
            # Restrição do tamanho da senha
            if len(senha_cd) != 8:
                Menu.limpar_terminal()
                print('senha inválida.')
            # Confirmação da senha
            else:
                senha_2 = self.input_senha('Confirme a senha: ').strip()
                if senha_cd == senha_2:
                    Menu.limpar_terminal()
                    print('Senha cadastrada!') 
                    return senha_cd
                else:
                    Menu.limpar_terminal()
                    print('As senhas precisam ser idênticas.')

    def cadastro_numero(self):
        '''
        Fazer a docstring...
        '''
        from menu import Menu

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
                    Menu.limpar_terminal()
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
        from menu import Menu
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
                Menu.limpar_terminal()
                print('Usuário inválido ou esse e-mail não está cadastrado')
        
    def esqueci_senha(self):
        '''
            Aqui está presente a função que consegue mudar a senha do usuário cadastrado antes do login.
            Isso é possível porque após confirmar o usuário o código manda um código para o email do usuário.
            Depois chama as funções enviar_email e mudar_senha_esqueci para a confirmação do código e troca de senha
            Se o email não estiver no txt, repete o input até receber uma entrada válida.
            Se o código não estiver correto, repete o input até confirmar o código.
        '''
        from menu import Menu
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
                self.enviar_email(email_log, None, None, 'Mensagem do Bazar Brejó!', conteudo)
                while True:
                    codigo_input = input('digite o código enviado ao seu email: ').strip()
                    if codigo_input == str(codigo):
                        print('Código correto. Agora crie uma senha nova')
                        self.mudar_senha_esqueci(email_log)
                        return codigo_input and email_log
                    else:
                        print('Código incorreto')
                    
            else:
                Menu.limpar_terminal()
                print('Usuário inválido ou esse e-mail não está cadastrado')

        
    def mudar_senha_esqueci(self, usuario):
        '''
            Essa função é iniciada após a confirmação do código, então ela recebe como entrada a nova senha
            Ocorre a leitura do bancodedados.txt para separar a senha do usuário e trocá-la pela senha_nova.
            
            Parâmetros:
                usuario(email_log): o email do login do esqueci a senha.

            Se a senha não for trocada exibe mensagem de erro e volta para menu inicial.
        '''
        from sistema import menu_global
        from menu import Menu

        Menu.limpar_terminal()
        print('Código correto')
        senha_nova = self.input_senha('Nova senha: ').strip()

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

    def mudar_nome_config(self, usuario):
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
        from sistema import menu_global
        from menu import Menu
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
            senha_cadastrada = self.input_senha('Sua senha: ').strip()

            # Se a senha for a mesma da linha do usuário no banco de dados
            if senha_cadastrada == usuarios.get(usuario):
                Menu.limpar_terminal()
                print('Senha correta')
                break            
            else:
                Menu.limpar_terminal()
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
            Menu.limpar_terminal()
            print('Erro: e-mail não encontrado.')
            menu_global.menu_principal(usuario)

        

    def mudar_senha_config(self, usuario):
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
        from sistema import menu_global
        from menu import Menu
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
            senha_cadastrada = self.input_senha('Sua senha: ').strip() # Chamar criptografia

            # Se a senha for a mesma da linha do usuário no banco de dados
            if senha_cadastrada == usuarios[usuario]:
                Menu.limpar_terminal()
                print('Senha correta')
                break            
            else:
                Menu.limpar_terminal()
                print('Senha incorreta')

        senha_nova = self.input_senha('Nova senha: ').strip()

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

    def excluir_conta(self, usuario):
        '''
            Aqui é a parte que se pode deletar a conta do usuário depois da confirmação digitando 1
            Após ler o bancodedados.txt a linha que contem a conta do usuário atual é apagada, excluindo assim o cadastro da pessoa.
            Se digitar 2, volta para o menu_config().
            Se opção inválida, continua até opção válida.
            
            Parâmetros:
                usuario (email_log): o email do login_usuario().

            Se não for possível excluir a conta, exibir mensagem de erro e ir para menu_config()

        '''
        from sistema import menu_global
        from menu import Menu
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
                        Menu.limpar_terminal()
                
                if conta_excluida:
                    print('Conta exluída com sucesso!')
                else:
                    print('Erro ao encontrar email. Tente novamente') 
                    menu_global.menu_config(usuario)
                break

            elif resposta_ec == '2':
                Menu.limpar_terminal()
                menu_global.menu_config(usuario)
                break
            else:
                Menu.limpar_terminal()
                print('Opção inválida')    


    def feedback(self, usuario):
        '''
            Aqui está a conexão entre o usuário e os desenvolvedores, uma opção de enviar email para os criadores do programa.
            Essa função envia a mensagem (input) para Breno, João e o próprio usuário para mostrar e possibilitar a conversa ao cliente

            Parâmetros:
                usuario (email_log): o email do login_usuario().
        
            Também tem a opção de editar ou cancelar o envio da mensagem
            Se não for possível enviar email retornar.

        '''
        from sistema import menu_global
        from menu import Menu
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
                Menu.limpar_terminal()
                print('Enviando email...')
                try:
                    self.enviar_email(email_suporte1, email_suporte2, email_copia_cliente, assunto, feed_mensagem)
                    print('Feedback enviado! Uma cópia foi enviada ao seu e-mail também.')
                except Exception:
                    print('Erro ao enviar feedback')
                break

            elif editar == '3':
                Menu.limpar_terminal()
                return menu_global.menu_config(usuario) 
            else:
                print('Opção Inválida!')   
    
    def registrar_compra(self, login_usuario, nome_produto, valor):
        '''
        Salva a compra no extrato.txt no formato:
        email: item1 | item2 | item3 ...
        '''

        from datetime import datetime # Import para usar o datetime.now, registra a data e hora atual

        data = datetime.now().strftime('%d-%m-%Y %H:%M')
        nova_entrada = (f'{nome_produto} - R${valor:.2f} ({data})')

        try:
            with open('extrato.txt', 'r', encoding= 'utf-8') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            linhas = []
        
        nova_linha = []
        usuario_encontrado = False

        for linha in linhas:
            if linha.startswith(f'{login_usuario}:'):
                usuario_encontrado = True
                linha = linha.strip()
                if not linha.endswith('|'):
                    linha += ' |'
                linha += f' {nova_entrada} |'
                nova_linha.append(linha + '\n')
            else:
                nova_linha.append(linha)

        if not usuario_encontrado:
            nova_linha.append(f'{login_usuario}: {nova_entrada} |\n')

        with open('extrato.txt', 'w', encoding='utf-8') as f:
            f.writelines(nova_linha)
    
    def mostrar_extrato(self, usuario):
        from sistema import menu_global
        from menu import Menu
        
        
        console = Console()
        try:
            with open('extrato.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()
        except FileNotFoundError:
            linhas = []

        encontrou = False
        conteudo = ""

        for linha in linhas:
            if linha.startswith(f'{usuario}'):
                conteudo_raw = linha.split(':', 1)[1].strip().strip('|')
                itens = [f'• {item.strip()}' for item in conteudo_raw.split('|') if item.strip()]
                conteudo = '\n'.join(itens)
                encontrou = True
                break

        if encontrou:
            panel = Panel(conteudo, title=f'Extrato do usuário: {usuario}', border_style='green')
            console.print(panel)
        else:
            console.print(f'[bold red]Nenhum item registrado para {usuario}.[/bold red]')

        while True:
            console.print('\n[bold yellow]X[/bold yellow] - Voltar')
            opcao = input('Digite: ').strip().upper()
            if opcao == 'X':
                Menu.limpar_terminal()
                menu_global.menu_config(usuario)
                break