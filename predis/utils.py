import redis


def gera_id():
    try:
        conn = conectar()

        chave = conn.get('chave')

        if chave:
            chave = conn.incr('chave')
            return chave
        else:
            conn.set('chave', 1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'não foi possivel gerar a chave. {e}')


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = redis.Redis(host='localhost', port=6379)

    return conn


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    conn.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()

    try:
        dados = conn.keys(pattern='produtos:*')

        if len(dados) > 0:
            print('Listando produtos')
            print('-----------------')
            for chave in dados:
                produto = conn.hgetall(chave)
                print(f"ID: {str(chave, 'utf-8', 'ignore')}")
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ignore')}")
                print(f"preco: {str(produto[b'preco'], 'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque', 'utf-8', 'ignore'])}")
                print('-------------------')
        else:
            print('não existem produtos cadastrados')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possivel listar os produtos. {e}')
    desconectar(conn)
    menu()



def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o valar do produto: '))
    estoque = int(input('Informe o estoque: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    chave = f'produtos:{gera_id()}'

    try:
        res = conn.hmset(chave, produto)

        if res:
            print(f'O produto {nome} foi inserido com suecsso. ')
        else:
            print('não foi possivel inserir o produto')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possivel inserir o produto; {e}')
    desconectar(conn)
    menu()





def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()

    chave = conn.get('chave')

    chaves = input('Informe a chave do produto: ')
    if chaves == chave:

        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o valor do produto: '))
        estoque = int(input('Informe o estoque: '))
    else:
        print('Não foi possivel encontrar a chave desejada')

    produto = {"nome": nome, "preco": preco, "estoque": estoque}

    try:
        res = conn.hmset(chave, produto)

        if res:
            print(f'O produto {nome} fo atualizado com sucesso.')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possivel atualzar os dados. {e}')
    desconectar(conn)
    menu()


def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()

    chave = input('Informe a chave do produto: ')

    try:
        res = conn.delete(chave)

        if res == 1:
            print("O produto foi deletado com sucesso. ")
        else:
            print('não existe produto com a chave informada')
    except redis.exceptions.ConnectionError as e:
        print(f'Erro ao conectar ao Redis: {e}')
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
