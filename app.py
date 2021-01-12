import json

from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades


app = Flask(__name__)
api = Api(app)
SUCESSO = "sucesso"
FALHA = "falha"
ESTADO = {"status": FALHA, "mensagem": "Erro Desconhecido"}

class Pessoa(Resource):

    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }

        except AttributeError:
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO

        except Exception:
            response = ESTADO

        return response

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
        lista_retorno = {}
        for p in Pessoas.query.all():
            pessoa = {
                'idade': p.idade,
                'id': p.id
            }
            lista_retorno[p.nome] = pessoa

        return lista_retorno

    def post(self):
        dados = json.loads(request.data)
        print(dados)
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        ESTADO["status"] = SUCESSO
        ESTADO["mensagem"] = "Registro incluido com sucesso"
        return ESTADO


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa/')

if __name__ == '__main__':
    app.run(debug=True)

