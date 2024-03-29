#!/usr/bin/python3
import psycopg2
import pandas as pd

produtos = []
regras_interessantes = []
arq = open('resultado.txt', 'w')
data_frame = None


class Produto(object):
    transacoes = []

    def __init__(self, nome):
        self.nome = nome

    def add(self, valor):
        self.transacoes.append(valor)

    def trocar_transacoes(self, transacoes):
        self.transacoes = transacoes


class DataMining(object):
    _db = None

    def __init__(self, mhost, db, usr, pwd):
        try:
            self._db = psycopg2.connect(
                host=mhost, database=db, user=usr, password=pwd)

        except:
            return None

    def manipular(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False
            return True

    def consultar(self, sql):
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
            return rs
        except:
            return None

    def proximaPK(self, tabela, chave):
        sql = 'select max(' + chave + ') from ' + tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk + 1

    def fechar(self):
        self._db.close()

    def criar_produtos(self, lista_produtos):
        lista_produtos.append(Produto('leite'))
        lista_produtos.append(Produto('cafe'))
        lista_produtos.append(Produto('cerveja'))
        lista_produtos.append(Produto('pao'))
        lista_produtos.append(Produto('manteiga'))
        lista_produtos.append(Produto('arroz'))
        lista_produtos.append(Produto('feijao'))


def calculo_suporte(produto_x, produto_y):
    total_transacoes = len(produto_x.transacoes)
    qtd_x_and_y = 0

    i = 0
    while i < total_transacoes:
        if produto_x.transacoes[i] == True and produto_y.transacoes[i] == True:
            qtd_x_and_y += 1
        i += 1
    return float(qtd_x_and_y / total_transacoes)


def calculo_confianca(produto_x, produto_y):
    total_transacoes = len(produto_x.transacoes)
    qtd_x_and_y = 0
    qtd_x = 0

    i = 0
    while i < total_transacoes:
        if produto_x.transacoes[i] == True and produto_y.transacoes[i] == True:
            qtd_x_and_y += 1

        if produto_x.transacoes[i] == True:
            qtd_x += 1

        i += 1

    return float(qtd_x_and_y / qtd_x)


def preparar_dados():
    data_mining = DataMining('localhost', 'DataMining', 'postgres', 'admin')
    data_mining.criar_produtos(produtos)

    consulta_tabela = "select * from transacoes"
    
    rs = data_mining.consultar(consulta_tabela)

    # Lib PANDAS para analizar a tabela em si
    data_frame = pd.read_sql_query(consulta_tabela, data_mining._db)


    arq.writelines(
        '\n\n************************DADOS EXTRAIDOS DO BANCO************************\n\n')
    for linha in rs:
        arq.write(str(linha) + '\n')
        i = 1
        for produto in produtos:
            produto.add(linha[i])
            i += 1
    arq.write(
        '\n************************************************************************\n')

    # linhas da tabela
    qtd_transacoes = data_frame.shape[0]
    # colunas da tabela
    qtd_produtos = data_frame.shape[1] - 1
    
    aux = []
    produto_atual = 0
    for produto in produtos:
        index = produto_atual

        for i in range(0, qtd_transacoes):
            aux.append(produto.transacoes[index])
            index += qtd_produtos

        produto.trocar_transacoes(aux)
        aux = []
        produto_atual += 1

    arq.write(
        '\n\n********************PRODUTOS PREPARADOS DEVIDAMENTE*********************\n')
    for produto in produtos:
        arq.write('\n' + produto.nome + '\n' + str(produto.transacoes) + '\n')
    arq.write(
        '\n************************************************************************\n\n')

    data_mining.fechar()


def analisar_dados():
    minsup = float(
        input('Insira o valor de suporte minimo para analise: <Formato: 0.0>'))
    minconf = float(
        input('Insira o valor de confianca minima para analise: <Formato: 0.0>'))

    arq.write('\n\nSuporte minimo utilizado para a analise: {}\n'.format(minsup))
    arq.write('\nConfianca minima utilizada para a analise: {}\n\n'.format(minconf))

    for produto in produtos:
        for produto2 in produtos:
            if produto.nome != produto2.nome:
                if calculo_suporte(produto, produto2) >= minsup and calculo_confianca(produto,
                                                                                      produto2) >= minconf:
                    regras_interessantes.append('{} and {} - Suporte = {} / Confianca = {}'.format(
                        produto.nome, produto2.nome, calculo_suporte(produto, produto2), calculo_confianca(produto, produto2)))

    arq.write(
        '\n\n*******************REGRAS INTERESSANTES ENCONTRADAS*******************\n')
    for regra in regras_interessantes:
        arq.write(regra + '\n')
    arq.write(
        '\n************************************************************************\n')

    print("\nArquivo salvo em ./resultado.txt")


def main():
    preparar_dados()
    analisar_dados()
    arq.close()


if __name__ == "__main__":
    main()
