import psycopg2

class DataMining(object):
    _db=None
    def __init__(self, mhost, db, usr, pwd):
        self._db = psycopg2.connect(host=mhost, database=db, user=usr,  password=pwd)

    def manipular(self, sql):
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            cur.close();
            self._db.commit()
        except:
            return False;
            return True;

    def consultar(self, sql):
        rs=None
        try:
            cur=self._db.cursor()
            cur.execute(sql)
            rs=cur.fetchall();
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

def main():
    con=DataMining('localhost','DataMining','postgres','aluno')
    # sql = "insert into cidade values (default,'Rio de Janeiro','RJ')"
    # if con.manipular(sql):
    #   print('inserido com sucesso!')
    # print (con.proximaPK('cidade', 'id'))
    rs=con.consultar("select * from transacao")
    for linha in rs:
      print (linha)
    con.fechar()

if __name__ == "__main__":
    main()
