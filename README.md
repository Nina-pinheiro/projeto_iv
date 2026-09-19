# Análise de Vacinação — Porto Alegre

Projeto de Ciência de Dados voltado à análise de padrões de vacinação e comportamento temporal dos registros de imunização em Porto Alegre.

## Objetivos

O projeto possui dois principais eixos de análise:

1. **Identificar perfis de vacinação por CEP**, utilizando técnicas de clustering.
2. **Modelar a evolução temporal das aplicações**, com foco em previsão de demanda e apoio ao planejamento operacional.

## Arquitetura analítica

```text
BigQuery
   ↓
Camada Gold
   ↓
Validação e EDA
   ↓
Feature Engineering
   ↓
Clustering
   ├── K-Means
   └── DBSCAN
   ↓
Séries temporais
   ├── ARIMA
   └── Prophet
```

## Fontes de dados

As tabelas utilizadas até o momento estão armazenadas no BigQuery, no projeto:

```text
pi4-vacinacao-poa
```

Tabelas da camada `pni_gold`:

- `tb_visao_geral_kpis`
- `tb_series_temporais_doses`
- `tb_clustering_espacial_cep`

Os dados não são versionados diretamente neste repositório.

## Estrutura sugerida do repositório

```text
pi4-vacinacao-poa/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_validacao_eda.ipynb
│   ├── 02_clustering.ipynb
│   └── 03_series_temporais.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── validation.py
│   ├── eda.py
│   ├── feature_engineering.py
│   ├── clustering.py
│   └── time_series.py
│
├── reports/
│   ├── metodologia.md
│   ├── eda.md
│   ├── clustering.md
│   └── figures/
│
├── data/
│   └── README.md
│
└── tests/
```

## Etapas concluídas

Até o momento foram concluídas:

- ingestão das tabelas do BigQuery;
- validação estrutural das bases;
- análise exploratória;
- engenharia de atributos para clustering;
- definição do número de clusters;
- treinamento e interpretação do K-Means;
- análise com PCA;
- avaliação por Silhouette Score;
- análise de distância ao centróide;
- aplicação complementar de DBSCAN;
- comparação entre K-Means e DBSCAN.

## Principais resultados de clustering

O K-Means foi utilizado como método principal de segmentação, com **K = 3**, resultando em três perfis distintos de vacinação por CEP:

- maior participação de aplicações em adultos e influenza;
- maior participação de aplicações em crianças;
- maior participação de aplicações em idosos, maior presença de Covid e maior volume de registros.

O DBSCAN foi utilizado de forma complementar para identificar **observações atípicas**. A configuração escolhida foi:

```text
eps = 1.50
min_samples = 4
```

Nessa configuração, a maior parte dos CEPs ficou concentrada em uma única região densa, enquanto aproximadamente 10,9% foram classificados como ruído.

## Interpretação dos clusters

Os clusters representam **perfis das aplicações de vacinas registradas nos CEPs**.

Eles não devem ser interpretados como descrição direta da composição demográfica da população residente, pois a base utilizada não contém denominadores populacionais por microárea.

## Próxima etapa

A próxima etapa do projeto é a modelagem de séries temporais:

```text
Preparação da série
   ↓
Divisão temporal treino/teste
   ↓
Baseline
   ↓
ARIMA
   ↓
Prophet
   ↓
MAE / RMSE
   ↓
Comparação dos modelos
```
