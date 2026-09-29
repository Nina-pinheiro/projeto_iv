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
- preparação das séries diárias por imunobiológico (TOTAL, COV-19, INF3, INF4, HB, dT);
- divisão temporal treino/teste (últimos 28 dias como teste);
- baselines (ingênuo, sazonal ingênuo 7d, média por dia da semana);
- SARIMA (busca de ordens, SARIMA(0,1,1)(0,1,1)₇ e variante em log) e Prophet;
- comparação por RMSE e previsão dos 14 dias seguintes (01/08 a 14/08/2026).

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

## Principais resultados de séries temporais

- A sazonalidade semanal domina todas as séries (quedas aos sábados e domingos).
- O sazonal ingênuo foi o melhor modelo em COV-19 e INF4; o Prophet, em HB e dT;
  o SARIMA em log foi usado no INF3.
- No TOTAL, o Prophet teve o menor RMSE, mas projetou uma queda implausível de 44%;
  por isso, a previsão futura usou o sazonal ingênuo.
- Os modelos SARIMA aditivos geraram valores negativos nos fins de semana,
  o que motivou a versão em log (efeito multiplicativo).
- Limitações: uma única janela de teste, sem feriados ou campanhas como variáveis externas,
  e previsão de doses aplicadas, não de cobertura.
