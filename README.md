# Projeto 1 — Laboratório de Ciência de Dados

**Grupo 1 | Análise Exploratória de Dados — NBA**

## 1. Apresentação

Este projeto foi desenvolvido para a disciplina de **Laboratório de Ciência de Dados**, com o objetivo de realizar uma análise exploratória e estatística das equipes **Los Angeles Lakers** e **Denver Nuggets**, utilizando o conjunto de dados `stats_times_regular_final.csv`.

A aplicação consiste em um dashboard web interativo, desenvolvido em Python com Flask, que permite visualizar estatísticas, avaliar a qualidade dos dados, identificar valores atípicos (*outliers*) e comparar o desempenho das equipes.

As análises são realizadas por equipe e por variável, preservando as observações originais.

## 2. Objetivos

- Explorar a estrutura, os tipos e a qualidade dos dados.
- Calcular medidas de tendência central, dispersão e assimetria.
- Visualizar a distribuição das estatísticas por meio de gráficos interativos.
- Identificar valores atípicos utilizando diferentes métodos estatísticos e algoritmos de detecção de anomalias.
- Comparar a concordância entre os métodos de detecção.
- Interpretar criticamente os resultados encontrados.
- Elaborar uma síntese estatística comparativa entre Lakers e Nuggets.

## 3. Base de dados

**Arquivo:** `data/stats_times_regular_final.csv`

**Unidade de análise:** uma observação corresponde às estatísticas de uma equipe em um jogo.

O conjunto original é preservado, e o processamento seleciona exclusivamente os registros das duas equipes do Grupo 1.

### Variáveis analisadas

| Variável | Descrição |
|---|---|
| PTS | Pontos marcados |
| REB | Rebotes totais |
| AST | Assistências |
| STL | Roubos de bola |
| BLK | Bloqueios |
| PF | Faltas pessoais |
| FG3M | Cestas de três pontos convertidas |

### Preparação dos dados

O processamento é realizado em `analytics.py` e inclui:

- Filtragem dos registros das equipes selecionadas.
- Conversão de `GAME_DATE` para formato de data.
- Conversão explícita das variáveis estatísticas para valores numéricos.
- Renomeação de colunas para facilitar o processamento, incluindo `Game_ID` para `id_jogo`, `TEAM_NAME` para `time` e `GAME_DATE` para `data_jogo`.
- Identificação de valores ausentes, duplicatas e inconsistências.

Os valores atípicos não são removidos automaticamente, pois podem representar desempenhos esportivos legítimos.

## 4. Funcionalidades do dashboard

### 4.1. Visão geral e qualidade dos dados

Apresenta informações sobre a estrutura do conjunto de dados, dicionário de variáveis, tipos, valores ausentes, duplicatas, registros das equipes e possíveis inconsistências.

### 4.2. Estatística descritiva

Para cada equipe e variável, são calculadas medidas como:

- Média, mediana e moda.
- Mínimo, máximo e amplitude.
- Variância e desvio padrão amostral.
- Primeiro e terceiro quartis.
- Amplitude interquartil (IQR).
- Coeficiente de variação (CV).
- Assimetria ajustada.
- Limites para identificação de outliers pela regra de Tukey.

### 4.3. Visualizações

O dashboard apresenta gráficos interativos com Plotly, incluindo distribuições, histogramas com estimativa de densidade por kernel (KDE), boxplots e visualizações comparativas.

Uma tabela complementar ao boxplot apresenta as principais medidas estatísticas, incluindo quartis, limites, média, mediana, moda e extremos.

### 4.4. Detecção de outliers

São utilizados sete métodos:

| Método | Critério utilizado |
|---|---|
| Z-score | Valores com \|z\| superior a 3 |
| IQR | Valores fora dos limites de 1,5 × IQR |
| Grubbs | Teste de um extremo, com α = 0,05 |
| ECOD empírico | Pontuação univariada baseada nas caudas da distribuição |
| K-NN | Observações com maiores distâncias aos vizinhos |
| DBSCAN | Observações classificadas como ruído |
| LOF | Observações com densidade local discrepante |

Os métodos possuem pressupostos e parâmetros distintos. Portanto, diferenças entre seus resultados são esperadas.

### 4.5. Concordância entre detectores

A seção de concordância identifica os jogos sinalizados por diferentes métodos e informa quantos detectores classificaram cada observação como atípica.

O objetivo é investigar a consistência das sinalizações, sem assumir que a concordância representa necessariamente uma classificação correta.

### 4.6. Interpretação crítica dos detectores

A interpretação é atualizada conforme a equipe e a variável selecionadas.

A seção apresenta as quantidades de outliers identificadas por método, os três pares de detectores com maior índice de Jaccard e uma interpretação contextualizada dos resultados.

O índice de Jaccard mede a sobreposição entre conjuntos de observações sinalizadas. Ele não representa acurácia, pois não há rótulos de referência para avaliação supervisionada.

### 4.7. Síntese estatística integrada

A seção de síntese final compara Lakers e Nuggets nas sete variáveis analisadas.

São apresentados indicadores de tendência central, dispersão, variabilidade relativa, assimetria e outliers, acompanhados de interpretações comparativas.

As diferenças observadas são **descritivas** e não devem ser interpretadas automaticamente como estatisticamente significativas.

## 5. Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Flask:** servidor web e API.
- **Pandas:** leitura, filtragem e manipulação dos dados.
- **NumPy:** operações numéricas.
- **SciPy:** cálculos estatísticos e KDE.
- **Scikit-learn:** K-NN, DBSCAN, LOF e padronização.
- **Plotly:** gráficos interativos.
- **HTML, CSS e JavaScript:** interface web.
- **unittest:** testes automatizados.

As dependências Python estão especificadas em `requirements.txt`.

## 6. Instalação e execução

### 6.1. Requisitos

- Python 3.10 ou superior, com dependências compatíveis.
- Gerenciador de pacotes `pip`.
- Navegador web.
- Acesso à internet para carregar os gráficos Plotly via CDN.

### 6.2. Linux / Ubuntu

Clone o repositório ou acesse a pasta do projeto.

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Execute a aplicação:

```bash
python app.py
```

Acesse no navegador:

**http://127.0.0.1:5000**

Para interromper o servidor, pressione `Ctrl+C` no terminal.

### 6.3. Windows

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative-o no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências e execute:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Acesse **http://127.0.0.1:5000**.

## 7. Estrutura do projeto

```text
proj_CD/
├── app.py
├── analytics.py
├── requirements.txt
├── README.md
├── data/
│   └── stats_times_regular_final.csv
├── templates/
│   └── index.html
└── tests/
    └── arquivos de testes automatizados
```

**Arquivos principais:**

- `app.py`: inicialização do Flask, rotas e respostas JSON.
- `analytics.py`: preparação dos dados, estatística descritiva e detecção de outliers.
- `templates/index.html`: interface do dashboard e visualizações.
- `data/`: conjunto de dados original.
- `tests/`: testes automatizados dos endpoints e funcionalidades estatísticas.

## 8. API

A aplicação disponibiliza os seguintes endpoints:

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/` | Página principal |
| GET | `/api/overview` | Visão geral dos dados |
| GET | `/api/data-quality` | Qualidade dos dados |
| GET | `/api/analysis` | Análise por equipe e variável |
| GET | `/api/summary` | Resumo de indicadores |
| GET | `/api/outlier-comparison` | Concordância entre detectores |
| GET | `/api/outlier-interpretation` | Interpretação crítica de outliers |
| GET | `/api/statistical-synthesis` | Síntese estatística comparativa |

### Exemplos

Análise de pontos dos Lakers:

```text
http://127.0.0.1:5000/api/analysis?team=Los%20Angeles%20Lakers&metric=PTS
```

Concordância de outliers dos Nuggets:

```text
http://127.0.0.1:5000/api/outlier-comparison?team=Denver%20Nuggets&metric=REB
```

Interpretação crítica:

```text
http://127.0.0.1:5000/api/outlier-interpretation?team=Los%20Angeles%20Lakers&metric=AST
```

Síntese estatística:

```text
http://127.0.0.1:5000/api/statistical-synthesis
```

## 9. Testes automatizados

Os testes utilizam `unittest` e verificam funcionalidades da aplicação, incluindo endpoints de análise, filtros por equipe e variável, comparação de outliers, interpretação e síntese estatística.

Na pasta principal do projeto, execute:

```bash
python -m unittest discover -s tests -v
```

A execução é considerada bem-sucedida quando os testes terminam com `OK`, sem falhas ou erros.

Os testes devem ser executados novamente após alterações no processamento ou nos endpoints.

## 10. Decisões metodológicas e limitações

### Estatística descritiva

Os quartis utilizam interpolação linear. O desvio padrão é amostral, e a assimetria utiliza o coeficiente ajustado de Fisher–Pearson.

A regra de Tukey identifica valores abaixo de Q1 − 1,5 × IQR ou acima de Q3 + 1,5 × IQR.

### Métodos de detecção

O teste de Grubbs é aplicado a um único extremo, sob hipótese de normalidade. A implementação de ECOD utiliza pontuações empíricas univariadas de cauda, não correspondendo à implementação multivariada de uma biblioteca especializada.

K-NN, DBSCAN e LOF são sensíveis às configurações adotadas e à distribuição dos dados. Seus resultados devem ser interpretados de maneira exploratória.

### Dados ausentes

Os mecanismos MCAR, MAR e MNAR são discutidos conceitualmente, mas não são classificados por testes formais na implementação.

A ausência de valores faltantes nas métricas analisadas torna esses procedimentos pouco informativos para o recorte utilizado.

### Interpretação dos resultados

A identificação de um outlier não significa necessariamente erro de registro. No contexto esportivo, valores extremos podem refletir jogos excepcionalmente bons ou ruins.

A concordância entre detectores não equivale à confirmação de anomalias reais.

As comparações entre equipes são descritivas, sem inferência causal ou testes de significância estatística.

## 11. Considerações finais

O projeto integra preparação de dados, análise exploratória, visualização interativa, detecção de outliers e interpretação estatística em uma única aplicação web.

A comparação entre Los Angeles Lakers e Denver Nuggets permite investigar padrões de desempenho, diferenças de variabilidade e observações atípicas, considerando os pressupostos e as limitações de cada método.

A aplicação foi concebida como ferramenta acadêmica de análise e interpretação de dados, sem objetivo de previsão de resultados esportivos.

---

**Disciplina:** Laboratório de Ciência de Dados  
**Projeto:** Projeto 1  
**Grupo:** 1  
**Equipes analisadas:** Los Angeles Lakers e Denver Nuggets  
**Linguagem principal:** Python  
**Interface:** Flask + Plotly
