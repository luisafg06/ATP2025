# Medical Clinic Simulation

Simulação de uma clínica médica no âmbito da unidade curricular **Algoritmos e Técnicas de Programação**, da **Licenciatura em Engenharia Biomédica (2.º ano)** – Universidade do Minho.

---

## Objetivo do Projeto

O objetivo deste projeto é desenvolver uma aplicação em Python que simule o funcionamento de uma clínica médica, modelando:
- a chegada de doentes,
- o atendimento por médicos,
- a formação de filas de espera,
- e a recolha de métricas estatísticas relevantes.

A aplicação permite analisar o comportamento do sistema perante diferentes parâmetros, como a taxa de chegada de doentes, o número de médicos e a distribuição do tempo de consulta.

---

## Modelo de Simulação

A simulação segue um modelo de **eventos discretos**, onde os principais eventos são:

- **CHEGADA**: um novo doente chega à clínica;
- **SAÍDA**: termina a consulta de um doente.

### Chegada de Doentes
- As chegadas seguem um **processo de Poisson**, implementado através de uma distribuição **exponencial** para os intervalos entre chegadas.
- O parâmetro λ representa a taxa média de chegada de doentes (doentes/hora).

### Atendimento Médico
- Cada médico atende apenas um doente de cada vez.
- Se houver um médico disponível, o atendimento é imediato.
- Caso contrário, o doente entra numa **fila de espera (FIFO)**.
- Doentes com idade superior a 65 anos são tratados como **prioritários**, sendo colocados à frente na fila.

### Tempo de Consulta
O tempo de consulta pode seguir uma das seguintes distribuições:
- Exponencial
- Normal
- Uniforme

---

## Métricas Calculadas

Durante a simulação são recolhidas as seguintes métricas:

- Tempo médio de espera dos doentes
- Tempo médio de consulta
- Tempo médio total na clínica
- Tamanho médio da fila de espera (média temporal)
- Tamanho máximo da fila
- Ocupação global dos médicos (%)
- Ocupação individual por médico (%)
- Número total de doentes atendidos

As médias temporais (fila e ocupação) são calculadas de forma **ponderada no tempo**, garantindo maior rigor estatístico.

---

## Gráficos Gerados

A aplicação gera automaticamente os seguintes gráficos:

1. Evolução do tamanho da fila de espera ao longo do tempo  
2. Evolução da taxa de ocupação dos médicos ao longo do tempo  
3. Relação entre o tamanho médio da fila e a taxa de chegada de doentes (λ entre 10 e 30)

---

## Interface Gráfica

A aplicação dispõe de uma interface gráfica desenvolvida com **FreeSimpleGUI**, permitindo:

- Alterar os parâmetros da simulação
- Executar a simulação
- Visualizar os resultados estatísticos
- Visualizar os gráficos gerados

---

## Estrutura do Projeto

O projeto está organizado de forma modular, separando claramente a lógica da simulação, a interface gráfica e a análise de resultados.
```text
projeto_ATP_G6/
├── main.py               # Ponto de entrada da aplicação
├── gui.py                # Interface gráfica (FreeSimpleGUI)
├── simulation.py         # Motor principal da simulação
├── models.py             # Estruturas de dados (médicos e eventos)
├── queue_utils.py        # Gestão de filas (eventos e fila de espera)
├── distributions.py      # Geração de distribuições estatísticas
├── statistics.py         # Cálculo de métricas estatísticas
├── plots.py              # Geração e visualização de gráficos
├── data_loader.py        # Carregamento de dados externos
├── pessoas.json          # Dataset de pessoas (opcional)
├── config.py             # Parâmetros default da simulação
└── README.md             # Relatório técnico do projeto


