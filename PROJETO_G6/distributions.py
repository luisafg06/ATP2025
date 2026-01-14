import numpy as np
from config import TEMPO_MEDIO_CONSULTA, DISTRIBUICAO_TEMPO_CONSULTA, STD_NORMAL


def gera_intervalo_tempo_chegada(taxa_chegada_por_minuto):
    rate = float(taxa_chegada_por_minuto)
    inter = float("inf")
    if rate > 0:
        inter = float(np.random.exponential(1.0 / rate))
    return inter


def gera_tempo_consulta(media=TEMPO_MEDIO_CONSULTA, 
                        distribuicao=DISTRIBUICAO_TEMPO_CONSULTA, 
                        std=STD_NORMAL):
    dist = str(distribuicao).strip().lower()
    med = float(media)

    t = 0.0
    if dist == "exponential":
        t = float(np.random.exponential(med))
    elif dist == "uniform":
        t = float(np.random.uniform(0.5 * med, 1.5 * med))
    elif dist == "normal":
        t = float(np.random.normal(med, float(std)))
        if t < 0:
            t = 0.0
    else:
        t = float(np.random.exponential(med))
    return t
