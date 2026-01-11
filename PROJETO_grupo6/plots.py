
import os
import numpy as np
import matplotlib.pyplot as plt
import FreeSimpleGUI as sg
from config import NUM_MEDICOS, TEMPO_MEDIO_CONSULTA, TEMPO_SIMULACAO, DISTRIBUICAO_TEMPO_CONSULTA, STD_NORMAL
from simulation import simula


def fig_fila(res):
    serie = res["series"]["fila"]
    xs = [t for (t, _) in serie]
    ys = [v for (_, v) in serie]
    fig = plt.figure()
    plt.plot(xs, ys)
    plt.title("Evolução do tamanho da fila de espera")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Tamanho da fila")
    plt.grid(True)
    return fig


def fig_ocupacao(res):
    serie = res["series"]["ocupacao"]
    xs = [t for (t, _) in serie]
    ys = [v * 100.0 for (_, v) in serie]
    fig = plt.figure()
    plt.plot(xs, ys)
    plt.title("Evolução da ocupação dos médicos")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Ocupação (%)")
    plt.ylim(0, 150)
    plt.grid(True)
    return fig


def fig_fila_vs_lambda(base_params, pessoas=None, lam_min=10, lam_max=30, step=2, reps=10):
    lambdas = []
    medias = []

    lam = int(lam_min)
    while lam <= int(lam_max):
        lambdas.append(int(lam))

        vals = []
        r = 0
        while r < int(reps):
            seed0 = base_params.get("seed", None)
            seed_use = None
            if seed0 is not None:
                seed_use = int(seed0) + r + (lam * 1000)

            rr = simula(
                num_medicos=base_params.get("num_medicos", NUM_MEDICOS),
                taxa_chegada_por_minuto=float(lam) / 60.0,
                tempo_medio_consulta=base_params.get("tempo_medio_consulta", TEMPO_MEDIO_CONSULTA),
                tempo_simulacao=base_params.get("tempo_simulacao", TEMPO_SIMULACAO),
                distribuicao_tempo_consulta=base_params.get("distribuicao", DISTRIBUICAO_TEMPO_CONSULTA),
                std_normal=base_params.get("std_normal", STD_NORMAL),
                seed=seed_use,
                pessoas=pessoas,
                verbose=False,
            )
            vals.append(float(rr["estatisticas"]["fila_media"]))
            r = r + 1

        medias.append(float(np.mean(vals)) if len(vals) > 0 else 0.0)
        lam = lam + int(step)

    fig = plt.figure()
    plt.plot(lambdas, medias)
    plt.title("Relação: tamanho médio da fila vs taxa de chegada (λ)")
    plt.xlabel("λ (doentes/hora)")
    plt.ylabel("Tamanho médio da fila (média temporal)")
    plt.grid(True)
    return fig


def save_fig_png(fig, fpath):
    fig.savefig(fpath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fpath


def show_plot(title, fig_func, *args, **kwargs):
    if sg is None:
        return
    fig = fig_func(*args, **kwargs)
    tmp = os.path.join(os.path.dirname(__file__) if "__file__" in globals() else ".", "_tmp_plot.png")
    save_fig_png(fig, tmp)

    layout = [
        [sg.Text(title, font=("Arial", 20))],
        [sg.Image(filename=tmp)],
        [sg.Button("Fechar", font=("Arial", 14))]
    ]
    w = sg.Window(title, layout, finalize=True)
    done = False
    while not done:
        ev, _ = w.read()
        if ev in (sg.WIN_CLOSED, "Fechar"):
            done = True
    w.close()

    if os.path.exists(tmp):
        try:
            os.remove(tmp)
        except Exception:
            pass
