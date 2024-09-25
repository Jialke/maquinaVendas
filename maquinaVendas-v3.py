import copy  # biblioteca copy para gerar uma lista a partir de outra

# Declaração de matrizes e variáveis
# produtos = [id, nome, valor unitário, quantidade]
produtos = [[1, 'Coca-cola', 3.76, 2],
            [2, 'Pepsi', 3.67, 5],
            [3, 'Monster', 9.96, 1],
            [4, 'Café', 1.25, 100],
            [5, 'Redbull', 13.99, 2]]

# Notas = [id, nota, quantidade]
notasFixas = [[1, 200, 20],
              [2, 100, 10],
              [3, 50, 15],
              [4, 20, 30],
              [5, 10, 10],
              [6, 5, 10],
              [7, 2, 40],
              [8, 1, 10],
              [9, 0.5, 24],
              [10, 0.1, 20],
              [11, 0.01, 30]]

continuar = True

# Declaração de funções
def buscaProduto(id, produtos):
    for produto in produtos:
        if id == produto[0]:
                return produto
    return 1 #Se ID não existe, retorna 1

def buscaNota(id, notas):
    for nota in notas:
        if id == nota[0]:
            return nota
    return 1 #Se nota não existe, retorna 1

def listaProduto(produtos):
    for produto in produtos:
        print(produto)

def listaNota(notas):
    for nota in notas:
        print(nota)

def troco(valorDigitado, valorProduto):
    global notasFixas
    notas_temp = copy.deepcopy(notasFixas) #Criação de matriz temporária para armazenar as notas
    troco_final = []
    troco = round(valorDigitado - valorProduto, 2)

    for nota in notas_temp:
        quant = 0
        while troco >= nota[1] and nota[2] > 0: # Verifica se o troco é maior que a nota analisada e se existe a nota no estoque
            troco = round(troco - nota[1], 2)
            nota[2] -= 1
            quant += 1
        if quant > 0:
            troco_final.append([quant, nota[1]])

    if troco == 0: #Se o troco for zero, teve notas suficientes na maquina então notas fixa são atualizadas com os descontos no estoque
        notasFixas = copy.deepcopy(notas_temp)
    else:
        troco_final = 0
    return troco_final

def tiraEstoqueProduto(id, produtos):
    for produto in produtos:
        if id == produto[0]:
            produto[3] -= 1

def continuarExecucao():
    verifica = int(input('\nDeseja continuar?\n[1] sim\n[2] não\n'))
    while verifica < 1 or verifica > 2:
        verifica = int(input('Valor inválido, digite novamente: '))
    if verifica == 2:
        global continuar
        continuar = False

def compra(produtos):
    print('\nProdutos:')
    for produto in produtos:
        print('[', produto[0], ']', produto[1]) #Lista o ID e o nome dos produtos

    idproduto = int(input('Digite o número do produto que deseja: '))
    produto = buscaProduto(idproduto, produtos) # Chama função para buscar o produto

    while produto == 1 or produto[3] == 0: #Verificação de ID e de estoque
        if produto == 1:
            idproduto = int(input('Produto inválido! Digite novamente: '))
        else:
            idproduto = int(input('Produto sem estoque! Digite novamente: '))

        produto = buscaProduto(idproduto, produtos)
    print()

    print('Produto selecionado:', produto[1])
    valorProduto = produto[2]
    print('Valor:', valorProduto)
    valorDigitado = float(input('Insira o valor de pagamento: '))

    while valorDigitado < valorProduto: #Verificação de pagamento
        valorDigitado = float(input('Valor inválido! Insira o valor de pagamento novamente: '))
    print()

    if valorDigitado > valorProduto: #Verificação de existência de troco
        troco_final = troco(valorDigitado, valorProduto) # Chama função troco
        
        print('Troco total: R$', round(valorDigitado - valorProduto, 2))
        print('Troco:')

        # Verificação do troco
        if troco_final == 0:
            print('Notas insuficientes para completar troco... Encerrando compra.')
        else:
            for valor in troco_final:
                if valor[1] > 1:
                    print(valor[0], 'nota(s) de R$', valor[1], 'reais')
                elif valor[1] == 1:
                    print(valor[0], 'moeda(s) de R$', valor[1], 'real')
                else:
                    print(valor[0], 'moeda(s) de', valor[1], 'centavos')
            tiraEstoqueProduto(idproduto, produtos)
            print('Obrigado pela compra!')
    else:
        print('Valor exato! Obrigado pela compra!')
        tiraEstoqueProduto(idproduto, produtos)
    continuarExecucao()

def administrador(produtos, notas): # Função do modo Administrador
    admin = True
    while admin:
        seleciona = int(input('\nSelecione o que deseja realizar:\n[1] Adicionar produto\n[2] Remover produto\n[3] '
                              'Alterar produto\n[4] Alterar estoque de notas\n')) # Seleção de opção de ação no modo administrador
        while seleciona < 1 or seleciona > 4: #Verificação de validez
            seleciona = int(input('Valor inválido! Tente novamente: '))

        if seleciona == 1: # Adicionar produto
            maiorID = 0
            for produto in produtos:
                if produto[0] > maiorID:
                    maiorID = produto[0]
            id = maiorID + 1 # Gerar ID para novo produto
            nomeProduto = input('\nInsira o nome do produto: ')
            valorProduto = float(input('Insira o valor unitário do produto: '))
            estoqueProduto = int(input('Insira a quantidade do estoque: '))

            produtos.append([id, nomeProduto, valorProduto, estoqueProduto]) #Adicionar linha à matriz produtos

        elif seleciona == 2: # Remover produto
            print('\nProdutos:')
            listaProduto(produtos)

            selecionaProduto = int(input('Selecione o ID do produto que deseja deletar: '))
            produto = buscaProduto(selecionaProduto, produtos) # Procura o ID do produto
            while produto == 1: #Verificação de validez
                selecionaProduto = int(input('ID inválido! Digite novamente: '))
                produto = buscaProduto(selecionaProduto, produtos)

            linhaDeletar = produto[0] - 1 # Seleciona a linha a ser deletada
            del produtos[linhaDeletar] #Deleta linha da matriz produto

            idAnterior = 0 # Arrumar IDs após deletar uma linha
            for item in produtos:
                if item[0] == idAnterior + 2:
                    item[0] -= 1
                    idAnterior = item[0]
                else:
                    idAnterior = item[0]

        elif seleciona == 3: # Editar produto
            print('\nProdutos:')
            listaProduto(produtos)

            selecionaProduto = int(input('\nSelecione qual produto deseja alterar: '))
            produto = buscaProduto(selecionaProduto, produtos)
            while produto == 1: #Verificação de validez
                selecionaProduto = int(input('ID inválido! Digite novamente: '))
                produto = buscaProduto(selecionaProduto, produtos)

            selecionaEditar = int(
                input('\nSelecione o que deseja alterar:\n[1] Nome do produto\n[2] Valor do produto\n[3] Estoque\n'))
            while selecionaEditar < 1 or selecionaEditar > 3: #Verificação de validez
                selecionaEditar = int(input('Valor inválido! Tente novamente: '))
            if selecionaEditar == 1: # Editar nome
                editar = input('\nDigite o novo nome: ') 
                produto[1] = editar
            elif selecionaEditar == 2: # Editar valor unitário
                editar = float(input('\nDigite o novo valor: '))
                produto[2] = editar
            else: # Editar estoque
                editar = int(input('\nDigite o novo valor do estoque: '))
                produto[3] = editar

        else: # Alterar estoque de notas
            print('\nNotas:')
            listaNota(notas)

            selecionaNota = int(input('\nSelecione o id da nota para alterá-la: '))
            nota = buscaNota(selecionaNota, notas)
            while nota == 1: #Verificação de validez
                selecionaNota = int(input('Valor inválido! Tente novamente: '))
                nota = buscaNota(selecionaNota, notas)

            editar = int(input('\nDigite a nova quantidade do estoque: '))
            nota[2] = editar

        continuar = int(input('\nDeseja continuar a editar?\n[1] sim\n[2] não\n')) # Verifica se deseja permanecer no modo Administrador
        while continuar < 1 or continuar > 2:
            continuar = int(input('Valor inválido! tente novamente!'))
        if continuar == 2:
            admin = False

def selecionaModo(produtos, notas):
    seleciona = int(input('\nSelecione o modo de execução:\n[1] Administrador\n[2] Comprar\n[3] Encerrar execução\n'))
    while seleciona < 1 or seleciona > 3:
        seleciona = int(input('Valor inválido! Tente novamente: '))
    if seleciona == 1:
        return administrador(produtos, notas)
    elif seleciona == 2:
        return compra(produtos)
    else:
        global continuar
        continuar = False

# Execução do código
while continuar:
    selecionaModo(produtos, notasFixas)

print('\nCréditos: Lucas da Costa Paula')