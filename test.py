import requests
import random
BASE = "http://127.0.0.1:5000/"


# campos existentes no BD id, nome, idade {"id": int, "nome": str, "idade": int}
dados_entrada_pessoa =[]
#  tipos[0] == Strings, tipos[1] == int, tipos[2] == float
tipos = [["abc", "bcd", "jan", "junior", "ok"], [1, 2, 3, 4], [1.0, 2.1, 3.1, 4.5]]

for nome in tipos:
    for idade in tipos:
        # inserindo diversos formatos em cada parametros
        dados_entrada_pessoa.append({"nome": random.choice(nome), "idade": random.choice(idade)})

dados_entrada_pessoa.append({"id": 0, "nome": "teste", "idade": 1})  # Testando passar o ID
dados_entrada_pessoa.append({"idade": 1})  # Testando passar apenas 1 parametro
dados_entrada_pessoa.append({"teste": random.choice(nome), "idade": random.choice(idade)}) # PARAMETRO inexistente
# PARAMETRO inexistente a mais
dados_entrada_pessoa.append({"nome": "juniorir", "teste": random.choice(nome), "idade": random.choice(idade)})
dados_entrada_pessoa.append({})  # Vazio(sem dados)

# Testando funcionalidade de Atividades

BASE_PESSOA = BASE + "pessoa"

# Testando funcionalidades de Pessoa
def testa_metodos(caminho_relativo, entrada):
    metodos = []
    metodos.append(requests.post)
    metodos.append(requests.put)
    metodos.append(requests.patch)
    metodos.append(requests.get)
    metodos.append(requests.delete)
    for metodo in metodos:
        caminho = BASE+caminho_relativo
        resultado = metodo(caminho, entrada)
        print(metodo.__name__)
        print(resultado.request)
        print(entrada)
        print(resultado.status_code)
        print(resultado.json())
        yield


for entrada in dados_entrada_pessoa:
    try:
        teste = testa_metodos("pessoa/{}".format(entrada["nome"]), entrada)
    except KeyError:
        pass
    while True:
        try:
            teste.__next__()
            input()
        except:
            break
