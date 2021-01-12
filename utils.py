from models import Pessoas

def insere_pessoa():
    pessoa = Pessoas(nome='Jan', idade=26)
    pessoa.save()



def consulta_pessoa():
    pessoa = Pessoas.query.all()
    for i in pessoa:
        print(i, i.idade)


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jan').first()
    pessoa.idade = 25
    pessoa.save()


def deleta_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jan').first()
    pessoa.delete()


if __name__ == '__main__':
    consulta_pessoa()
    deleta_pessoa()
    #insere_pessoa()
    consulta_pessoa()
