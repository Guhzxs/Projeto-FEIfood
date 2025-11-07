import os

#aspecto visual do início do projeto
nome_projeto = "FEIfood"
separador = "-" * len(nome_projeto)
cabecalho = separador + "\n" + nome_projeto + "\n" + separador

print(cabecalho)
print("Seja bem vindo(a) ao FEIfood! É um prazer ter você conosco.")
print()

nome_arquivo = "FEIfood.txt"

nome_arquivo2 = "restaurantes.txt"

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
                if contador < 2:       #pula as 2 primeiras linhas, pois lá está o nosso cabeçalho
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
    
def buscar_alimento(nome_alimento, arquivo = nome_arquivo2):

    encontrados = []
    try:
        with open (arquivo, 'r', encoding= "utf-8") as f:
            for linha in f:
                dados = linha.strip().split("|")
                if len(dados) >= 3 and nome_alimento.lower() in dados[1].lower():
                     nome = dados[1]
                     preco = dados[2]
                     encontrados.append((nome, preco))
    except FileNotFoundError:
        print("Arquivo de alimentos não encontrado.")
    return encontrados

def listar_alimentos(alimentos):
    if not alimentos:
        print("Nenhum alimento encontrado.")
    else: 
        print("\n Alimentos encontrados: ")
        for alimento in alimentos:
            print(f"- {nome} | Preço: R$ {preco}")
    
def menu_usuario (usuario):
    while True:
        print("O que deseja fazer hoje? ")
        print("[1] Buscar alimento")
        print("[2] Fazer pedido")
        print("[3] Avaliar pedido")
        print("[4] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == 1:
            nome = input("Digite o nome do alimento: ")
            resultados = buscar_alimento(nome)
            listar_alimentos(resultados)
        elif opcao ==2:
            itens = input("Digite os alimentos separdos por vírgula: ").split("|")
            cadastrar_pedido(usuario, itens)
            print("Pedido cadastrado!")
while True:

    #menu
    print("Escolha uma opção:")
    print("[1] - Fazer Login")
    print("[2] - Realizar Cadastro")
    print("[3] - Sair do programa")
    try:
        opcao = int(input("Digite sua opção: "))
    except ValueError:
        error_msg = "opção inválida! Digite as opções do menu (1, 2 ou 3)."
        print(error_msg)
        continue
    if opcao == 1:
        
        usuario_login = input("Nome de usuário: ")
        senha_login = input("Digite sua senha: ")

        if verifica_login(usuario_login,senha_login):
            print(f"Login bem sucedido! Que bom te ver novamente {usuario_login}.")
            menu_usuario(usuario_login)
            break
        else:
            print("Nome de usuário ou senha incorretos. Tente novamente.")
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
        print("Opção inválida. Digite uma das opções do menu (1, 2 ou 3).")

