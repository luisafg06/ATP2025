# Medical Clinic Simulation

Simulação de uma clínica médica recorrendo a **simulação de eventos discretos**, desenvolvida no âmbito da unidade curricular **Algoritmos e Técnicas de Programação**, da **Licenciatura em Engenharia Biomédica (2.º ano)** – Universidade do Minho.

---

## Objetivo do Projeto

O objetivo deste projeto é desenvolver uma aplicação em Python que simule o funcionamento de uma clínica médica, modelando:
- A chegada de doentes à clínica
- O atendimento por parte dos médicos
- A formação e gestão de filas de espera
- A recolha de métricas estatísticas relevantes

A aplicação permite analisar o comportamento do sistema perante diferentes parâmetros, como a taxa de chegada de doentes (λ), o número de médicos disponíveis e a distribuição do tempo de consulta.

---

## Instalação e Dependências

### Bibliotecas Necessárias

O projeto requer as seguintes bibliotecas Python:

```bash
pip install numpy
pip install matplotlib
pip install FreeSimpleGUI
```

**IMPORTANTE:** Sem estas bibliotecas, o programa não irá executar. Certifica-te de que estão todas instaladas antes de correr a aplicação.

---

## Como Executar

1. Certifica-te de que todas as dependências estão instaladas
2. Executa o ficheiro principal:

```bash
python main.py
```

3. A interface gráfica será aberta automaticamente
4. Configura os parâmetros desejados
5. Clica em "Executar Simulação"

---

## Modelo de Simulação

A simulação segue um modelo de **eventos discretos**, onde os principais eventos são:

- **CHEGADA**: um novo doente chega à clínica
- **SAÍDA**: termina a consulta de um doente

### Chegada de Doentes

- As chegadas seguem um **processo de Poisson**, implementado através de uma distribuição **exponencial** para os intervalos entre chegadas
- O parâmetro **λ** (lambda) representa a taxa média de chegada de doentes (doentes/hora)
- **Relação estatística:** Se as chegadas seguem Poisson, os intervalos entre chegadas seguem uma distribuição exponencial com parâmetro 1/λ

### Atendimento Médico

- Cada médico atende apenas **um doente de cada vez**
- Se houver um médico disponível, o atendimento é **imediato**
- Caso contrário, o doente entra numa **fila de espera**
- **Exceção:** Doentes com idade superior a 65 anos são tratados como **prioritários**, sendo colocados à frente dos doentes não prioritários na fila

### Tempo de Consulta

O tempo de consulta pode seguir uma das seguintes distribuições:

| Distribuição | Descrição | Realismo |
|--------------|-----------|----------|
| **Exponencial** | Gera maioritariamente tempos curtos, com ocasionais consultas mais longas | Mais realista |
| **Normal** | Todas as consultas têm duração próxima da média (com desvio padrão configurável) | Realista para cenários controlados |
| **Uniforme** | Todas as consultas têm duração uniformemente distribuída entre 50% abaixo e 50% acima da média | Menos realista |

**Nota:** Por defeito, se a distribuição não for reconhecida, o sistema assume **exponencial**.

---

## Estrutura do Projeto

```
PROJETO_grupo6/
├── main.py                    # Ponto de entrada da aplicação
├── gui.py                     # Interface gráfica (FreeSimpleGUI)
├── simulation.py              # Motor principal da simulação
├── models.py                  # Estruturas de dados (médicos e eventos)
├── queueevents_utils.py       # Gestão da fila de eventos
├── distributions.py           # Geração de distribuições estatísticas
├── mediaponderada.py          # Cálculo de médias ponderadas temporais
├── plots.py                   # Geração e visualização de gráficos
├── data_loader.py             # Carregamento de dados externos (pessoas.json)
├── pessoas.json               # Dataset de pessoas (opcional)
├── config.py                  # Parâmetros default da simulação
└── README.md                  # Documentação do projeto
```

### Estruturas de Dados Principais

#### Item da Fila de Eventos
```python
# evento = (tempo, tipo, doente)
# Exemplo: [15.5, "chegada", "d3"]
```

#### Item da Fila de Espera
```python
# item_fila = (doente, tempo_chegada, prioritario, idade)
# Exemplo: ("d7", 150.0, True, 70)
```

#### Médico
```python
# medico = [id, ocupado, doente_corrente, tempo_ocupado, inicio_consulta]
# Exemplo: ["m0", True, "d5", 120.5, 100.0]
```

---

## Funcionalidades Implementadas

### 1. Simulação de Eventos Discretos
- Motor de simulação baseado em fila de eventos ordenada por tempo
- Tratamento de eventos de chegada e saída
- Gestão automática da disponibilidade dos médicos

### 2. Sistema de Filas
- **Fila de eventos:** Todos os eventos futuros ordenados cronologicamente
- **Fila de espera:** Doentes aguardando por médico disponível, com suporte a prioridades

### 3. Sistema de Prioridades
- Doentes com **idade > 65 anos** têm prioridade no atendimento
- Inserção inteligente na fila: prioritários ficam à frente dos não prioritários
- Lógica implementada: percorre a fila enquanto encontrar outros prioritários, depois insere

### 4. Integração com Dataset Real
- Suporte para ficheiro `pessoas.json` com dados reais de pacientes
- Cada doente simulado é associado a uma pessoa do dataset (com idade, nome, etc.)
- Sistema cíclico: `índice = (contadorDoentes - 2) % len(pessoas)`
- **Se o ficheiro não existir:** O programa funciona normalmente, mas sem prioridades por idade

### 5. Reprodutibilidade (Seed)
- Opção de definir um **seed** para o gerador de números aleatórios
- Com o mesmo seed e mesmos parâmetros, os resultados são **idênticos**
- Útil para comparações estatísticas e debugging
- **Sem seed:** Cada execução gera resultados diferentes (comportamento aleatório)

---

## Métricas Calculadas

Durante a simulação são recolhidas as seguintes métricas:

| Métrica | Descrição |
|---------|-----------|
| **Tempo médio de espera** | Tempo médio que os doentes aguardam na fila antes de serem atendidos |
| **Tempo médio de consulta** | Duração média das consultas realizadas |
| **Tempo médio na clínica** | Tempo total médio que cada doente passa na clínica (espera + consulta) |
| **Tamanho médio da fila** | Média temporal ponderada do número de doentes em espera |
| **Tamanho máximo da fila** | Número máximo de doentes em fila simultânea |
| **Ocupação global dos médicos** | Percentagem de tempo em que os médicos estão ocupados (agregado) |
| **Ocupação por médico** | Percentagem de tempo ocupado para cada médico individualmente |
| **Doentes atendidos** | Número total de doentes que completaram consulta |

### Média Ponderada Temporal

A métrica **"Tamanho médio da fila"** é calculada usando uma **média ponderada no tempo**, não uma simples média aritmética.

**Por quê?**  
Ter 2 pessoas na fila durante 10 minutos tem um impacto diferente de ter 2 pessoas durante 2 horas. A média ponderada considera quanto tempo cada estado da fila durou.

**Fórmula:**
```
média_ponderada = Σ(valor × duração) / tempo_total
```

**Exemplo:**
- De 0 a 10 min: 2 pessoas na fila → contribui 2 × 10 = 20
- De 10 a 30 min: 5 pessoas na fila → contribui 5 × 20 = 100
- Total: (20 + 100) / 30 = 4.0 pessoas (média)


---

## Gráficos Gerados

A aplicação gera automaticamente três tipos de gráficos:

### 1. Evolução do Tamanho da Fila
- **Eixo X:** Tempo (minutos)
- **Eixo Y:** Número de pessoas na fila
- Mostra como a fila de espera evolui ao longo da simulação

### 2. Evolução da Ocupação dos Médicos
- **Eixo X:** Tempo (minutos)
- **Eixo Y:** Ocupação (%)
- **Limite do eixo Y:** 0% a 110% (margem estética)
- Mostra a percentagem de médicos ocupados em cada momento

### 3. Relação Fila vs Taxa de Chegada (λ)
- **Eixo X:** λ (doentes/hora)
- **Eixo Y:** Tamanho médio da fila
- Executa múltiplas simulações variando λ de 10 a 30 doentes/hora
- Cada ponto é a média de 10 repetições (para reduzir variabilidade)
- Útil para identificar pontos de saturação do sistema

---

## Interface Gráfica

A aplicação dispõe de uma interface gráfica desenvolvida com **FreeSimpleGUI**, permitindo:

### Painel Esquerdo - Configuração
- **λ (doentes/hora):** Taxa de chegada de doentes
- **Nº médicos:** Número de médicos disponíveis
- **Distribuição:** Tipo de distribuição do tempo de consulta (exponencial/normal/uniforme)
- **Média consulta (min):** Tempo médio de duração da consulta
- **Std normal (min):** Desvio padrão (apenas para distribuição normal)
- **Tempo simulação (min):** Duração total da simulação
- **Seed (opcional):** Seed para reprodutibilidade

### Botões Disponíveis
- **Executar Simulação:** Corre a simulação com os parâmetros configurados
- **Gráfico: Fila:** Mostra a evolução da fila de espera
- **Gráfico: Ocupação:** Mostra a evolução da ocupação dos médicos
- **Fila vs λ (10-30):** Gera o gráfico
- **Sair:** Fecha a aplicação

### Painel Direito - Resultados
- Exibe todos os parâmetros utilizados
- Apresenta as estatísticas calculadas
- Mostra a ocupação individual de cada médico

---

## Extras Implementados

Funcionalidades adicionais desenvolvidas pelo grupo:

### 1. Sistema de Prioridades para Idosos
- Doentes com idade > 65 anos têm atendimento prioritário
- Implementação: inserção inteligente na fila de espera
- Baseado em dados reais do ficheiro `pessoas.json`

### 2. Média Ponderada Temporal
- Cálculo correto de médias temporais (fila)
- Essencial para análise rigorosa de sistemas de filas
- Implementado no módulo `mediaponderada.py`

### 3. Sistema de Seed
- Permite reproduzir exatamente as mesmas simulações
- Fundamental para validação estatística
- Facilita debugging e comparações

### 4. Integração com Dataset Real
- Cada doente simulado corresponde a uma pessoa real do dataset
- Atributos: nome, idade, género, etc.
- Melhora o realismo da simulação

### 5. Interface Gráfica Intuitiva
- Fácil configuração de parâmetros
- Visualização imediata de resultados
- Geração de gráficos com um clique

### 6. Validação de Inputs
- Se um parâmetro não estiver em formato válido (ex: "40/20" em vez de número), o sistema assume o **valor default** definido em `config.py`
- Impede crashes e garante funcionamento robusto

---

## Notas Técnicas Importantes

### Valores Default
Se algum parâmetro não for preenchido corretamente na interface (valores não numéricos, vazios, etc.), o sistema assume os valores configurados em `config.py`:

```python
NUM_MEDICOS = 3
TAXA_CHEGADA = 10 / 60  # 10 doentes/hora
TEMPO_MEDIO_CONSULTA = 15  # minutos
TEMPO_SIMULACAO = 8 * 60  # 480 minutos (8 horas)
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"
STD_NORMAL = 5.0
```

### Indexação
- **Médicos e doentes:** A numeração começa em 0 (índice Python padrão)
- **Médicos:** m0, m1, m2, ...
- **Doentes:** d1, d2, d3, ... (contador começa em 1 para legibilidade)


### Distribuição Normal - Valores Negativos

Quando se usa a distribuição **normal**, teoricamente podem ser gerados valores negativos. O código trata este caso:

```python
if dist == "normal":
    t = float(np.random.normal(med, float(std)))
    if t < 0:
        t = 0.0  # Corrige valores negativos
```

### Limites Temporais nas Consultas

O código garante que consultas que ultrapassem o `tempo_simulacao` são truncadas no cálculo da ocupação:

```python
if t1 > float(tempo_simulacao):
    t1 = float(tempo_simulacao)
```

Isto assegura que o tempo de ocupação dos médicos não conta tempo após o tempo maximo da clínica.

---

## Conceitos de Estatística Aplicados

### Seed (Semente Aleatória)
- Sem seed: cada execução gera resultados diferentes (números verdadeiramente aleatórios)
- Com seed: a sequência de números "aleatórios" é sempre a mesma
- Exemplo: `seed=42` gera sempre a mesma sequência; `seed=100` gera outra sequência diferente
- Possível graças ao gerador `numpy.random`

### Desvio Padrão (Std)
- Na distribuição **normal**, o `std` define a dispersão em torno da média
- Quanto maior o std, maior a variabilidade dos tempos de consulta

---

## Resolução de Problemas

### Erro: "ModuleNotFoundError: No module named 'FreeSimpleGUI'"
**Solução:** Instala a biblioteca com `pip install FreeSimpleGUI`

### Erro: "ModuleNotFoundError: No module named 'numpy'"
**Solução:** Instala a biblioteca com `pip install numpy`

### O programa não mostra gráficos
**Solução:** Certifica-te de que `matplotlib` está instalado: `pip install matplotlib`

### Os resultados são sempre diferentes
**Solução:** Define um valor no campo "Seed (opcional)" para reproduzir os mesmos resultados

### Não tenho o ficheiro pessoas.json
**Solução:** O programa funciona sem este ficheiro, mas sem o sistema de prioridades por idade. 