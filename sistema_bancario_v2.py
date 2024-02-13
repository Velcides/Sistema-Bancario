import textwrap
#UPGRADES V2 =================================================
#funções para as operações do banco, sacar, depositar e extrato
#função de criar usuário (cliente do banco) 
#função que filra e verificar duplicidade de cpf,
#função criar conta corrente (vincular com o usuario)
#função criar função de listar contas

# Função para exibir o menu e receber a escolha do usuário
def menu():
    # Definição do menu com opções disponíveis
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    # Exibir menu e retornar escolha do usuário
    return input(textwrap.dedent(menu))

# Função para realizar um depósito
#fornecer as variáveis apenas por posição, na chamada da função na main()
def depositar(saldo, valor, extrato, /):
    # Verificar se o valor do depósito é válido
    if valor > 0:
        # Atualizar saldo com o valor do depósito
        saldo += valor
        # Adicionar registro ao extrato
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        # Exibir mensagem de sucesso
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        # Exibir mensagem de falha se o valor for inválido
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retornar saldo e extrato atualizados
    return saldo, extrato

# Função para realizar um saque
#fornecer as variáveis apenas por nome(keyword), na chamada da função na main()
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    # Verificar se houve excedentes nas condições de saque
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    # Tratar cada caso de falha nas condições de saque
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        # Atualizar saldo com o valor do saque
        saldo -= valor
        # Adicionar registro ao extrato
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        # Incrementar o contador de saques
        numero_saques += 1
        # Exibir mensagem de sucesso
        print("\n=== Saque realizado com sucesso! ===")

    else:
        # Exibir mensagem de falha se o valor for inválido
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    # Retornar saldo, extrato e contador de saques atualizados
    return saldo, extrato

# Função para exibir o extrato da conta
#fornecer as variaveis por posição e por nome(keyword), na chamada da função na main()
def exibir_extrato(saldo, /, *, extrato):
    # Exibir o cabeçalho do extrato
    print("\n================ EXTRATO ================")
    # Exibir extrato ou mensagem de que não houve movimentações
    print("Não foram realizadas movimentações." if not extrato else extrato)
    # Exibir saldo atualizado
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    # Exibir rodapé do extrato
    print("==========================================")


# Função para criar um novo usuário
def criar_usuario(usuarios):
    # Receber CPF do novo usuário
    cpf = input("Informe o CPF (somente número): ")
    # Filtrar usuário pelo CPF
    usuario = filtrar_usuario(cpf, usuarios)

    # Verificar se já existe usuário com esse CPF
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    # Se não houver usuário com esse CPF, receber informações do novo usuário
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adicionar novo usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    # Exibir mensagem de sucesso
    print("=== Usuário criado com sucesso! ===")

# Função para filtrar um usuário por CPF
def filtrar_usuario(cpf, usuarios):
    # Filtrar lista de usuários pelo CPF fornecido
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    # Retornar o primeiro usuário encontrado, se houver, ou None se não encontrar nenhum
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios):
    # Receber CPF do titular da conta
    cpf = input("Informe o CPF do usuário: ")
    # Filtrar usuário pelo CPF fornecido
    usuario = filtrar_usuario(cpf, usuarios)

    # Verificar se encontrou um usuário com o CPF fornecido
    if usuario:
        # Se encontrou, criar a conta associada ao usuário
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    # Se não encontrou, informar que o usuário não foi encontrado
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Função para listar todas as contas criadas
def listar_contas(contas):
    # Iterar sobre cada conta e exibir suas informações
    for conta in contas:
        # Formatando a linha de exibição da conta
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        # Exibir linha com informações da conta
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função principal
def main():
    
    # Constantes
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    # Variáveis iniciais
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    # Loop principal do programa
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

