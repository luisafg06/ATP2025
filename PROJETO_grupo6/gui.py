import os
import FreeSimpleGUI as sg
from config import NUM_MEDICOS, TEMPO_MEDIO_CONSULTA, TEMPO_SIMULACAO, DISTRIBUICAO_TEMPO_CONSULTA, STD_NORMAL
from simulation import simula
from data_loader import carrega_pessoas
import plots as p


DISTRIBUICOES_DISPONIVEIS = ["exponential", "normal", "uniform"]


def parse_int(s, default):
    v = default
    try:
        v = int(str(s).strip())
    except Exception:
        v = default
    return v


def parse_float(s, default):
    v = default
    try:
        v = float(str(s).strip())
    except Exception:
        v = default
    return v


def format_res(res):
    par = res["parametros"]
    est = res["estatisticas"]

    lines = []
    lines.append("=== Parâmetros ===")
    lines.append(f"λ (doentes/hora): {par['lambda_por_hora']:.2f}")
    lines.append(f"Nº médicos: {par['num_medicos']}")
    lines.append(f"Distribuição consulta: {par['distribuicao']}")
    lines.append(f"Média consulta (min): {par['tempo_medio_consulta']}")
    if str(par["distribuicao"]).strip().lower() == "normal":
        lines.append(f"Std normal (min): {par['std_normal']}")
    lines.append(f"Tempo simulação (min): {par['tempo_simulacao']}")
    lines.append("")
    lines.append("=== Resultados ===")
    lines.append(f"Doentes atendidos: {res['doentes_atendidos']}")
    lines.append(f"Tempo médio espera (min): {est['tempo_medio_espera']:.2f}")
    lines.append(f"Tempo médio consulta (min): {est['tempo_medio_consulta']:.2f}")
    lines.append(f"Tempo médio na clínica (min): {est['tempo_medio_na_clinica']:.2f}")
    lines.append(f"Fila média (média temporal): {est['fila_media']:.2f}")
    lines.append(f"Fila máxima: {est['fila_maxima']}")
    lines.append(f"Ocupação global (%): {est['ocupacao_global_pct']:.2f}")
    lines.append("")
    lines.append("=== Ocupação por médico (%) ===")
    for k in sorted(est["ocupacao_por_medico_pct"].keys()):
        lines.append(f"{k}: {est['ocupacao_por_medico_pct'][k]:.2f}")
    return "\n".join(lines)


def clinic_app():
    if sg is None:
        print("Erro: SimpleGUI não está instalado. Instala FreeSimpleGUI.")
        return

    sg.theme("LightGrey1")

    base_dir = os.path.dirname(__file__) if "__file__" in globals() else "."
    pessoas_path = os.path.join(base_dir, "pessoas.json")
    pessoas = carrega_pessoas(pessoas_path)

    col_esq = [
        [sg.Text("Medical Clinic Simulation", font=("Arial", 28))],
        [sg.Text("Parâmetros", font=("Arial", 18))],
        [sg.Text("λ (doentes/hora)", size=(18, 1)), sg.Input("10", key="-LAM-", size=(10, 1))],
        [sg.Text("Nº médicos", size=(18, 1)), sg.Input(str(NUM_MEDICOS), key="-NDOC-", size=(10, 1))],
        [sg.Text("Distribuição", size=(18, 1)), 
         sg.Combo(DISTRIBUICOES_DISPONIVEIS, default_value=DISTRIBUICAO_TEMPO_CONSULTA, 
                  key="-DIST-", readonly=True, size=(14, 1))],
        [sg.Text("Média consulta (min)", size=(18, 1)), 
         sg.Input(str(TEMPO_MEDIO_CONSULTA), key="-MEAN-", size=(10, 1))],
        [sg.Text("Std normal (min)", size=(18, 1)), 
         sg.Input(str(STD_NORMAL), key="-STD-", size=(10, 1))],
        [sg.Text("Tempo simulação (min)", size=(18, 1)), 
         sg.Input(str(TEMPO_SIMULACAO), key="-SIMT-", size=(10, 1))],
        [sg.Text("Seed (opcional)", size=(18, 1)), sg.Input("", key="-SEED-", size=(10, 1))],
        [sg.HSep(color="white")],
        [sg.Button("Executar Simulação", key="-RUN-", font=("Arial", 16))],
        [sg.Button("Gráfico: Fila", key="-PLOTQ-", font=("Arial", 14)),
         sg.Button("Gráfico: Ocupação", key="-PLOTO-", font=("Arial", 14))],
        [sg.Button("Fila vs λ (10-30)", key="-PLOTQL-", font=("Arial", 14))],
        [sg.HSep(color="white")],
        [sg.Button("Sair", key="-EXIT-", font=("Arial", 14))],
    ]

    col_dir = [
        [sg.Text("Resultados / Log", font=("Arial", 18))],
        [sg.Multiline("", key="-LOG-", size=(60, 24), font=("Consolas", 11))]
    ]

    layout = [[sg.Column(col_esq), sg.VSep(color="white"), sg.Column(col_dir)]]
    w = sg.Window("ClinicApp", layout, location=(60, 60), resizable=False, finalize=True)

    last_res = None
    stop = False
    
    while not stop:
        event, values = w.read()

        if event == sg.WIN_CLOSED or event == "-EXIT-":
            stop = True

        elif event == "-RUN-":
            lam_h = parse_float(values.get("-LAM-", "10"), 10.0)
            ndoc = parse_int(values.get("-NDOC-", str(NUM_MEDICOS)), NUM_MEDICOS)
            dist = str(values.get("-DIST-", DISTRIBUICAO_TEMPO_CONSULTA))
            mean = parse_float(values.get("-MEAN-", str(TEMPO_MEDIO_CONSULTA)), float(TEMPO_MEDIO_CONSULTA))
            std = parse_float(values.get("-STD-", str(STD_NORMAL)), float(STD_NORMAL))
            simt = parse_float(values.get("-SIMT-", str(TEMPO_SIMULACAO)), float(TEMPO_SIMULACAO))

            seed_txt = str(values.get("-SEED-", "")).strip()
            seed = None
            if seed_txt != "":
                seed = parse_int(seed_txt, 0)

            taxa_min = float(lam_h) / 60.0
            last_res = simula(
                num_medicos=max(0, ndoc),
                taxa_chegada_por_minuto=taxa_min,
                tempo_medio_consulta=mean,
                tempo_simulacao=simt,
                distribuicao_tempo_consulta=dist,
                std_normal=std,
                seed=seed,
                pessoas=pessoas if len(pessoas) > 0 else None,
                verbose=False,
            )
            w["-LOG-"].update(format_res(last_res))

        elif event == "-PLOTQ-":
            if last_res is not None:
                p.show_plot("Fila de Espera", p.fig_fila, last_res)
            else:
                w["-LOG-"].update("Executa uma simulação primeiro (botão: Executar Simulação).")

        elif event == "-PLOTO-":
            if last_res is not None:
                p.show_plot("Ocupação dos Médicos", p.fig_ocupacao, last_res)
            else:
                w["-LOG-"].update("Executa uma simulação primeiro (botão: Executar Simulação).")

        elif event == "-PLOTQL-":
            lam_h = parse_float(values.get("-LAM-", "10"), 10.0)
            ndoc = parse_int(values.get("-NDOC-", str(NUM_MEDICOS)), NUM_MEDICOS)
            dist = str(values.get("-DIST-", DISTRIBUICAO_TEMPO_CONSULTA))
            mean = parse_float(values.get("-MEAN-", str(TEMPO_MEDIO_CONSULTA)), float(TEMPO_MEDIO_CONSULTA))
            std = parse_float(values.get("-STD-", str(STD_NORMAL)), float(STD_NORMAL))
            simt = parse_float(values.get("-SIMT-", str(TEMPO_SIMULACAO)), float(TEMPO_SIMULACAO))

            seed_txt = str(values.get("-SEED-", "")).strip()
            seed = None
            if seed_txt != "":
                seed = parse_int(seed_txt, 0)

            base = {
                "num_medicos": max(0, ndoc),
                "tempo_medio_consulta": mean,
                "tempo_simulacao": simt,
                "distribuicao": dist,
                "std_normal": std,
                "seed": seed,
            }
            p.show_plot("Fila vs λ", p.fig_fila_vs_lambda, base, 
                       pessoas if len(pessoas) > 0 else None, 10, 30, 2, 10)

    w.close()
