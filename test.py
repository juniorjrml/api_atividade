import requests
import random
import json
BASE = "http://127.0.0.1:5000/"


# campos existentes no BD id, nome, idade {"id": int, "nome": str, "idade": int}
dados_entrada_pessoa =[]
#  tipos[0] == Strings, tipos[1] == int, tipos[2] == float
tipos = [["abc", "bcd", "jan", "junior", "ok"], [1, 2, 3, 4], [1.0, 2.1, 3.1, 4.5]]

# gera entradas aleatorias com tipo de variaveis sdiferentes para cada chave
for nome in tipos:
    for idade in tipos:
        # inserindo diversos formatos em cada parametros
        dados_entrada_pessoa.append({"nome": random.choice(nome), "idade": random.choice(idade)})

# Testando passar o ID
dados_entrada_pessoa.append({"id": 0, "nome": "teste", "idade": 1})

# Testando passar apenas 1 parametro
dados_entrada_pessoa.append({"idade": 1})

# PARAMETRO inexistente
dados_entrada_pessoa.append({"teste": random.choice(nome), "idade": random.choice(idade)})

# PARAMETRO inexistente inserido a mais
dados_entrada_pessoa.append({"nome": "juniorir", "teste": random.choice(nome), "idade": random.choice(idade)})

dados_entrada_pessoa.append({})  # Vazio(sem dados)

# Testando funcionalidade de Atividades
BASE_ATIVIDADE = BASE + "atividade"


# Testando funcionalidades de Pessoa

BASE_PESSOA = BASE + "pessoa/"

def exibe_resultado_request(request):
    print(request.url)
    print(resultado.request)
    print(request.__str__())

    # Caso não tenha resultado json imprime ----
    try:
        print(request.json())
    except:
        print("---")
    print()



for entrada in dados_entrada_pessoa:
    print(entrada)
    jsons = json.dumps(entrada)

    # Caso n tenha o campo nome coloca em uma rota existente para testar
    try:
        nome = str(entrada["nome"])
    except:
        nome = "juniorJRML"  # nome existente no bd
    resultado = requests.post(BASE_PESSOA, jsons)
    exibe_resultado_request(resultado)

    resultado = requests.get(BASE_PESSOA)
    exibe_resultado_request(resultado)

    resultado = requests.put(BASE_PESSOA+nome, jsons)
    exibe_resultado_request(resultado)

    resultado = requests.patch(BASE_PESSOA+nome, jsons)
    exibe_resultado_request(resultado)

    resultado = requests.get(BASE_PESSOA+nome)
    exibe_resultado_request(resultado)

    resultado = requests.delete(BASE_PESSOA+nome)
    exibe_resultado_request(resultado)

    resultado = requests.get(BASE_PESSOA+nome)
    exibe_resultado_request(resultado)

    resultado = requests.get(BASE_PESSOA)
    exibe_resultado_request(resultado)

    print("*"*20)
