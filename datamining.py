import psycopg2

class Produto(object):
    transacoes = []
    def __init__(self, nome):
        self.nome = nome

    def add(self, valor):
        self.transacoes.append(valor)
    
    def switch(self, transacoes):
        self.transacoes = transacoes

class DataMining(object):
    _db=None
    def __init__(self, mhost, db, usr, pwd):
        try:
            self._db = psycopg2.connect(host=mhost, database=db, user=usr,  password=pwd)

        except:
            return None

    def manipular(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
        except:
            return False
            return True

    def consultar(self, sql):
        rs=None
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall()
            return rs
        except:
            return None

    def proximaPK(self, tabela, chave):
        sql='select max('+chave+') from '+tabela
        rs = self.consultar(sql)
        pk = rs[0][0]
        return pk+1

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

    def calculo_suporte(self, produto_x, produto_y, total):
        pass

    def calculo_confianca(self, produto_x, produto_y):
        pass



def main():
    produtos = []
    data_mining = DataMining('localhost','DataMining','postgres','admin')
    data_mining.criar_produtos(produtos)

    rs = data_mining.consultar("select * from transacoes")

    # ESTRANHO NAO TER FUNCIONADO NESSE METODO ABAIXO:
    # i = 0
    # for linha in rs:
    #     print(str(linha))
    #     for coluna in linha:
    #         produtos[i].add(coluna)
        # i += 1

    # ESTRANHO NAO TER FUNCIONADO NESSE METODO ABAIXO TAMBEM:
    for linha in rs:
        print(str(linha))
        i = 1
        for produto in produtos:
            produto.add(linha[i])
            i+=1

    aux = []
    prod_atual = 0
    for produto in produtos:
        index = prod_atual
        for i in range(0, 10):
            aux.append(produto.transacoes[index])
            index += 7
        produto.switch(aux)
        print('\n' + 'aquiiii' + str(aux))
        print(produto.transacoes)
        aux.clear()
        prod_atual += 1

    for produto in produtos:
        print('\n' + produto.nome + '   -   ' + str(produto.transacoes))
        

    ##################### EXTREME GOHORSE 1 ####################
    # i = 1
    # for produto in produtos:
    #     for linha in rs:
    #         produto.add(linha[i])
    #     i+=1

    # for produto in produtos:
    #     produto._transacoes = produto._transacoes[0:10]

    #################### EXTREME GOHORSE 2 ####################
    # i = 0
    # for produto in produtos:
    #     for coluna in rs[i]:
    #         produto.add(coluna)
    #     i+=1

    # x = 1
    # y = 8
    # for produto in produtos:
    #     produto._transacoes = produto._transacoes[x:y]
    #     x+=8
    #     y+=8

    ###########################################################

    # suporte_min = float(input('Insira o valor de suporte mínimo: <Formato: 0.0>'))
    # confianca_min = float(input('Insira o valor de confiança mínima: <Formato: 0.0>'))

    # i = 0
    # while i < len(produtos):
    #     TODO: CONTINUAR...
    #     i+=1
    

    data_mining.fechar()

if __name__ == "__main__":
    main()
