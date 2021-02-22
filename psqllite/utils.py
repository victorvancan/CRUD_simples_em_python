import sqlite3


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = sqlite3.connect('psqlite3')

    conn.execute(""" CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL, 
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL);""")
    return conn

def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
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
        print('Listando produtos...')
        print('--------------------')
        for produto in produtos:
            print(f'ID: {produto[0]}')
            print(f'Nome: {produto[1]}')
            print(f'Preço: {produto[2]}')
            print(f'Estoque: {produto[3]}')
            print('--------------------')
    else:
        print('não existem produtos cadastrados. ')
    desconectar(conn)
    menu()

def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    cursor = conn.cursor()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    quantidade = int(input('informe a quantidade em estoque: '))

    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) VALUES ('{nome}', {preco}, {quantidade})")
    conn.commit()

    if cursor.rowcount == 1:
        print(f'O produto {nome} foi inserido com sucesso')
    else:
        print('não foi possivel inserir o produto')
    desconectar(conn)
    menu()

def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    cursor = conn.cursor()

    codigo = int(input('Informe o codigo do produto: '))
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    quantidade = int(input('informe a quantidade em estoque: '))

    cursor.execute(f" UPDATE produtos SET nome='{nome}', preco={preco}, estoque={quantidade} WHERE id={codigo}")
    conn.commit()

    if cursor.rowcount == 1:
        print(f' O produto {nome} foi atualizado com sucesso')
    else:
        print('Erro ao atualizar produto')
    desconectar(conn)
    menu()

def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    cursor = conn.cursor()

    codigo = int(input('Informe o código do produto: '))

    cursor.execute(f"DELETE FROM produtos WHERE id={codigo}")

    if cursor.rowcount == 1:
        print('Produto excluido com sucesso!')
    else:
        print(f'Erro ao exlcuir o produto com id {codigo}')
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
