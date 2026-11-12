
import json
from datetime import date

produtos = []
movimentacoes = []

# Carrega os dados do arquivo JSON
def Carregar_Dados():
    global produtos, movimentacoes

    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            produtos = dados["produtos"]
            movimentacoes = dados["movimentacoes"]

    except FileNotFoundError:
        produtos = []
        movimentacoes = []

    except json.JSONDecodeError:
        produtos = []
        movimentacoes = []
        print("Erro ao ler o arquivo!")

    except KeyError:
        produtos = []
        movimentacoes = []
        print("Estrutura do arquivo inválida!")

# Salva os dados no arquivo JSON
def Salvar_Dados():
    dados = {
        "produtos": produtos,
        "movimentacoes": movimentacoes
    }

    try:
        with open("dados.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    except OSError:
        print("Erro ao salvar os dados!")

# Menu principal
def menu():
    print("\nMenu:")
    print("1 - Incluir Produto")
    print("2 - Alterar Produto")
    print("3 - Excluir Produto")
    print("4 - Listar Produtos")
    print("5 - Registrar Entrada")
    print("6 - Registrar Saída")
    print("7 - Consultar Estoque")
    print("8 - Produtos com Estoque Baixo")
    print("9 - Sair")

# Inclui um produto
def Incluir_Produto():
    try:
        codigo = int(input("Código: "))

        for produto in produtos:
            if produto["codigo"] == codigo:
                print("Código já cadastrado!")
                return

        descricao = input("Nome: ").strip()
        quantidade = int(input("Quantidade: "))
        minimo = int(input("Estoque mínimo: "))
        preco = float(input("Preço: ").replace(",", "."))

        if codigo <= 0 or descricao == "" or quantidade < 0 or minimo < 0 or preco <= 0:
            print("Dados inválidos!")
            return

        produto = {
            "codigo": codigo,
            "descricao": descricao,
            "quantidade": quantidade,
            "estoque_minimo": minimo,
            "preco": preco
        }

        produtos.append(produto)
        Salvar_Dados()
        print("Produto cadastrado!")

    except ValueError:
        print("Digite valores válidos!")

# Altera um produto
def Alterar_Produto():
    try:
        codigo = int(input("Código do produto: "))

        for produto in produtos:
            if produto["codigo"] == codigo:
                descricao = input("Novo nome: ").strip()
                minimo = int(input("Novo estoque mínimo: "))
                preco = float(input("Novo preço: ").replace(",", "."))

                if descricao == "" or minimo < 0 or preco <= 0:
                    print("Dados inválidos!")
                    return

                produto["descricao"] = descricao
                produto["estoque_minimo"] = minimo
                produto["preco"] = preco

                Salvar_Dados()
                print("Produto alterado!")
                return

        print("Produto não encontrado!")

    except ValueError:
        print("Digite valores válidos!")

# Exclui um produto
def Excluir_Produto():
    try:
        codigo = int(input("Código do produto: "))

        for produto in produtos:
            if produto["codigo"] == codigo:
                produtos.remove(produto)
                Salvar_Dados()
                print("Produto excluído!")
                return

        print("Produto não encontrado!")

    except ValueError:
        print("Código inválido!")

# Lista os produtos
def Listar_Produto():
    if len(produtos) == 0:
        print("Nenhum produto cadastrado!")
        return

    for produto in produtos:
        print("Código:", produto["codigo"])
        print("Nome:", produto["descricao"])
        print("Quantidade:", produto["quantidade"])
        print("Estoque mínimo:", produto["estoque_minimo"])
        print("Preço: R$", produto["preco"])

# Registra entrada ou saída
def Movimentar_Estoque(tipo):
    try:
        codigo = int(input("Código do produto: "))

        for produto in produtos:
            if produto["codigo"] == codigo:
                quantidade = int(input("Quantidade: "))

                if quantidade <= 0:
                    print("Quantidade inválida!")
                    return

                if tipo == "saida":
                    if quantidade > produto["quantidade"]:
                        print("Estoque insuficiente!")
                        return

                    produto["quantidade"] -= quantidade

                else:
                    produto["quantidade"] += quantidade

                movimentacao = {
                    "codigo": codigo,
                    "descricao": produto["descricao"],
                    "tipo": tipo,
                    "quantidade": quantidade,
                    "data": date.today().strftime("%d/%m/%Y")
                }

                movimentacoes.append(movimentacao)
                Salvar_Dados()
                print("Movimentação registrada!")
                return

        print("Produto não encontrado!")

    except ValueError:
        print("Digite valores válidos!")

# Consulta estoque por código ou nome
def Consultar_Estoque():
    busca = input("Digite o código ou nome: ").strip()

    for produto in produtos:
        if busca == str(produto["codigo"]) or busca.lower() in produto["descricao"].lower():
            print("Produto:", produto["descricao"])
            print("Código:", produto["codigo"])
            print("Quantidade:", produto["quantidade"])
            print("Estoque mínimo:", produto["estoque_minimo"])
            print("Preço: R$", produto["preco"])
            return

    print("Produto não encontrado!")

# Mostra produtos com estoque baixo
def Estoque_Baixo():
    encontrou = False

    for produto in produtos:
        if produto["quantidade"] <= produto["estoque_minimo"]:
            print("Produto:", produto["descricao"])
            print("Quantidade:", produto["quantidade"])
            print("Estoque mínimo:", produto["estoque_minimo"])
            encontrou = True

    if encontrou == False:
        print("Nenhum produto com estoque baixo!")

# Carrega os dados
Carregar_Dados()

# Executa o programa
while True:
    menu()
    opc = input("Escolha uma opção: ").strip()

    if opc == "1":
        Incluir_Produto()
    elif opc == "2":
        Alterar_Produto()
    elif opc == "3":
        Excluir_Produto()
    elif opc == "4":
        Listar_Produto()
    elif opc == "5":
        Movimentar_Estoque("entrada")
    elif opc == "6":
        Movimentar_Estoque("saida")
    elif opc == "7":
        Consultar_Estoque()
    elif opc == "8":
        Estoque_Baixo()
    elif opc == "9":
        print("Saindo . . .")
        break
    else:
    print("Opção inválida. Tente novamente.")   