from models import Pessoas, Usuarios

def insere_usuario(username, senha):
    usuarios = Usuarios(login=username, password=senha)
    usuarios.save()


def consulta_usuarios():
    usuarios = Usuarios.query.all()
    return [{"id": u.id, "login": u.login} for u in usuarios]


def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jan').first()
    pessoa.idade = 25
    pessoa.save()


def deleta_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Jan').first()
    pessoa.delete()


if __name__ == '__main__':
    insere_usuario('juniorjrml', 'aaa')
    insere_usuario('jan', 'bbb')
    print(consulta_usuarios())
