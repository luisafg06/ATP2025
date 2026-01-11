import numpy as np
from config import (NUM_MEDICOS, TAXA_CHEGADA, TEMPO_MEDIO_CONSULTA, 
                   TEMPO_SIMULACAO, DISTRIBUICAO_TEMPO_CONSULTA, STD_NORMAL,
                   CHEGADA, SAIDA)
from models import *
from queue_utils import enqueue, dequeue, queue_empty
from distributions import gera_intervalo_tempo_chegada, gera_tempo_consulta
from statistics import media_ponderada_tempo


def simula(
    num_medicos=NUM_MEDICOS,
    taxa_chegada_por_minuto=TAXA_CHEGADA,
    tempo_medio_consulta=TEMPO_MEDIO_CONSULTA,
    tempo_simulacao=TEMPO_SIMULACAO,
    distribuicao_tempo_consulta=DISTRIBUICAO_TEMPO_CONSULTA,
    std_normal=STD_NORMAL,
    seed=None,
    pessoas=None,
    verbose=True,
):
    if seed is not None:
        np.random.seed(int(seed))

    tempo_atual = 0.0
    contadorDoentes = 1
    queueEventos = []
    queue = []
    doentes_atendidos = 0

    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(int(num_medicos))]

    chegadas = {}
    inicios = {}
    saidas = {}
    servicos = {}

    doente_pessoa = {}
    doente_idade = {}
    doente_prioritario = {}

    serie_fila = [(0.0, 0)]
    serie_ocup = [(0.0, 0.0)]
    ultimo_fila = 0
    ultimo_ocup = 0.0

    tempo_atual = tempo_atual + gera_intervalo_tempo_chegada(taxa_chegada_por_minuto)
    while tempo_atual < float(tempo_simulacao):
        doente = f"d{contadorDoentes}"
        contadorDoentes = contadorDoentes + 1

        chegadas[doente] = float(tempo_atual)

        idade = None
        prioritario = False
        p = None
        if pessoas is not None and len(pessoas) > 0:
            idx = (contadorDoentes - 2) % len(pessoas)
            p = pessoas[idx]
            if isinstance(p, dict):
                doente_pessoa[doente] = p
                idade_val = p.get("idade", None)
                try:
                    if idade_val is not None:
                        idade = float(idade_val)
                except Exception:
                    idade = None
        if idade is not None and idade > 65.0:
            prioritario = True
        doente_idade[doente] = idade
        doente_prioritario[doente] = prioritario

        queueEventos = enqueue(queueEventos, (float(tempo_atual), CHEGADA, doente))
        tempo_atual = tempo_atual + gera_intervalo_tempo_chegada(taxa_chegada_por_minuto)

    tempo_atual = 0.0

    while not queue_empty(queueEventos):
        ev, queueEventos = dequeue(queueEventos)
        tempo_atual, tipo, doente = ev

        if tipo == CHEGADA:
            medico_livre = None
            i = 0
            while i < len(medicos) and medico_livre is None:
                if not m_ocupado(medicos[i]):
                    medico_livre = i
                i = i + 1

            if medico_livre is not None:
                medico = medicos[medico_livre]
                medico = mOcupa(medico)
                medico = mInicioConsulta(medico, tempo_atual)
                medico = mDoenteCorrente(medico, doente)
                medicos[medico_livre] = medico

                inicios[doente] = float(tempo_atual)
                tempo_consulta = gera_tempo_consulta(tempo_medio_consulta, distribuicao_tempo_consulta, std_normal)
                servicos[doente] = float(tempo_consulta)
                queueEventos = enqueue(queueEventos, (float(tempo_atual + tempo_consulta), SAIDA, doente))
            else:
                prioritario = False
                if doente in doente_prioritario:
                    prioritario = bool(doente_prioritario[doente])
                idade = None
                if doente in doente_idade:
                    idade = doente_idade[doente]

                item = (doente, float(tempo_atual), prioritario, idade)
                if prioritario:
                    j = 0
                    while j < len(queue) and bool(queue[j][2]) is True:
                        j = j + 1
                    queue.insert(j, item)
                else:
                    queue.append(item)

        elif tipo == SAIDA:
            doentes_atendidos = doentes_atendidos + 1
            saidas[doente] = float(tempo_atual)

            idx_medico = None
            i = 0
            while i < len(medicos) and idx_medico is None:
                if m_doente_corrente(medicos[i]) == doente:
                    idx_medico = i
                i = i + 1

            if idx_medico is not None:
                medico = medicos[idx_medico]
                inicio = float(m_inicio_consulta(medico))
                fim = float(tempo_atual)

                t0 = float(inicio)
                t1 = float(fim)
                if t0 < 0.0:
                    t0 = 0.0
                if t1 > float(tempo_simulacao):
                    t1 = float(tempo_simulacao)

                delta = 0.0
                if t1 > t0:
                    delta = float(t1 - t0)

                medico = mSomaTempoOcupado(medico, delta)

                medico = mOcupa(medico)
                medico = mDoenteCorrente(medico, None)
                medicos[idx_medico] = medico

                if len(queue) > 0:
                    prox = queue.pop(0)
                    prox_doente = prox[0]

                    medico = medicos[idx_medico]
                    medico = mOcupa(medico)
                    medico = mInicioConsulta(medico, tempo_atual)
                    medico = mDoenteCorrente(medico, prox_doente)
                    medicos[idx_medico] = medico

                    inicios[prox_doente] = float(tempo_atual)
                    tempo_consulta = gera_tempo_consulta(tempo_medio_consulta, distribuicao_tempo_consulta, std_normal)
                    servicos[prox_doente] = float(tempo_consulta)
                    queueEventos = enqueue(queueEventos, (float(tempo_atual + tempo_consulta), SAIDA, prox_doente))

        ocupados = 0
        i = 0
        while i < len(medicos):
            if m_ocupado(medicos[i]):
                ocupados = ocupados + 1
            i = i + 1

        frac = ocupados / float(len(medicos)) if len(medicos) > 0 else 0.0

        t_reg = float(tempo_atual)
        if t_reg <= float(tempo_simulacao):
            ultimo_fila = int(len(queue))
            ultimo_ocup = float(frac)
            serie_fila.append((t_reg, ultimo_fila))
            serie_ocup.append((t_reg, ultimo_ocup))

    if len(serie_fila) > 0:
        t_last = float(serie_fila[-1][0])
        if t_last < float(tempo_simulacao):
            serie_fila.append((float(tempo_simulacao), int(ultimo_fila)))
    if len(serie_ocup) > 0:
        t_last = float(serie_ocup[-1][0])
        if t_last < float(tempo_simulacao):
            serie_ocup.append((float(tempo_simulacao), float(ultimo_ocup)))

    esperas = []
    tempos_servico = []
    tempos_totais = []

    for d in chegadas.keys():
        if d in inicios:
            esperas.append(float(inicios[d] - chegadas[d]))
        if d in servicos:
            tempos_servico.append(float(servicos[d]))
        if d in saidas:
            tempos_totais.append(float(saidas[d] - chegadas[d]))

    media_espera = float(np.mean(esperas)) if len(esperas) > 0 else 0.0
    media_servico = float(np.mean(tempos_servico)) if len(tempos_servico) > 0 else 0.0
    media_total = float(np.mean(tempos_totais)) if len(tempos_totais) > 0 else 0.0

    max_fila = 0
    i = 0
    while i < len(serie_fila):
        if int(serie_fila[i][1]) > max_fila:
            max_fila = int(serie_fila[i][1])
        i = i + 1
    fila_media = media_ponderada_tempo([(t, float(v)) for (t, v) in serie_fila], float(tempo_simulacao))

    ocup_por_medico = {}
    soma_ocup = 0.0
    i = 0
    while i < len(medicos):
        tbusy = float(m_tempo_ocupado(medicos[i]))
        soma_ocup = soma_ocup + tbusy
        ocup_por_medico[m_id(medicos[i])] = 100.0 * (tbusy / float(tempo_simulacao)) if float(tempo_simulacao) > 0 else 0.0
        i = i + 1

    ocup_global = 0.0
    if len(medicos) > 0 and float(tempo_simulacao) > 0:
        ocup_global = 100.0 * (soma_ocup / (float(len(medicos)) * float(tempo_simulacao)))

    res = {
        "parametros": {
            "num_medicos": int(num_medicos),
            "taxa_chegada_por_minuto": float(taxa_chegada_por_minuto),
            "lambda_por_hora": float(taxa_chegada_por_minuto) * 60.0,
            "tempo_medio_consulta": float(tempo_medio_consulta),
            "tempo_simulacao": float(tempo_simulacao),
            "distribuicao": str(distribuicao_tempo_consulta),
            "std_normal": float(std_normal),
            "seed": seed,
        },
        "medicos": medicos,
        "doentes_atendidos": int(doentes_atendidos),
        "estatisticas": {
            "tempo_medio_espera": float(media_espera),
            "tempo_medio_consulta": float(media_servico),
            "tempo_medio_na_clinica": float(media_total),
            "fila_media": float(fila_media),
            "fila_maxima": int(max_fila),
            "ocupacao_global_pct": float(ocup_global),
            "ocupacao_por_medico_pct": ocup_por_medico,
        },
        "series": {
            "fila": serie_fila,
            "ocupacao": serie_ocup,
        },
        "doentes": {
            "chegadas": chegadas,
            "inicios": inicios,
            "saidas": saidas,
            "servicos": servicos,
            "idades": doente_idade,
            "prioritario": doente_prioritario,
            "pessoas": doente_pessoa,
        }
    }
    
    if verbose:
        print(f"Doentes atendidos: {doentes_atendidos}")

    return res
