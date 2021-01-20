import json

from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)



@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return Usuarios.query.filter_by(login=login, password=password)

SUCESSO = "sucesso"
FALHA = "falha"
ESTADO = {"status": FALHA, "mensagem": "Erro Desconhecido"}

campos_pessoa = {
    "nome": fields.String(40),
    "idade": fields.Integer
}


class Pessoa(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
            n_status = 200

        except AttributeError:
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO
            n_status = 404

        except Exception:
            response = ESTADO
            n_status = 400

        return response, n_status
    @auth.login_required
    def put(self, nome):
        try:
            dados = json.loads(request.data)
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.idade = dados["idade"]
            pessoa.nome = dados["nome"]
            pessoa.save()
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro Alterado"
            response = ESTADO

        except AttributeError:
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO

        except Exception:
            response = ESTADO

        return response
    @auth.login_required
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro Excluido"
            response = ESTADO

        except AttributeError:
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO

        except Exception:
            response = ESTADO

        return response


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = [

            {'idade': p.idade, 'id': p.id, 'nome': p.nome} for p in pessoas]

        return response
    @auth.login_required
    def post(self):
        dados = json.loads(request.data)
        print(dados)
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        ESTADO["status"] = SUCESSO
        ESTADO["mensagem"] = "Registro incluido com sucesso"
        return ESTADO


class ListaAtividades(Resource):

    def get(self):
        atividades = Atividades.query.all()
        response = []
        for a in atividades:
            try:
                response.append({"nome": a.nome, "pessoa": a.pessoa.nome})
            except AttributeError:
                ESTADO["status"] = FALHA
                ESTADO["mensagem"] = "registro invalido id = {}".format(a.id)
                response.append(ESTADO)

        return response
    @auth.login_required
    def post(self):
        dados = json.loads(request.data)
        print(dados)
        pessoa = Pessoas.query.filter_by(nome=dados["pessoa"]).first()
        try:
            pessoa.nome
            atividade = Atividades(nome=dados["nome"], pessoa=pessoa)
            atividade.save()
            pessoa.save()
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro incluido com sucesso"
        except AttributeError:
            ESTADO["status"] = FALHA
            ESTADO["mensagem"] = "Falha ao incluir Registro"

        return ESTADO

api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividade/')

if __name__ == '__main__':
    app.run(debug=True)

