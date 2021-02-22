import MySQLdb


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db='pmysql',
            host='localhost',
            user='Insira seu usuario',
            passwd='Insria sua senha'
        )
        return conn
    except MySQLdb.Error as e:
        print(f'Erro na conexão ao Mysql Server: {e}')

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
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    if len(produtos) > 0:
        print('listando produtos.......')
        print('------------------------')
        for produto in produtos:
            print(f'ID: {produto[0]}')
            print(f'produto: {produto[1]}')
            print(f'preco: {produto[2]}')
            print(f'quantidade: {produto[3]}')
            print('------------------------')
    else:
        print('não existem produtos cadastrados')
    desconectar(conn)
    menu()

def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    cursor = conn.cursor()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preco do produto: '))
    estoque = int(input('Informe a quantidade de produto em estoque: '))

    cursor.execute(f"insert Into produtos(nome, preco, estoque) values ('{nome}', '{preco}', '{estoque}');")
    conn.commit()

    if cursor.rowcount == 1:
        print(f'O produto {nome} foi inserido com sucesso')
    else:
        print('não foi possivel inserir produto')
    desconectar(conn)
    menu()

def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    cursor = conn.cursor()

    codigo = int(input('Informe o código do produto: '))
    nome = input('Informe o novo nome do produto: ')
    preco = float(input('Informe o novo preço do produto'))
    estoque = int(input('informe a nova quantidade em estoque: '))

    cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id = {codigo}")
    conn.commit()

    if cursor.rowcount == 1:
        print(f' O produto {nome} foi atualizado com sucesso')
    else:
        print('não foi possivel atualizar produto')
    desconectar(conn)
    menu()


def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    cursor = conn.cursor()

    codigo = int(input('Informe o codigo do produto: '))

    cursor.execute(f"DELETE FROM produtos WHERE id={codigo}")

    if cursor.rowcount == 1:
        print(f' O produto foi excluido com sucesso')
    else:
        print(f'não foi possivel excluir produto id = {codigo}')
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
