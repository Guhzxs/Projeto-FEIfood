import os

nome_projeto = "FEIfood"
separador = "-" * len(nome_projeto)
cabecalho = separador + "\n" + nome_projeto + "\n" + separador

print(cabecalho)
print("Seja bem vindo(a) ao FEIfood! É um prazer ter você conosco.")
print()
print("Escolha uma opção:")
print("[1] - Fazer Login")
print("[2] - Realizar Cadastro")
print("[3] - Sair do programa")

nome_arquivo = "FEIfood.txt"
if not os.path.exists(nome_arquivo):
    arquivo_cadastro = open(nome_arquivo, 'w+t' , encoding="utf-8")
    arquivo_cadastro.write(cabecalho)
    arquivo_cadastro.close()


def salvar_cadastro(usuario):
    valores_lista = list(usuario.values())
    linha_texto = "|".join(valores_lista) + "\n"
    with open(nome_arquivo, 'a', encoding="utf-8") as arquivo_cadastro:
        arquivo_cadastro.write(linha_texto)
    print(usuario)

def verifica_login(usuario_digitado, senha_digitada):
    try:
        with open(nome_arquivo, 'r', encoding="utf-8") as arquivo:
            contador = 0
            for linha in arquivo:
                if contador < 3:
                    contador += 1
                    continue
            linha_limpa = linha.strip()
            if linha_limpa: 

                dados_salvos = linha_limpa.split('|')

                if len(dados_salvos) >= 4:
                    usuario_salvo = dados_salvos[0]
                    senha_salva = dados_salvos[3]

                    if usuario_salvo == usuario_digitado and senha_salva == senha_digitada:
                        return True
            return False
    
    except FileNotFoundError:
        print("Erro")
        return False

while True:

    print("Escolha uma opção:")
    print("[1] - Fazer Login")
    print("[2] - Realizar Cadastro")
    print("[3] - Sair do programa")
    try:
        opcao = int(input("Digite sua opção: "))
    except ValueError:
        print("opção inválida! Digite as opções do menu (1, 2 ou 3).")
        continue
    if opcao == 1:
        print("Em construção")
        usuario_login = input("Nome de usuário: ")
        senha_login = input("Digite sua senha: ")

        if verifica_login(usuario_login,senha_login):
            print(f"Login bem sucedido! Que bom te ver novamente {usuario_login}.")
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

