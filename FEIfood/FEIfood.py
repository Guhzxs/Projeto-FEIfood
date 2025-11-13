import os

# ==========================
# CABEÇALHO VISUAL
# ==========================
def exibir_cabecalho():
    """Mostra a mensagem inicial do programa."""
    titulo = "▶ BEM-VINDO AO FEIFOOD "
    largura = 60
    print("\n" + "=" * largura)
    print(titulo.center(largura))
    print("=" * largura)
    print("\nÉ um prazer ter você conosco!")

exibir_cabecalho()

# ==========================
# CONSTANTES DE ARQUIVOS
# ==========================
ARQUIVO_USUARIOS = "FEIfood.txt"
ARQUIVO_ALIMENTOS = "alimentos.txt"
ARQUIVO_PEDIDOS = "pedidos.txt"

# ==========================
# FUNÇÕES GENÉRICAS DE ARQUIVO
# ==========================
def ler_arquivo(nome):
    """Lê todas as linhas de um arquivo e retorna como lista."""
    try:
        with open(nome, "r", encoding="utf-8") as arq:
            return arq.readlines()
    except FileNotFoundError:
        return []

def salvar_arquivo(nome, linhas):
    """Sobrescreve um arquivo com as linhas fornecidas."""
    with open(nome, "w", encoding="utf-8") as arq:
        arq.writelines(linhas)

# Cria o arquivo de usuários se não existir
if not os.path.exists(ARQUIVO_USUARIOS):
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        f.write("\n")

# ==========================
# USUÁRIOS (CADASTRO / LOGIN)
# ==========================
def salvar_cadastro(usuario):
    """Salva um novo usuário no arquivo de cadastro."""
    linha = "|".join(usuario.values()) + "\n"
    salvar_arquivo(ARQUIVO_USUARIOS, ler_arquivo(ARQUIVO_USUARIOS) + [linha])
    print(usuario)

def verifica_login(usuario_digitado, senha_digitada):
    """Verifica se login e senha existem no arquivo de usuários."""
    for linha in ler_arquivo(ARQUIVO_USUARIOS):
        dados = linha.strip().split("|")
        if len(dados) >= 4:
            if dados[0].lower() == usuario_digitado.lower() and dados[3] == senha_digitada:
                return True
    return False

# ==========================
# ALIMENTOS (CARDÁPIO / BUSCA)
# ==========================
def carregar_alimentos():
    """Carrega todos os alimentos do arquivo e retorna lista de dicionários."""
    alimentos = []
    for linha in ler_arquivo(ARQUIVO_ALIMENTOS):
        dados = linha.strip().split("|")
        if len(dados) >= 5:
            alimentos.append({
                "Código": dados[0],
                "Nome": dados[1],
                "Categoria": dados[2],
                "Preco": float(dados[3]),
                "Descricao": dados[4]
            })
    return alimentos

def buscar_alimentos():
    """Permite buscar alimentos pelo nome digitado pelo usuário."""
    alimentos = carregar_alimentos()
    if not alimentos:
        print("Nenhum alimento cadastrado.")
        return
    while True:
        termo = input("\nDigite o nome do alimento que deseja buscar (ou 0 para sair): ")
        if termo == "0":
            print("\nEncerrando busca de alimentos e retornando ao menu principal..")
            break
        resultados = [a for a in alimentos if termo.lower() in a["Nome"].lower()]
        exibir_alimentos(resultados)

def exibir_alimentos(lista):
    """Mostra os alimentos encontrados em formato bonito."""
    if not lista:
        print("Nenhum alimento encontrado")
        return
    largura = 75
    titulo = "RESULTADOS DA BUSCA"
    print("\n" + "=" * largura)
    print(titulo.center(largura))
    print("=" * largura)
    for alimento in lista:
        print(f"Código   : {alimento['Código']}")
        print(f"Nome     : {alimento['Nome']}")
        print(f"Categoria: {alimento['Categoria']}")
        print(f"Preço    : R${alimento['Preco']:.2f}")
        print(f"Descrição: {alimento['Descricao']}")
        print("-" * largura)
    print("=" * largura)

def buscar_por_codigo(codigo):
    """Retorna o nome do alimento dado um código."""
    for linha in ler_arquivo(ARQUIVO_ALIMENTOS):
        partes = linha.strip().split("|")
        if len(partes) >= 2 and partes[0] == codigo:
            return partes[1]
    return None

def exibir_cardapio():
    """Mostra todos os alimentos cadastrados em formato de tabela."""
    alimentos = carregar_alimentos()
    if not alimentos:
        print("\nCardápio não encontrado.")
        return

    titulo = "▶ CARDÁPIO COMPLETO "
    largura_total = 137 # largura fixa da tabela

    print("=" * largura_total)
    print(titulo.center(largura_total))
    print("=" * largura_total)

    # Cabeçalho com larguras fixas
    cabecalho = f"{'Código':<6} | {'Nome':<30} | {'Categoria':<12} | {'Preço':<8} | {'Descrição'}"
    print(cabecalho.ljust(largura_total))
    print("-" * largura_total)

    # Linhas
    for a in alimentos:
        linha = f"{a['Código']:<6} | {a['Nome']:<30} | {a['Categoria']:<12} | R${a['Preco']:6.2f} | {a['Descricao']}"
        print(linha.ljust(largura_total))

    print("=" * largura_total)

# ==========================
# PEDIDOS
# ==========================
def gerar_id():
    """Gera um novo ID de pedido sequencial."""
    maior_id = 1000
    for linha in ler_arquivo(ARQUIVO_PEDIDOS):
        partes = linha.strip().split("|")
        if partes and partes[0].isdigit():
            id_atual = int(partes[0])
            if id_atual > maior_id:
                maior_id = id_atual
    return maior_id + 1

def criar_pedidos(nome_usuario):
    """Cria um novo pedido vazio para o usuário."""
    id_pedido = gerar_id()
    linha = f"{id_pedido}|{nome_usuario}||-\n"
    salvar_arquivo(ARQUIVO_PEDIDOS, ler_arquivo(ARQUIVO_PEDIDOS) + [linha])
    return id_pedido

def carregar_pedidos():
    """Carrega todos os pedidos do arquivo."""
    return ler_arquivo(ARQUIVO_PEDIDOS)

def salvar_pedidos(pedidos):
    """Salva a lista de pedidos no arquivo."""
    salvar_arquivo(ARQUIVO_PEDIDOS, pedidos)

def linha_para_pedido(linha):
    """Converte uma linha em dicionário de pedido."""
    id_pedido, usuario, itens, avaliacao = linha.strip().split("|")
    return {"id": int(id_pedido), "usuario": usuario,
            "itens": itens.split(",") if itens else [], "avaliacao": avaliacao}

def pedido_para_linha(pedido):
    """Converte um dicionário de pedido em linha de arquivo."""
    itens = ",".join(pedido["itens"])
    return f"{pedido['id']}|{pedido['usuario']}|{itens}|{pedido['avaliacao']}\n"

def exibir_pedido_formatado(linha):
    """Mostra um pedido formatado."""
    pedido = linha_para_pedido(linha)
    largura = 60
    titulo = f"PEDIDO #{pedido['id']}"
    print("\n" + "=" * largura)
    print(titulo.center(largura))
    print("=" * largura)
    print(f"Usuário: {pedido['usuario']}")
    print("-" * largura)
    print("Carrinho atual:")
    if pedido["itens"]:
        for item in pedido["itens"]:
            print(f"  • {item}")
    else:
        print("  (Nenhum item no carrinho)")
    print("-" * largura)
    print(f"Avaliação: {pedido['avaliacao']}")
    print("=" * largura)

def editar_itens_pedido(pedido):
    """Permite adicionar ou remover itens de um pedido."""
    cardapio_exibido = False #flag para controlar a exibição do cardápio
    while True:
        print("O que deseja fazer hoje?")
        print("\n[1] - Adicionar item\n[2] - Remover item\n[0] - Finalizar edição\n")
        escolha = input("Digite sua opção: ")
        if escolha == "0":
            break
        elif escolha == "1":
            if not cardapio_exibido:   
                print("\n" + "." * 137 + "\n")  # separador visual pois estava bugando meu terminal 
                exibir_cardapio()
                cardapio_exibido = True

            codigo = input("Digite o código do item (ou 0 para cancelar): ")
            if codigo == "0": 
                continue
            alimento = buscar_por_codigo(codigo)
            if alimento:
                pedido["itens"].append(alimento)
                print(f"\n- {alimento} adicionado ao carrinho.")
            else:
                print("Código inválido.")
        elif escolha == "2":
            if not pedido["itens"]:
                print("Nenhum item para remover.")
                continue

            print("\nItens no carrinho:")
            print("=" * 40)
            for idx, item in enumerate(pedido["itens"]):
                print(f"\n[{idx}] {item}")
            print("=" * 40)

            remover = input("Digite o índice do item (ou 0 para cancelar): ")
            if remover == "0":
                continue
            elif remover.isdigit() and int(remover) < len(pedido["itens"]):
                removido = pedido["itens"].pop(int(remover))
                print(f"- {removido} removido.")
            else:
                print("Índice inválido.")
        else:
            print("Opção inválida. Digite 1, 2 ou 0.")

def atualizar_pedido(usuario_login):
    """Atualiza um pedido existente (adicionar/remover itens)."""
    id_atualizar = int(input("Digite o ID do pedido que deseja atualizar: "))
    pedidos = carregar_pedidos()
    for i, linha in enumerate(pedidos):
        pedido = linha_para_pedido(linha)
        if pedido["id"] == id_atualizar:
            exibir_pedido_formatado(linha)
            editar_itens_pedido(pedido)
            pedidos[i] = pedido_para_linha(pedido)
            salvar_pedidos(pedidos)
            print("\nPedido atualizado com sucesso!")
            exibir_pedido_formatado(pedidos[i])
            menu_pos_pedido(usuario_login, pedidos[i])
            return
    print("Pedido não encontrado.")

def excluir_pedido():
    """Exclui um pedido pelo ID."""
    id_apagar = int(input("Digite o ID do pedido que deseja apagar: "))
    pedidos = carregar_pedidos()
    for i, linha in enumerate(pedidos):
        partes = linha.strip().split("|")
        if len(partes) != 4:
            continue
        id_pedido, usuario, alimento, avaliacao = partes
        if id_apagar == int(id_pedido):
            exibir_pedido_formatado(linha)
            resposta = input("\nTem certeza que deseja excluir este pedido? (s/n): ")
            if resposta.lower() == "s":
                pedidos.pop(i)
                salvar_pedidos(pedidos)
                print("\nPedido excluído com sucesso!")
            else:
                print("\nPedido não foi alterado.")
            return
    print("Pedido não encontrado.")

def avaliar_pedido():
    """Permite avaliar um pedido já realizado."""
    id_avaliar = int(input("Digite o ID do pedido que deseja avaliar: "))
    pedidos = carregar_pedidos()
    for i, linha in enumerate(pedidos):
        pedido = linha_para_pedido(linha)
        if pedido["id"] == id_avaliar:
            nota = input("Digite a nota (0 a 5): ")
            while nota not in ["0","1","2","3","4","5"]:
                nota = input("Nota inválida. Digite entre 0 e 5: ")
            pedido["avaliacao"] = nota
            pedidos[i] = pedido_para_linha(pedido)
            salvar_pedidos(pedidos)
            print("Pedido avaliado com sucesso.")
            return
    print("Pedido não encontrado.")

def menu_pos_pedido(usuario_login, linha_pedido):
    """Menu de finalização do pedido: pagamento, endereço e avaliação."""
    print("\nTodos os itens adicionados com sucesso!")
    print("O que deseja fazer agora? ")

    while True:
        print("\n[1] - Finalizar pedido")
        print("[2] - Voltar ao menu principal\n")

        decisao = input("Digite sua opção: ")

        if decisao == "1":
            print("\nEscolha a forma de pagamento:\n")
            print("[1] - Pix")
            print("[2] - Cartão de crédito/débito")
            print("[3] - Dinheiro")

            pagamento = input("\nDigite o índice da forma de pagamento desejada: ")
            if pagamento == "1":
                forma = "Pix"
            elif pagamento == "2":
                forma = "Cartão de crédito/débito"
            else:
                forma = "Dinheiro"

            endereco = input("\nDigite o endereço para entrega: ").strip()
            while not endereco:
                print("Endereço é um campo obrigatório.")
                endereco = input("Digite o endereço para entrega: ").strip()

            largura = 70
            titulo = "RESUMO FINAL DO PEDIDO"

            print("\n" + "=" * largura)
            print(titulo.center(largura))
            print("=" * largura)

            # Exibe os dados do pedido formatados
            id_pedido, usuario, alimento, avaliacao = linha_pedido.strip().split("|")

            print(f"ID do Pedido : {id_pedido}")
            print(f"Usuário      : {usuario}")
            print("-" * largura)
            print("Carrinho atual:")

            itens = alimento.split(",") if alimento else []
            if itens and itens[0]:
                for item in itens:
                    print(f"  • {item}")
            else:
                print("  (Nenhum item no carrinho)")

            print("-" * largura)
            print(f"Avaliação    : {avaliacao}")
            print("-" * largura)
            print(f"Forma de pagamento : {forma}")
            print(f"Endereço de entrega: {endereco}")
            print("=" * largura)

            print("\nSeu pedido foi finalizado com sucesso!")
            print("Ele chegará em até 40 minutos.")
            print("\nObrigado por escolher o FEIfood.")
            print("=" * largura)

            # avaliação do pedido
            avaliar = input("\nDeseja avaliar seu pedido agora? (s/n): ").strip().lower()
            if avaliar == "s":
                nota = input("Digite a nota de avaliação (0 a 5): ").strip()
                while nota not in ["0", "1", "2", "3", "4", "5"]:
                    print("Nota inválida. Digite uma nota entre 0 e 5.")
                    nota = input("Digite a nota de avaliação (0 a 5): ").strip()

                id_pedido, usuario, alimento, _ = linha_pedido.strip().split("|")
                linha_pedido_avaliada = f"{id_pedido}|{usuario}|{alimento}|{nota}\n"
                pedidos = carregar_pedidos()
                for i, linha in enumerate(pedidos):
                    if linha.startswith(f"{id_pedido}|"):
                        pedidos[i] = linha_pedido_avaliada
                        break

                salvar_pedidos(pedidos)
                print("Obrigado por sua avaliação! Retornando ao menu inicial...")
                return menu_inicial()
            
            elif avaliar == "n":
                print("Não esqueça de avaliar seu pedido mais tarde!")
                break

            else:
                print("Opção inválida! Digite apenas 's' para sim ou 'n' para não.")
        elif decisao == "2":
            return
        else:
            print("Opção inválida! Digite 1 ou 2.")
        


def novo_pedido(usuario_login):
    """Cria um novo pedido e permite apenas adicionar itens, depois finaliza ou volta ao menu inicial."""
    exibir_cardapio()

    # cria pedido vazio
    id = criar_pedidos(usuario_login)
    print(f"\nPedido criado com sucesso! O ID do seu pedido é: {id}")

    pedidos = carregar_pedidos()
    for i, linha in enumerate(pedidos):
        pedido = linha_para_pedido(linha)
        if pedido["id"] == id:
            # fluxo de adicionar itens
            while True:
                codigo = input("\nDigite o código do item para adicionar (ou 0 para finalizar): ")
                if codigo == "0":
                    break
                alimento = buscar_por_codigo(codigo)
                if alimento:
                    pedido["itens"].append(alimento)
                    print(f"- {alimento} adicionado ao carrinho.")
                else:
                    print("Código inválido.")

            # salva pedido
            pedidos[i] = pedido_para_linha(pedido)
            salvar_pedidos(pedidos)

            # mostra resumo
            exibir_pedido_formatado(pedidos[i])

            # chama menu de finalização
            menu_pos_pedido(usuario_login, pedidos[i])
            return

# ==========================
# MENUS
# ==========================
def exibir_menu(titulo, opcoes):
    """Mostra um menu genérico com título e opções."""
    largura = 50
    print("\n" + "=" * largura)
    print(titulo.center(largura))
    print("=" * largura)
    for chave, texto in opcoes.items():
        print(f"| [{chave}] - {texto.ljust(largura-9)}|")
    print("=" * largura)

def menu_pos_login(usuario_login):
    """Menu principal após login."""
    opcoes = {
        "1": "Fazer novo pedido",
        "2": "Atualizar pedido",
        "3": "Excluir pedido",
        "4": "Avaliar pedido",
        "5": "Buscar alimentos",
        "6": "Sair"
    }
    funcoes = {
        "1": lambda: novo_pedido(usuario_login),
        "2": lambda: atualizar_pedido(usuario_login),
        "3": excluir_pedido,
        "4": avaliar_pedido,
        "5": buscar_alimentos,
        "6": lambda: print("\nSaindo da guia de pedidos e retornando ao menu inicial...")
    }
    while True:
        exibir_menu("MENU PRINCIPAL", opcoes)
        escolha = input("Digite sua opção: ")

        if escolha == "6":
                funcoes["6"]()
                break
        else:

            funcao = funcoes.get(escolha)
            if funcao:
                funcao()
            else:
                print("Opção inválida! Digite de 1 a 6.")

def fazer_login():
    """Realiza login do usuário."""
    usuario_login = input("Nome de usuário: ")
    senha_login = input("Digite sua senha: ")
    if verifica_login(usuario_login, senha_login):
        print(f"\nLogin bem sucedido! Que bom te ver novamente {usuario_login}.")
        menu_pos_login(usuario_login)
    else:
        print("\nNome de usuário ou senha incorretos. Tente novamente.")

def realizar_cadastro():
    """Realiza cadastro de novo usuário."""
    usuario = {
        "Nome de usuário": input("Nome de usuário: "),
        "CPF": input("CPF: "),
        "Data de Nascimento": input("Data de Nascimento(00/00/0000): "),
        "Senha": input("Senha: ")
    }
    salvar_cadastro(usuario)
    print("\nCadastro realizado com sucesso! Faça o seu login.")

def sair_programa():
    """Finaliza o programa."""
    print("Obrigado(a) por usar o FEIfood. Até a próxima!")
    exit()

def menu_inicial():
    """Menu inicial do programa."""
    opcoes = {
        "1": "Fazer Login",
        "2": "Realizar Cadastro",
        "3": "Sair do programa"
    }
    funcoes = {
        "1": fazer_login,
        "2": realizar_cadastro,
        "3": sair_programa
    }
    while True:
        exibir_menu("MENU INICIAL", opcoes)
        escolha = input("Digite sua opção: ")
        funcao = funcoes.get(escolha)
        if funcao:
            funcao()
        else:
            print("Opção inválida! Digite 1, 2 ou 3.")

# ==========================
# INÍCIO DO PROGRAMA
# ==========================
menu_inicial()

