import json

from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

def converter_para_tipo_do_elemento(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x



auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


SUCESSO = "sucesso"
FALHA = "falha"
ESTADO = {"status": FALHA, "mensagem": "Erro Desconhecido"}

pessoa_post_args = reqparse.RequestParser()
pessoa_post_args.add_argument(
    'nome', type=str, help="Nome da Pessoa a cadasTrar", required=True)
pessoa_post_args.add_argument(
    'idade', type=int, help="Idade da Pessoa a cadastrar", required=True)

campos_pessoa = {
    "nome": fields.String(40),
    "idade": fields.Integer
}

@auth.verify_password
def autentica_usuario(login, senha):
    if not (login, senha):
        return False
    else:
        return Usuarios.query.filter_by(login=login, password=senha).first()

class Pessoa(Resource):
    def get(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
            print(pessoa)
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

            n_status = 200
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro Alterado"
            response = ESTADO

        except AttributeError:
            n_status = 404
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO

        except Exception:
            n_status = 400
            response = ESTADO

        return response, n_status


    @auth.login_required
    def delete(self, nome):
        try:
            pessoa = Pessoas.query.filter_by(nome=nome).first()
            pessoa.delete()
            n_status = 200
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro Excluido"
            response = ESTADO

        except AttributeError:
            n_status = 404
            ESTADO["mensagem"] = "Registro não localizado"
            ESTADO["status"] = FALHA
            response = ESTADO

        except Exception:
            n_status = 400
            response = ESTADO

        return response, n_status


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()
        response = []
        n_status = 404
        for p in pessoas:
            try:
                n_status = 200
                response.append({'idade': p.idade, 'id': p.id, 'nome': p.nome})
            except:
                ESTADO["mensagem"] = "Registro não localizado"
                ESTADO["status"] = FALHA
                response.append(ESTADO)
        return response, n_status

    @auth.login_required
    def post(self):
        try:
            dados = json.loads(request.data)
            for atributo in dados:
                dados[atributo] = converter_para_tipo_do_elemento(dados[atributo])

            if type(dados['nome']) != str or type(dados['idade']) != int:
                raise KeyError
            pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
            pessoa.save()

            n_status = 201
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro incluido com sucesso"

        except KeyError:
            n_status = 400
            ESTADO["status"] = FALHA
            ESTADO["mensagem"] = "Falha ao inserir"

        return ESTADO, n_status


class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = []
        n_status = 404
        for a in atividades:
            try:
                response.append({"nome": a.nome, "pessoa": a.pessoa.nome})
                n_status = 200
            except AttributeError:
                ESTADO["status"] = FALHA
                ESTADO["mensagem"] = "registro invalido id = {}".format(a.id)
                response.append(ESTADO)

        return response, n_status

    @auth.login_required
    def post(self):
        dados = json.loads(request.data)
        print(dados)
        try:
            pessoa = Pessoas.query.filter_by(nome=dados["pessoa"]).first()
            pessoa.nome
            atividade = Atividades(nome=dados["nome"], pessoa=pessoa)
            atividade.save()
            pessoa.save()
            n_status = 201
            ESTADO["status"] = SUCESSO
            ESTADO["mensagem"] = "Registro incluido com sucesso"

        except AttributeError:
            n_status = 404
            ESTADO["status"] = FALHA
            ESTADO["mensagem"] = "Falha ao localizar pessoa"

        return ESTADO, n_status

api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividade/')

if __name__ == '__main__':
    app.run(debug=True)

