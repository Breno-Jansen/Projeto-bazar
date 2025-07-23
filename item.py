from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import time

console = Console()

class Item:
    def __init__(self, nome, preco, estado, descricao, usuario):
        self.nome = nome
        self.preco = preco
        self.estado = estado
        self.descricao = descricao
        self.usuario = usuario

    def SalvarItem(self):
        """
            Salva o item atual no arquivo listadeitens.txt
        """
        from sistema import menu_global

        try:
            with open('listadeitens.txt', 'r', encoding='utf-8') as txt:
                linhas = txt.readlines()
            numeracoes = [
                int(linha.split('.')[1])
                for linha in linhas if '|' in linha and len(linha.split('|')) >= 5
            ]
            nova_numeracao = str(max(numeracoes) + 1) if numeracoes else '1'
        except FileNotFoundError:
            nova_numeracao = '1'

        with open('listadeitens.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'.{nova_numeracao}. {self.nome} | R${self.preco} | Estado (1 a 5): {self.estado} | {self.descricao} | Vendedor: {self.usuario}\n\n')
        console.print(Panel(f'✅ Item "{self.nome}" adicionado com sucesso!', border_style="green", width=60))
        time.sleep(1.5)
        menu_global.MenuPrincipal(self.usuario)




    @staticmethod
    def CarregarItens():
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
                    vendedor_info = partes[4].strip()
                    email_vendedor = ""
                    if vendedor_info.startswith('Vendedor:'):
                        email_vendedor = vendedor_info.replace('Vendedor:', '').strip()

                    item = Item(nome_e_numero, preco, estado, descricao, usuario= email_vendedor)  # Sem dono definido
                    itens.append(item)
        except FileNotFoundError:
           console.print(Panel("❌ Arquivo de itens não encontrado.", border_style="red", width=60))
        return itens

    @classmethod
    def LancarItem(cls, usuario):
        """
            Nessa função existe a possibilidade de lançar itens à listadeitens.txt.
            Para isso é necessário um nome, descrição, estado do item de 1 a 5 e preço.
            Após as entradas os dados são escritos no txt.        
        """
        from menu import Menu

        Menu.LimparTerminal()
        console.print(Panel('[bold white]Aqui você poderá lançar itens ao Bazar Brejó[/bold white]\n[cyan]Digite "cancelar" para sair a qualquer momento.[/cyan]', title= '[bold white]🛍️ LANÇAR ITEM[/bold white]', border_style='purple', width=60))
        nome = input('Nome do item: ').strip()
        if nome.lower() == 'cancelar':
            console.print(Align.center(Panel('❌ [red]Operação cancelada.[/red]', width=40, border_style='red')))
            time.sleep(1.5)
            return Menu().MenuPrincipal(usuario)
    
        descricao = input('Descrição do item: ').strip()
        if descricao.lower() == 'cancelar':
            console.print(Align.center(Panel('❌ [red]Operação cancelada.[/red]', width=40, border_style='red')))
            time.sleep(1.5)
            return Menu().MenuPrincipal(usuario)

        while True:
            tabela = (
                '1 - Péssimo\n'
                '2 - Ruim\n'
                '3 - Regular\n'
                '4 - Bom\n'
                '5 - Excelente'
            )
            console.print(Panel(tabela, title = '[bold white]GUIA DO ESTADO DE CONSERVAÇÃO[/bold white]', border_style = 'purple', width = 60))
            estado_input = input('Estado do item (1 a 5): ').strip()
            
            if estado_input.lower() == 'cancelar':
                console.print(Align.center(Panel('❌ [red]Operação cancelada.[/red]', width=40, border_style='red')))
                time.sleep(1.5)
                return Menu().MenuPrincipal(usuario)
        
            # Converter 
            if estado_input in ['1', '2', '3', '4', '5']:
                estados_dict = {
                    '1': 'Péssimo',
                    '2': 'Ruim',
                    '3': 'Regular',
                    '4': 'Bom',
                    '5': 'Excelente'
                }
                estado = estados_dict[estado_input]
                break
            else:
                console.print(Panel("❌ Estado inválido. Digite um número entre 1 e 5.", border_style="red", width=60))
                input('Pressione ENTER para tentar novamente')
        while True:
            console.print(Panel('💰 [bold yellow]Modelo de preço: R$ 20,00[/bold yellow]', width=50, border_style='purple'))
            try:
                preco_str = input('Digite o preço (ex: 15.50 ou 15,50): R$ ').strip().replace(',', '.')
                if preco_str.lower() == 'cancelar':
                    console.print(Align.center(Panel('❌ [red]Operação cancelada.[/red]', width=40, border_style='red')))
                    time.sleep(1.5)
                    return Menu().MenuPrincipal(usuario)
                preco = float(preco_str)
                if preco < 0:
                    console.print("[red]O preço não pode ser negativo.[/red]")
                    continue

                preco_formatado = f'{preco:.2f}'.replace('.', ',')
                break
            except ValueError:
                console.print(Panel("❌ Preço inválido. Digite um valor numérico, como 19.99", border_style="red", width=60))

        # Criar instância do item e salvar
        item = cls(nome, preco_formatado, estado, descricao, usuario)
        item.SalvarItem()

    @staticmethod
    def RemoverItemDoArquivo(nome_item):
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
            console.print(Panel("❌ Arquivo listadeitens.txt não encontrado.", border_style="red", width=60))


    @staticmethod
    def ComprarItens(usuario):
        """
            Mostra os itens disponíveis do txt e permite ao usuário comprar ou negociar.
            EM DESENVOLVIMENTO (pagamento)
        """
        from sistema import menu_global
        from menu import Menu
        from usuario import Usuario
        usuario_obj = Usuario()
        itens = Item.CarregarItens()

        if not itens:
            console.print(Panel("❌ Nenhum item disponível.", border_style="red", width=60))
            time.sleep(1.5)
            return menu_global.MenuPrincipal(usuario)
        
        console.print(Panel("[bold]Itens Disponíveis:[/bold]", title="🛒 COMPRAR ITEM", border_style="purple", width=60))

        for index, item in enumerate(itens, start=1):
            console.print(f" .{index}. {item.nome.ljust(35)} | R${item.preco}")
        console.print(' .[bold yellow]X[/bold yellow]. Voltar para o menu principal')

        while True:
            escolha = input('Escolha um produto (número) ou X para voltar: ').strip().lower()
            if escolha == 'x':
                return menu_global.MenuPrincipal(usuario)
            if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(itens):
                console.print(Panel("❌ Opção inválida.", border_style="red", width=60))
                continue

            index = int(escolha) - 1
            item_selecionado = itens[index]
            Menu.LimparTerminal()
            while True:
                console.print(Panel(f"[bold]{item_selecionado.nome}[/bold]\n[dim]{item_selecionado.descricao}\nEstado: {item_selecionado.estado}   Preço: R${item_selecionado.preco}", title="📦 DETALHES DO ITEM", border_style="purple", width=60))
                opcao = input('1 - Comprar\n2 - Negociar com o vendedor\n3 - Voltar\nOpção: ')
                if opcao == '1':
                    Menu.LimparTerminal()
                    while True:
                        console.print(Panel(f'Para comprar "{item_selecionado.nome}", faça o pix de R${item_selecionado.preco} para: [bold]704.514.384-26[/bold]', title="💰 PAGAMENTO", border_style="green", width=60))
                        confirmar = input('1. Confirmar compra\n2. Cancelar\nOpção: ')
                        if confirmar == '1':
                            console.print(Panel("📧 Email enviado! Venha para o Ceagri II para pegar seu item.", border_style="green", width=60))
                            # Registra no extrato
                            try:
                                preco_float = float(item_selecionado.preco.replace(',','.'))
                                usuario_obj.RegistrarCompra(item_selecionado.nome, preco_float)
                            except Exception as e:
                                console.print(Panel(f"Erro ao registrar no extrato: {e}", border_style="red", width=60))
                            # Remove do arquivo listadeitens.txt
                            try:
                                Item.RemoverItemDoArquivo(item_selecionado.nome)
                            except Exception as e:
                                console.print(Panel(f"Erro ao remover item: {e}", border_style="red", width=60))  
                            return menu_global.MenuPrincipal(usuario)    
                        elif confirmar == '2':
                            Menu.LimparTerminal()
                            console.print(Panel("Compra cancelada.", border_style="yellow", width=60))
                            break
                        else:
                            Menu.LimparTerminal()
                            console.print(Panel("❌ Opção inválida.", border_style="red", width=60))
                    break
                elif opcao == '2':
                    Item.Negociar(usuario, item_selecionado)
                    break
                elif opcao == '3':
                    Menu.LimparTerminal()
                    menu_global.MenuPrincipal(usuario)
                    break
                else:
                    Menu.LimparTerminal()
                    console.print(Panel("❌ Opção inválida.", border_style="red", width=60))
            break

    @staticmethod
    def Negociar(usuario, item):
        """
            Permite negociar com o vendedor.
        """
        from sistema import menu_global
        from menu import Menu
        from usuario import Usuario

        console.print(Panel("Deseja negociar com o vendedor?", title="📨 NEGOCIAR", border_style="purple", width=60))
        print('1 - Escrever email\n2 - Ver contato\n3 - Voltar')
        assunto = 'Um cliente do Bazar Brejó quer negociar com você!'

        usuario_obj = Usuario()

        while True:
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                mensagem = input('Mensagem para o vendedor: ')
                while True:
                    print('1 - Editar mensagem\n2 - Enviar\n3 - Cancelar')
                    editar = input('Opção: ')
                    if editar == '1':
                        print('Mensagem atual:', mensagem)
                        mensagem = input('Nova mensagem: ')
                    elif editar == '2':
                        Menu.LimparTerminal()
                        try:
                            usuario_obj.EnviarEmail(destinatario1=item.usuario.email, destinatario2=None, destinatario3=None, assunto=assunto, conteudo=mensagem)
                            console.print(Panel("✅ Mensagem enviada! Uma cópia foi enviada ao seu e-mail.", border_style="green", width=60))
                        except Exception:
                            console.print(Panel("❌ Erro ao enviar mensagem.", border_style="red", width=60))
                        return
                    elif editar == '3':
                        Menu.LimparTerminal()
                        return menu_global.MenuConfig(usuario)
                    else:
                        console.print(Panel("❌ Opção inválida.", border_style="red", width=60))
            elif opcao == '2':
                Menu.limpar_terminal()
                console.print(Panel("📱 Número de telefone do vendedor: [em desenvolvimento]", border_style="yellow", width=60))
                if input('Digite X para voltar: ').strip().upper() == 'X':
                    return menu_global.MenuPrincipal(usuario)
            elif opcao == '3':
                Menu.LimparTerminal()
                return menu_global.MenuPrincipal(usuario)
            else:
                console.print(Panel("❌ Opção inválida.", border_style="red", width=60))
