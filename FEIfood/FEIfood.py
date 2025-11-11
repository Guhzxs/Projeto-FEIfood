import os

#aspecto visual do início do projeto
nome_projeto = "FEIfood"
separador = "-" * len(nome_projeto)
cabecalho = separador + "\n" + nome_projeto + "\n" + separador

print(cabecalho)
print("Seja bem vindo(a) ao FEIfood! É um prazer ter você conosco.")
print()

#arquivos utilizados no projeto 
nome_arquivo = "FEIfood.txt"
arquivo_alimentos = "alimentos.txt"
arquivo_pedidos = "pedidos.txt"


#criação do meu arquivo que funcionará como banco de dados
if not os.path.exists(nome_arquivo):
    arquivo_cadastro = open(nome_arquivo, 'w+t' , encoding="utf-8")      #cria o arquivo
    arquivo_cadastro.write(cabecalho)
    arquivo_cadastro.write("\n")
    arquivo_cadastro.close()

#armazenando o cadastro dos usuários
def salvar_cadastro(usuario):
    valores_lista = list(usuario.values())       #transformando o dicionário em uma lista contínua com separador
    linha_texto = "|".join(valores_lista) + "\n"      #separador
    with open(nome_arquivo, 'a', encoding="utf-8") as arquivo_cadastro:         #adicionando o cadastro no arquivo
        arquivo_cadastro.write(linha_texto)
    print(usuario)

#verificando se o login já existe
def verifica_login(usuario_digitado, senha_digitada):
    try:
        with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:       #abre o arquivo em modo leitura ('r')
            contador = 0
            for linha in arquivo:
                if contador < 4:       #pula as 4 primeiras linhas, pois lá está o nosso cabeçalho
                    contador += 1
                    continue
                linha_limpa = linha.strip()        # Remove espaços em branco e quebras de linha no início e fim da linha
                if linha_limpa:       # Verificando se a linha não está vazia

                    dados_salvos = linha_limpa.split('|') # Divide a linha em uma lista de dados usando o '|' como separador

                    if len(dados_salvos) >= 4:      # Garante que a linha possui os 4 campos de dados esperados
                        usuario_salvo = dados_salvos[0]    # O nome de usuário está na posição 0
                        senha_salva = dados_salvos[3]      # A senha está na posição 3

                        if usuario_salvo == usuario_digitado and senha_salva == senha_digitada:        # Compara o login digitado com o login salvo
                            return True
            return False             # Se o loop terminar sem encontrar uma correspondência, retorna falha
    
    except FileNotFoundError:
        print("Faça seu cadastro para que possa realizar o login")
        return False
    

def buscar_alimentos(alimento_desejado):
    try:
        resultados_alimentos = []
        with open(arquivo_alimentos, 'r') as arquivo_a:
            for alimento_encontrado in arquivo_a:
                alimento_limpo = alimento_encontrado.strip()
                if alimento_limpo:
                    dados_alimentos = alimento_limpo.split(',')

                    if len(dados_alimentos) >= 4:
                        if alimento_desejado.lower() in dados_alimentos[0].lower():
                            alimentos = {
                                "Nome": dados_alimentos[0],
                                "Categoria": dados_alimentos[1],
                                "Preco": float(dados_alimentos[2]),
                                "Descricao": dados_alimentos[3]
                            }
                            resultados_alimentos.append(alimentos)
            return resultados_alimentos

    except FileNotFoundError:
        print("Registo de alimentos não encontrado. Digite uma opção do cardápio")
        return False
        
def exibir_alimentos(lista):
    if not lista:
        print("Nenhum alimento encontrado")
        return
    for alimento in lista:
        print(f"Nome: {alimento['Nome']}")
        print(f"Categoria: {alimento['Categoria']}")
        print(f"Preço: {alimento['preco']:.2f}")
        print(f"Descrição: {alimento['Descricao']}")
        print("-" * 40)

def gerar_id ():
    maior_id = 1000
    try:
        with open(arquivo_pedidos, 'r') as arquivo_p:
            for linha in arquivo_p:
                partes = linha.strip().split("|")
                if partes and partes[0].isdigit():
                    id_atual = int(partes[0])
                    if id_atual > maior_id:
                        maior_id = id_atual
    except FileNotFoundError:
        pass #se o arquivo não existir começa do 0 

    return maior_id + 1

def criar_pedidos(nome_usuario):
    with open(arquivo_pedidos, 'a') as arquivo_p:
        id_pedido = gerar_id()
        itens = []
        avaliacao = "-"
        formatacao = ",".join(itens)
        linha_pedido = f"{id_pedido}|{nome_usuario}|{formatacao}|{avaliacao}\n"
        arquivo_p.write(linha_pedido)
        return id_pedido

def carregar_pedidos():
    try:
        with open("pedidos.txt", 'r') as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        return []
    
def salvar_pedidos(pedidos):
    with open("pedidos.txt", "w") as arquivo:
        arquivo.writelines(pedidos)

def validar_codigo(codigo):
    return buscar_por_codigo(codigo) is not None

def exibir_pedido_formatado(linha):
    id_pedido, usuario, alimento, avaliacao = linha.strip().split("|")
    print("\nPedido Encontrado:")
    print(f"- ID do Pedido: {id_pedido}")
    print(f"- Usuário: {usuario}")
    print("- Carrinho atual:")
    for item in alimento.split(","):
        print(f"  •  {item}")
    print(f"- Avaliação: {avaliacao}")
    print("-" * 40)

def atualizar_pedido(usuario_login):
    print("Atualizar pedido:")
    id_atualizar = int(input("Digite o ID do pedido que deseja atualizar: "))
    pedidos = carregar_pedidos()

    # Procura o pedido no arquivo
    for i, linha in enumerate(pedidos): # Para cada índice e linha no conteúdo do arquivo 
        partes = linha.strip().split("|") # Divide a linha em partes, separando pelo separador 
        if len(partes) != 4:
            continue
        id_pedido, usuario, alimento, avaliacao = partes
        if id_atualizar == int(id_pedido): # Verifica se o id procurado é igual ao id_pedido
            # Imprime os dados do pedido encontrado
            exibir_pedido_formatado(linha)

            # Atualiza os dados do pedido
            lista = alimento.split(",") if alimento else []

            while True: # Permite adicionar múltiplos itens até digitar 0
                codigo = input("Digite o novo item que deseja adicionar ao carrinho (ou 0 para finalizar): ")
                if codigo == "0":
                    break

                novo_alimento = buscar_por_codigo(codigo) # Busca o nome do alimento pelo código

                if not novo_alimento:
                    print("Código não encontrado no cardápio.") # Mensagem de erro se o código não existir
                else:
                    lista.append(novo_alimento) # Adiciona o novo alimento à lista
                    print(f"- {novo_alimento} adicionado ao carrinho.") # Confirmação de adição

            alimento_atualizado = ",".join(lista) # Junta os itens em uma única string
            pedidos[i] = f"{id_pedido}|{usuario}|{alimento_atualizado}|{avaliacao}\n" # Atualiza a linha do pedido
            salvar_pedidos(pedidos) 

            print("\n Pedido atualizado com sucesso:")
            exibir_pedido_formatado(pedidos[i])
            menu_pos_pedido(usuario_login, pedidos[i])
            return
            
    # Se não encontrar o pedido
        print("Pedido não encontrado.") # Mensagem de erro se o pedido não for encontrado
    

def excluir_pedido():
    id_apagar = int(input("Digite o ID do pedido que deseja apagar: "))
    pedidos = carregar_pedidos()
        # Procura o pedido no arquivo
    for i, linha in enumerate(pedidos):
        partes = linha.strip().split("|")
        if len(partes) != 4:
            continue
        id_pedido, usuario, alimento, avaliacao = partes

        if id_apagar == int(id_pedido):
            print(f"\nPedido encontrado: ")
            exibir_pedido_formatado(linha)

            resposta = input("\nTem certeza que deseja excluir este pedido? (s/n)")
            if resposta == "s".upper():
                # Remove o pedido da lista
                pedidos.pop(i)
                salvar_pedidos(pedidos)
                print("\nPedido excluído com sucesso!")
                return
            else:
                print("\nPedido não foi alterado. Voltando ao menu de funções.")
                return
        # Se não encontrar o pedido
    print("Pedido não encontrado.")

def excluir_item_pedido(usuario_login):
    id_alterar = int(input("Digite o ID do pedido que deseja alterar: "))
    pedidos = carregar_pedidos()

    for i, linha in enumerate(pedidos):
        partes = linha.strip().split("|")
        if len(partes) != 4:
            continue
        id_pedido, usuario, alimento, avaliacao = partes

        if id_alterar == int(id_pedido):
            print(f"\nPedido encontrado: ")
            exibir_pedido_formatado(linha)

            lista = alimento.split(",") if alimento else[]
            while True:
                print(f"\nItens do pedido:")
                for idx, item in enumerate(lista):
                    print(f"[{idx}] {item}")
                remover = input("\nDigite o código do item que deseja remover (Ou 0 caso tenha terminado de editar): ")
                if remover == "0":
                    break
                elif remover.isdigit() and int(remover) < len(lista):
                    item_removido = lista.pop(int(remover))
                    print(f"\n- {item_removido} removido do pedido {id_pedido}.")
                else:
                    print("Índice inválido. Tente novamente.")

            alimento_atualizado = ",".join(lista)
            pedidos[i] = f"{id_pedido}|{usuario}|{alimento_atualizado}|{avaliacao}\n"
            salvar_pedidos(pedidos)

            print("\nPedido atualizado após remoção:")
            exibir_pedido_formatado(pedidos[i])
            menu_pos_pedido(usuario_login, pedidos[i])
            return

    print("Pedido não encontrado.")


def menu_pos_pedido(usuario_login, linha_pedido):

    print("\nTodas as alterações feitas com sucesso!")
    print("O que deseja fazer agora? ")

    print("\n[1] -  Finalizar pedido")
    print("[2] - Voltar ao menu principal\n")

    decisao = int(input("Digite o que deseja fazer: "))

    if decisao == 1:
        print("\nEscolha a forma de pagamento:")
        print("[1] - Pix")
        print("[2] - Cartão de crédito/débito")
        print("[3] - Dinheiro")

        pagamento = int(input("\nDigite o indice da forma de pagamento desejada: "))
        if pagamento == 1:
            print("\nMetódo de pagamento escolhido: [Pix]")
            forma = "Pix"
        elif pagamento == 2:
            print("\nMetódo de pagamento escolhido: [Cartão de crédito/débito]")
            forma = "Cartão de crédito/débito"
        else:
            print("\nMétodo de pagamento escolhido: [Dinheiro]")
            forma = "Dinheiro"

        endereco = input("\nDigite o endereço para entrega: ").strip()
        while not endereco:
            print("Endereço é um campo obrigatório.")
            endereco = input("Digite o endereço para entrega: ").strip()

        print("Resumo final:")
        exibir_pedido_formatado(linha_pedido)
        print(f"\n- Forma de pagamento: {forma}")
        print(f"- Endereço de entrega: {endereco}")
        print(f"\nSeu pedido foi finalizado com sucesso!")
        print("Ele chegará em até 40 minutos. Obriagdo por escolher o FEIfood.")
        print("\nRetornando ao menu inicial...")
        menu_inicial()
    else: 
        menu_pos_login(usuario_login)
        
    

        
            
    

def avaliar_pedido(usuario_login):
    id_avaliar = int(input("Digite o ID do pedido que deseja avaliar: "))
    nota = input("Digite a nota de avaliação (0 a 5): ").strip()
    if nota not in ["0", "1", "2", "3", "4", "5"]:
        print("Nota inválida. Digite uma nota entre 0 e 5.")
        return
    

    pedidos = carregar_pedidos()
    for i, linha in enumerate(pedidos):
        id_pedido, usuario, alimento, _ = linha.split("|")
        if id_avaliar == int(id_pedido):
            print(f"Pedido encontrado: {linha.strip()}")
            pedidos[i] = f"{id_pedido}|{usuario}|{alimento}|{nota}\n"
            salvar_pedidos(pedidos)
            print("Pedido avaliado com sucesso. Obrigado por nos avaliar.")
            return
    print("Pedido não encontrado.")


# def adicionar_item_pedido(id_pedido, item):
#     pedidos = carregar_pedidos()

#     for i, linha in enumerate(pedidos):
#         id_atual, usuario, alimento, avaliacao = linha.strip().split("|")
#         if int(id_atual) == id_pedido:
#             lista = alimento.split(",") if alimento else []
#             lista.append(item)
#             alimento_atualizado = ",".join(lista)
#             pedidos[i] = f"{id_atual}|{usuario}|{alimento_atualizado}|{avaliacao}\n"
#             salvar_pedidos(pedidos)
#             print(f"{item} adicionado ao seu pedido com sucesso.")
#             return
#         print("Pedido não encontrado.")

def buscar_por_codigo(codigo):
    try: 
        with open(arquivo_alimentos, 'r', encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split("|")
                if len(partes) >= 2 and partes[0] == codigo:
                    return partes [1]
    except FileNotFoundError:
        print("Arquivo de alimentos não encontrado.")
    return None
    
def exibir_cardapio():
    try:
        with open(arquivo_alimentos, 'r', encoding='utf-8') as arquivo:
            print("\n CARDÁPIO COMPLETO")
            print("-" * 40)

            for linha in arquivo:
                codigo, nome, categoria, preco, descricao = linha.strip().split("|")
                print(f"Código: {codigo}")
                print(f"Nome: {nome}")
                print(f"Catgeoria: {categoria}")
                print(f"Preço: {float(preco):.2f}")
                print(f"Descrição: {descricao}") 
                print("-" * 40)
    except FileNotFoundError:
        print("\nCardápio não encontrado.")


def menu_pos_login (usuario_login):
    while True:
        print("\nO que você deseja fazer hoje?")
        print("[1] - Fazer novo pedido")
        print("[2] - Atualizar pedido")
        print("[3] - Excluir pedido")
        print("[4] - Sair")

        escolha = input("Digite sua opção: ")

        if escolha == "1":
            exibir_cardapio()
            id = criar_pedidos(usuario_login)
            print(f"\nPedido criado, o ID do seu pedido é: {id}")
            print("\nAgora vamos adicionar os itens ao seu pedido.")
            atualizar_pedido()  
            print("\nPedido finalizado!")

        elif escolha == "2":
            atualizar_pedido()
        elif escolha == "3":
            excluir_pedido()
        elif escolha == "4":
            print("\nSaindo da guia de pedidos e retornado ao menu inicial...")
            break
        else:
            print("\nOpção inválida. Digite o que você deseja fazer hoje (0 a 4): ")


def menu_inicial():
    while True:

        #menu
        print("\nEscolha uma opção:")
        print("[1] - Fazer Login")
        print("[2] - Realizar Cadastro")
        print("[3] - Sair do programa\n")
        try:
            opcao = int(input("Digite sua opção: "))
        except ValueError:
            error_msg = "Opção inválida! Digite as opções do menu (1, 2 ou 3)."
            print(error_msg)
            continue
        if opcao == 1:
            
            usuario_login = input("Nome de usuário: ")
            senha_login = input("Digite sua senha: ")

            if verifica_login(usuario_login,senha_login):
                print(f"\nLogin bem sucedido! Que bom te ver novamente {usuario_login}.")
                menu_pos_login(usuario_login)

            else:
                print("\nNome de usuário ou senha incorretos. Tente novamente.")
        elif opcao == 2:
        #cadastro
            usuario = {
                "Nome de usuário": "",
                "CPF": "",
                "Data de Nascimento": "",
                "Senha": ""
            }

            print("Digite os campos abaixo para realizar o seu cadastro:")
            for chave in usuario:
                usuario[chave] = input(chave + ": ")
        
            salvar_cadastro(usuario)
            print("Cadastro realizado com sucesso! Faça login.")
        elif opcao == 3:
            print("Obrigado(a) por usar o FEIfood. Até a próxima!")
            break
        else:
            print(error_msg)


menu_inicial()