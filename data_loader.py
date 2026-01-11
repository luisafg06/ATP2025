# data_loader.py
"""
Funções para carregar dados externos (pessoas.json)
"""
import json
import os


def carrega_pessoas(path):
    """Carrega dados de pessoas de um ficheiro JSON"""
    pessoas = []
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    pessoas = data
        except Exception:
            pessoas = []
    return pessoas
