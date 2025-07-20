class Item:
    def __init__(self, nome, preco, estado, descricao, usuario):
        self.nome = nome
        self.preco = preco
        self.estado = estado
        self.descricao = descricao
        self.usuario = usuario

    def salvar_item(self):
        """
            Salva o item atual no arquivo listadeitens.txt
        """
        from sistema import menu_global

        try:
            with open('listadeitens.txt', 'r', encoding='utf-8') as txt:
                linhas = txt.readlines()
            numeracoes = [
                int(linha.split('.')[1])
                for linha in linhas if '|' in linha and len(linha.split('|')) == 5
            ]
            nova_numeracao = str(max(numeracoes) + 1) if numeracoes else '1'
        except FileNotFoundError:
            nova_numeracao = '1'

        with open('listadeitens.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'.{nova_numeracao}. {self.nome} | R${self.preco} | Estado (1 a 5): {self.estado} | {self.descricao} | \n\n')

        print(f'\n✅ Item "{self.nome}" adicionado com sucesso!')
        menu_global.menu_principal(self.usuario)


    @staticmethod
    def carregar_itens():
        """
            Lê todos os itens do arquivo 'listadeitens.txt' e retorna uma lista de objetos Item.
        """
        itens = []
        try:
            with open('listadeitens.txt', 'r', encoding='utf-8') as txt:
                linhas = txt.readlines()
            for linha in linhas:
                if '|' in linha and len(linha.split('|')) == 5:
                    partes = linha.split('|')
                    nome_e_numero = partes[0].split('. ', 1)[1].strip()
                    preco = partes[1].replace('R$', '').strip()
                    estado = partes[2].replace('Estado (1 a 5):', '').strip()
                    descricao = partes[3].strip()
                    item = Item(nome_e_numero, preco, estado, descricao, usuario=None)  # Sem dono definido
                    itens.append(item)
        except FileNotFoundError:
            print('Arquivo de itens não encontrado.')
        return itens

    @classmethod
    def lancar_item(cls, usuario):
        """
            Nessa função existe a possibilidade de lançar itens à listadeitens.txt.
            Para isso é necessário um nome, descrição, estado do item de 1 a 5 e preço.
            Após as entradas os dados são escritos no txt.        
        """
        print('\n--- Lançar Novo Item ---')
        nome = input('Nome do item: ').strip()
        descricao = input('Descrição do item: ').strip()

        while True:
            estado = input('Estado do item (1 a 5): ').strip()
            if estado.isdigit() and 1 <= int(estado) <= 5:
                break
            print('Estado inválido. Digite um número entre 1 e 5.')

        while True:
            preco = input('Preço (R$): ').strip().replace(',', '.')
            try:
                float(preco)
                break
            except ValueError:
                print('Preço inválido. Digite um valor numérico.')

        # Criar instância do item e salvar
        item = cls(nome, preco, estado, descricao, usuario)
        item.salvar_item()

    @staticmethod
    def remover_item_do_arquivo(nome_item):
        """
        Remove o item com o nome correspondente do arquivo listadeitens.txt
        """
        try:
            with open('listadeitens.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            with open('listadeitens.txt', 'w', encoding='utf-8') as f:
                for linha in linhas:
                    if nome_item not in linha:
                        f.write(linha)
        except FileNotFoundError:
            print('Arquivo listadeitens.txt não encontrado.')


    @staticmethod
    def comprar_itens(usuario):
        """
            Mostra os itens disponíveis do txt e permite ao usuário comprar ou negociar.
            EM DESENVOLVIMENTO (pagamento)
        """
        from sistema import menu_global
        from menu import Menu
        from usuario import Usuario
        usuario_obj = Usuario()
        itens = Item.carregar_itens()

        if not itens:
            print('Nenhum item disponível.')
            return menu_global.menu_principal(usuario)

        for index, item in enumerate(itens, start=1):
            print(f' .{index}. {item.nome.ljust(35)} | R${item.preco}')
        print(' .X. Voltar para o menu principal')

        while True:
            escolha = input('Escolha um produto (número) ou X para voltar: ').strip().lower()
            if escolha == 'x':
                return menu_global.menu_principal(usuario)
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(itens):
                print('Opção inválida.')
                continue

            index = int(escolha) - 1
            item_selecionado = itens[index]
            Menu.limpar_terminal()
            while True:
                print(f'Item: {item_selecionado.nome}')
                print('Mais informações:')
                print(f'{item_selecionado.descricao}, Estado: {item_selecionado.estado}, Preço: R${item_selecionado.preco}')
                opcao = input('1. Comprar\n2. Negociar com o vendedor\n3. Voltar\nOpção: ')
                if opcao == '1':
                    Menu.limpar_terminal()
                    while True:
                        print(f'Para comprar "{item_selecionado.nome}", faça o pix de R${item_selecionado.preco} para o pix: 704.514.384-26')
                        confirmar = input('1. Confirmar compra\n2. Cancelar\nOpção: ')
                        if confirmar == '1':
                            print('Email enviado! Venha para o Ceagri II para pegar seu item.')
                            # Registra no extrato
                            try:
                                preco_float = float(item_selecionado.preco.replace(',','.'))
                                usuario_obj.registrar_compra(item_selecionado.nome, preco_float)
                            except Exception as e:
                                print('Erro ao registrar no extrato:', e)
                            # Remove do arquivo listadeitens.txt
                            try:
                                Item.remover_item_do_arquivo(item_selecionado.nome)
                            except Exception as e:
                                print('Erro ao remover item', e)

                            return menu_global.menu_principal(usuario)    
                        elif confirmar == '2':
                            Menu.limpar_terminal()
                            print('Voltando...')
                            break
                        else:
                            Menu.limpar_terminal()
                            print('Opção inválida.')
                    break
                elif opcao == '2':
                    Item.negociar(usuario, item_selecionado)
                    break
                elif opcao == '3':
                    Menu.limpar_terminal()
                    menu_global.menu_principal(usuario)
                    break
                else:
                    Menu.limpar_terminal()
                    print('Opção inválida.')
            break

    @staticmethod
    def negociar(usuario, item):
        """
            Permite negociar com o vendedor (em desenvolvimento).
        """
        from sistema import menu_global
        from menu import Menu

        print('Para negociar com o vendedor:')
        print('1. Escrever email\n2. Ver contato\n3. Voltar')
        assunto = 'Um cliente do Bazar Brejó quer negociar com você!'

        while True:
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                mensagem = input('Mensagem para o vendedor: ')
                while True:
                    print('1. Editar mensagem\n2. Enviar\n3. Cancelar')
                    editar = input('Opção: ')
                    if editar == '1':
                        print('Mensagem atual:', mensagem)
                        mensagem = input('Nova mensagem: ')
                    elif editar == '2':
                        Menu.limpar_terminal()
                        try:
                            item.usuario.enviar_email(usuario, 'jgsa1502@gmail.com', None, assunto, mensagem)
                            print('Mensagem enviada! Uma cópia foi enviada ao seu e-mail.')
                        except Exception:
                            print('Erro ao enviar mensagem.')
                        return
                    elif editar == '3':
                        Menu.limpar_terminal()
                        return menu_global.menu_config(usuario)
                    else:
                        print('Opção inválida.')
            elif opcao == '2':
                Menu.limpar_terminal()
                print('Número de telefone do vendedor: [em desenvolvimento]')
                if input('Digite X para voltar: ').strip().upper() == 'X':
                    return menu_global.menu_principal(usuario)
            elif opcao == '3':
                Menu.limpar_terminal()
                return menu_global.menu_principal(usuario)
            else:
                print('Opção inválida.')
