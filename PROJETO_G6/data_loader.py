import json
import os

def carrega_pessoas(path):
    pessoas = []
    if os.path.exists(path):
        f = open(path, encoding="utf-8")
        conteudo = f.read()
        f.close()
        if conteudo != "":
            data = json.loads(conteudo)
            if type(data) == list:
                pessoas = data
    return pessoas