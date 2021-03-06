import socket
import couchdb


def conectar():
    """
    Função para conectar ao servidor
    """
    user = 'Insira deu user'
    password = 'Insira sua senha'
    conn = couchdb.Server(f'http://{user}:{password}@localhost:5984')

    banco = 'pcouch'
    if banco in conn:
        db = conn[banco]

        return db
    else:
        try:
            db = conn.create(banco)

            return db
        except socket.gaierror as e:
            print(f'Erro ao conectar ao servidor: {e}')
        except couchdb.http.Unauthorized as f:
            print(f'voce não tem permissão de acesso {f}')
        except ConnectionRefusedError as q:
            print(f'Não foi possivel conectar ao servidor: {q}')

def desconectar():
    """ 
    Função para desconectar do servidor.
    """
    print('Desconectando do servidor...')


def listar():
    """
    Função para listar os produtos
    """
    db = conectar()

    if db:
        if db.info()['doc_count'] > 0:
            print('listando produtos....')
            print('---------------------')
            for doc in db:
                print(f"ID: {db[doc]['_id']}")
                print(f"REV: {db[doc]['_rev']}")
                print(f"Produto: {db[doc]['nome']}")
                print(f"Preço: {db[doc]['preco']}")
                print(f"Estoque: {db[doc]['estoque']}")
                print('---------------------')
        else:
            print('Não existem produtos cadastrados. ')
    else:
        print('Nçao foi possivel conectar ao DB.')



def inserir():
    """
    Função para inserir um produto
    """  
    db = conectar()

    if db:
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o Preço do produto: '))
        estoque = int(input('Informe o estoque: '))

        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        res = db.save((produto))

        if res:
            print(f'O produto {nome} foi inserido com sucesso. ')
        else:
            print('O produto não foi salvo')
    else:
        ('não foi possivel conectar ao DB')


def atualizar():
    """
    Função para atualizar um produto
    """
    db = conectar()

    if db:
        chave = input('Informe o id do produto: ')

        try:
            doc = db[chave]

            nome = input('Informe o nome do produto: ')
            preco = float(input('Informe o Preço do produto: '))
            estoque = int(input('Informe o estoque: '))

            doc['nome'] =nome
            doc['preco'] = preco
            doc['estoque'] = estoque
            db[doc.id] = doc
            print(f'O produto {nome} foi atualizado com sucesso. ')
        except couchdb.http.ResourceNotFound as e:
            print(f'produto não encontrado; {e}')
    else:
        print('não foi possivel conectar ao DB')

def deletar():
    """
    Função para deletar um produto
    """  
    db = conectar()

    if db:
        _id = input('Informe o ID do produto: ')

        try:
            db.delete(db[_id])
            print('Produto deletado com sucesso.')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi ṕssível deletar o produto: {e}')
    else:
        print('Erro ao conectar no DB')

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
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
