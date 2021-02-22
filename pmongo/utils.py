from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as berros


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = MongoClient('localhost', 27017)

    return conn


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    db = conn.pmongo

    try:
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find()
            print('listando produtos')
            print('-----------------')
            for produto in produtos:
                print(f"ID: {produto['_id']}")
                print(f"Produto:{produto['nome']}")
                print(f"preco: {produto['preco']}")
                print(f"estoque: {produto['estoque']}")
                print('-----------------')
        else:
            print('não existem produtos cadastrado')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados {e}')
    desconectar(conn)
    menu()




def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    db = conn.pmongo

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe a quantidade em estoque: '))

    try:
        db.produtos.insert_one(
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
        )
        print('O produto foi registrado com sucesso! ')
    except errors.PyMongoError as e:
        print(f'Nâo foi possivel inserir o produto. {e}')
    desconectar(conn)
    menu()


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    db = conn.pmongo

    _id = input('Informe o ID do produto que deseja atualizar: ')
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe a quantidade em estoque: '))

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                }
            )
            if res.modified_count == 1:
                print(f'O produto {nome} foi atualizado com sucesso')
            else:
                print('não foi possivel atualizar o produto')
        else:
            print('não existem documento para serem atualizados.')
    except errors.PyMongoError as e:
        print(f'Erro ao atualizar o banco de dados: {e}')
    except berros.errosrs.InvalidId as f:
        print(f'OBJECTID invalido. {f}')
    desconectar(conn)
    menu()


def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    db = conn.pmongo

    _id = input('Informe o ID do produto: ')

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.delete_count > 0:
                print('Produto deletado com sucesso')
            else:
                print('Não foi possivel deletar o prodtos. ')
        else:
            print('Não existem produtos a serem deletados')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    except berros.errosrs.InvalidId as f:
        print(f'OBJECTID invalido. {f}')
    desconectar(conn)
    menu()


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    print('5 - sair do programa')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        elif opcao == 5:
            exit()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
