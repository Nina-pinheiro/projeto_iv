# Metodologia

## 1. Visão geral

O projeto foi estruturado em uma pipeline modular de Ciência de Dados, separando ingestão, preparação, validação, análise exploratória, engenharia de atributos e modelagem.

A arquitetura adotada busca permitir reprodutibilidade, manutenção simples e reutilização do código.

## 2. Ingestão dos dados

Os dados são carregados diretamente do BigQuery a partir do projeto:

```text
pi4-vacinacao-poa
```

Foram utilizadas três tabelas principais:

- `pni_gold.tb_visao_geral_kpis`
- `pni_gold.tb_series_temporais_doses`
- `pni_gold.tb_clustering_espacial_cep`

A conexão com o BigQuery foi realizada via biblioteca `google-cloud-bigquery`, utilizando autenticação por Application Default Credentials no ambiente Google Colab.

## 3. Validação dos dados

Antes da modelagem, foram executadas verificações de qualidade e consistência.

As validações incluíram:

- quantidade de registros;
- presença de valores nulos;
- registros duplicados;
- duplicidade das chaves esperadas;
- presença de valores negativos;
- validade das datas;
- continuidade da série temporal;
- variabilidade das features.

### Resultados

As bases apresentaram:

- **205.852 registros** na base de KPIs;
- **22.419 registros** na base de séries temporais;
- **1.102 CEPs** na base destinada ao clustering;
- ausência de valores nulos;
- ausência de duplicados exatos;
- ausência de CEPs duplicados;
- ausência de valores negativos nas variáveis avaliadas;
- datas válidas entre 01/01/2026 e 31/07/2026;
- ausência de dias completamente ausentes no período.

Com isso, a etapa de qualidade básica dos dados foi considerada concluída.

## 4. Análise exploratória

A EDA foi utilizada para compreender:

- distribuição das doses;
- comportamento das variáveis numéricas;
- concentração de aplicações;
- relações entre features;
- comportamento temporal;
- efeito do dia da semana;
- possíveis observações extremas.

A análise identificou forte assimetria nas variáveis de volume e correlação muito alta entre contagens absolutas.

## 5. Engenharia de atributos

Como as variáveis brutas estavam fortemente associadas ao volume total de aplicações, foram criadas variáveis relativas.

Foram construídas as features:

- `pct_criancas`
- `pct_adultos`
- `pct_idosos`
- `pct_feminino`
- `pct_influenza`
- `pct_covid`
- `doses_por_paciente`
- `log_total_doses`
- `media_idade`

A variável `pct_masculino` foi removida do conjunto final utilizado no clustering devido à correlação praticamente perfeita e inversa com `pct_feminino`.

A transformação `log(1 + total_doses)` foi utilizada para preservar informação de volume reduzindo a influência de valores extremos.

## 6. Padronização

As features foram padronizadas com `StandardScaler`.

Essa etapa foi necessária porque K-Means e DBSCAN são algoritmos baseados em distância e são sensíveis a diferenças de escala entre as variáveis.

## 7. K-Means

Foram avaliados valores de K entre 2 e 10 utilizando:

- inércia;
- Silhouette Score;
- interpretabilidade dos grupos.

As soluções K=2, K=3 e K=5 foram comparadas em maior detalhe.

Apesar de K=2 apresentar maior Silhouette Score, a solução com **K=3** apresentou melhor equilíbrio entre qualidade quantitativa e interpretação dos perfis encontrados.

## 8. PCA

O PCA foi aplicado somente para visualização dos clusters em duas dimensões.

As duas primeiras componentes explicaram aproximadamente:

- PC1: 33,4%;
- PC2: 26,5%;
- variância acumulada: 59,8%.

O PCA não substituiu as features utilizadas no treinamento do K-Means.

## 9. Avaliação interna do K-Means

Além do Silhouette global, foram avaliados:

- Silhouette por observação;
- Silhouette médio por cluster;
- distância ao centróide;
- CEPs com menor aderência ao agrupamento.

Essas análises mostraram que alguns CEPs apresentam características intermediárias entre os perfis identificados.

## 10. DBSCAN

O DBSCAN foi utilizado de maneira complementar ao K-Means.

Foram avaliadas diferentes combinações de:

- `eps`;
- `min_samples`;
- número de clusters;
- percentual de ruído;
- Silhouette Score.

A configuração adotada foi:

```text
eps = 1.50
min_samples = 4
```

O resultado indicou uma grande região densa contendo a maior parte dos CEPs e um conjunto de observações classificadas como ruído.

Por esse motivo, o DBSCAN foi interpretado principalmente como ferramenta de **detecção de perfis atípicos**, e não como substituto do K-Means para segmentação.

## 11. Limitações

As análises realizadas até aqui possuem algumas limitações importantes:

- o clustering descreve o perfil das aplicações registradas, não a composição demográfica da população residente;
- a base atual de clustering não utiliza latitude e longitude;
- portanto, o agrupamento não deve ser descrito como clustering geográfico estrito;
- alguns prefixos de CEP precisam ser validados antes de análises espaciais;
- a série temporal disponível cobre apenas janeiro a julho de 2026.

## 12. Próximas etapas

A continuidade do projeto inclui:

- validação de CEPs atípicos;
- eventual enriquecimento geográfico com latitude e longitude;
- construção de visualizações territoriais;
- preparação das séries temporais;
- ARIMA;
- Prophet;
- comparação por MAE e RMSE;
- integração dos resultados em dashboard.
