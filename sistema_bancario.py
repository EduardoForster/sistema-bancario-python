import textwrap
from datetime import datetime


class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []


class Conta:
    def __init__(self, agencia, numero_conta, cliente):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0.0
        self.extrato = ""


def menu():
    menu = """
    ================ MENU ================
    [d]	Depositar
    [s]	Sacar
    [e]	Extrato
    [nc]	Nova conta
    [lc]	Listar contas
    [nu]	Novo usuário
    [q]	Sair
    => """
    return input(textwrap.dedent(menu))


def depositar(conta, valor, /):
    if valor > 0:
        conta.saldo += valor
        conta.extrato += f"Depósito:\t\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")


def sacar(*, conta, valor, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > conta.saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        conta.saldo -= valor
        conta.extrato += f"Saque:\t\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return numero_saques


def exibir_extrato(conta, /):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta.extrato else conta.extrato)
    print(f"\nSaldo:\t\t\tR$ {conta.saldo:.2f}")
    print("==========================================")
    print(f"Titular:\t\t{conta.cliente.nome}")
    print(f"Agência:\t\t{conta.agencia}")
    print(f"C/C:\t\t\t{conta.numero_conta}")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = Cliente(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_cliente)

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        nova_conta = Conta(agencia, numero_conta, usuario)
        usuario.contas.append(nova_conta)
        print("\n=== Conta criada com sucesso! ===")
        return nova_conta

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero_conta}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    numero_saques = 0
    usuarios = []
    contas = []
    conta_selecionada = None

    while True:
        opcao = menu()

        if opcao == "d":
            if not conta_selecionada:
                print("\n@@@ Selecione uma conta primeiro (opção 'nc' ou 'lc')! @@@")
                continue
            valor = float(input("Informe o valor do depósito: "))
            depositar(conta_selecionada, valor)

        elif opcao == "s":
            if not conta_selecionada:
                print("\n@@@ Selecione uma conta primeiro (opção 'nc' ou 'lc')! @@@")
                continue
            valor = float(input("Informe o valor do saque: "))
            numero_saques = sacar(
                conta=conta_selecionada,
                valor=valor,
                limite=500,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            if not conta_selecionada:
                print("\n@@@ Selecione uma conta primeiro (opção 'nc' ou 'lc')! @@@")
                continue
            exibir_extrato(conta_selecionada)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                conta_selecionada = conta
                print(f"\n✓ Conta selecionada: Agência {conta.agencia} | C/C {conta.numero_conta}")

        elif opcao == "lc":
            listar_contas(contas)
            if contas:
                try:
                    idx = int(input("\nSelecione o número da conta (índice): "))
                    if 0 <= idx < len(contas):
                        conta_selecionada = contas[idx]
                        print(f"\n✓ Conta selecionada: Agência {conta_selecionada.agencia} | C/C {conta_selecionada.numero_conta}")
                        numero_saques = 0
                    else:
                        print("\n@@@ Índice inválido! @@@")
                except ValueError:
                    print("\n@@@ Entrada inválida! @@@")

        elif opcao == "q":
            print("\nObrigado por usar nosso banco! Até logo!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()