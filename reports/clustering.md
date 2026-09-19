# Análise de Clustering

## 1. Objetivo

A etapa de clustering teve como objetivo identificar padrões distintos nas aplicações de vacinas registradas por CEP.

Os agrupamentos devem ser interpretados como **perfis de vacinação observados nos CEPs**, e não como descrição direta da composição demográfica da população residente.

## 2. Engenharia de atributos

A análise exploratória mostrou que as variáveis brutas de contagem apresentavam correlações muito elevadas entre si.

Para reduzir a influência do volume total de vacinação, foram criadas variáveis relativas:

- `media_idade`
- `pct_criancas`
- `pct_adultos`
- `pct_idosos`
- `pct_feminino`
- `pct_influenza`
- `pct_covid`
- `doses_por_paciente`
- `log_total_doses`

A variável `pct_masculino` foi removida da matriz final por apresentar correlação praticamente perfeita e inversa com `pct_feminino`.

## 3. Padronização

As features foram padronizadas com `StandardScaler`.

Como K-Means e DBSCAN utilizam medidas de distância, a padronização evita que variáveis de maior escala dominem artificialmente os agrupamentos.

## 4. Definição do número de clusters

Foram avaliados valores de K entre 2 e 10.

As principais métricas utilizadas foram:

- inércia;
- Silhouette Score.

Após a remoção da variável redundante, foram observados aproximadamente:

| K | Silhouette |
|---:|---:|
| 2 | 0,278 |
| 3 | 0,262 |
| 4 | 0,254 |
| 5 | 0,260 |
| 6 | 0,194 |
| 7 | 0,187 |
| 8 | 0,188 |
| 9 | 0,181 |
| 10 | 0,190 |

Embora K=2 tenha apresentado o maior Silhouette Score, as soluções K=2, K=3 e K=5 foram comparadas em maior detalhe.

A solução K=3 foi selecionada por apresentar melhor equilíbrio entre qualidade estatística e capacidade de interpretação.

## 5. Resultado final do K-Means

A solução final com K=3 resultou em:

| Cluster | Quantidade de CEPs |
|---:|---:|
| 0 | 596 |
| 1 | 168 |
| 2 | 338 |

## 6. Caracterização dos clusters

### Cluster 0 — maior participação de aplicações em adultos e influenza

O Cluster 0 apresentou:

- idade média dos registros próxima de 36,8 anos;
- aproximadamente 72% das doses associadas a adultos entre 18 e 59 anos;
- participação infantil próxima de 9%;
- participação de idosos próxima de 13%;
- aproximadamente 72,3% de participação relativa de influenza;
- aproximadamente 3,7% de participação relativa de Covid;
- cerca de 1,23 dose por paciente.

Esse grupo representa CEPs com maior participação relativa de aplicações em adultos e forte presença da vacinação contra influenza.

### Cluster 1 — maior participação de aplicações em crianças

O Cluster 1 apresentou:

- idade média próxima de 21,9 anos;
- aproximadamente 44,2% das doses associadas a crianças de 0 a 5 anos;
- aproximadamente 38% associadas a adultos;
- menos de 10% associadas a idosos;
- aproximadamente 1,88 dose por paciente.

Esse grupo representa CEPs cujo histórico de vacinação apresenta maior participação relativa de aplicações em crianças.

Essa interpretação não significa que esses CEPs possuam necessariamente maior população infantil.

### Cluster 2 — maior participação de aplicações em idosos e maior volume

O Cluster 2 apresentou:

- idade média próxima de 43,9 anos;
- aproximadamente 35,2% das doses associadas a pessoas com 60 anos ou mais;
- aproximadamente 45,3% associadas a adultos;
- aproximadamente 11,5% associadas a crianças;
- maior participação relativa de vacinação contra Covid;
- maior valor médio de `log_total_doses`.

Esse grupo representa CEPs com maior participação relativa de aplicações em idosos e maior volume registrado de vacinação.

## 7. PCA

O PCA foi utilizado para visualizar os clusters em duas dimensões.

Resultados:

```text
PC1 ≈ 33,4%
PC2 ≈ 26,5%
Variância acumulada ≈ 59,8%
```

A visualização em duas dimensões preserva uma parcela relevante da estrutura dos dados, mas não toda a informação utilizada no treinamento.

## 8. Silhouette por cluster

Os Silhouette Scores médios foram aproximadamente:

| Cluster | Silhouette médio |
|---:|---:|
| 0 | 0,344 |
| 1 | 0,139 |
| 2 | 0,177 |

O Cluster 0 apresentou maior coesão e separação.

Os Clusters 1 e 2 apresentaram maior sobreposição e presença de observações próximas às fronteiras entre os grupos.

## 9. Observações com Silhouette negativo

Alguns CEPs apresentaram Silhouette negativo.

Isso indica que essas observações podem estar mais próximas, em média, de outro cluster do que do grupo ao qual foram atribuídas.

Esses casos foram tratados como perfis intermediários ou observações que merecem investigação, e não como erros automáticos.

## 10. Distância ao centróide

Também foi calculada a distância de cada CEP ao centróide de seu cluster.

Alguns CEPs apresentaram distâncias muito superiores às demais, como:

- `24740`;
- `13173`;
- `05640`;
- `95906`;
- `21021`.

Esses registros foram considerados casos atípicos para investigação adicional.

## 11. DBSCAN

O DBSCAN foi aplicado sobre o mesmo espaço padronizado de características.

O objetivo foi complementar o K-Means, principalmente na identificação de regiões densas e observações atípicas.

## 12. Seleção de parâmetros do DBSCAN

Foram avaliadas diferentes combinações de:

- `eps`;
- `min_samples`;
- número de clusters;
- quantidade de ruídos;
- percentual de ruído;
- Silhouette Score.

Configurações com Silhouette muito alto, mas que classificavam grande parte da base como ruído, foram descartadas.

Após refinamento, a configuração selecionada foi:

```text
eps = 1.50
min_samples = 4
```

Essa solução apresentou aproximadamente:

```text
2 clusters
120 CEPs como ruído
10,89% de ruído
Silhouette ≈ 0,280
```

## 13. Estrutura encontrada pelo DBSCAN

Apesar de indicar dois clusters, a distribuição foi altamente desequilibrada:

```text
-1: 120 CEPs
 0:   4 CEPs
 1: 978 CEPs
```

Portanto, o DBSCAN não identificou dois grandes segmentos comparáveis.

Na prática, encontrou:

- uma grande região densa;
- um pequeno grupo isolado;
- um conjunto de observações classificadas como ruído.

## 14. Comparação K-Means × DBSCAN

A comparação entre os modelos mostrou:

| K-Means | DBSCAN -1 | DBSCAN 0 | DBSCAN 1 | Total |
|---:|---:|---:|---:|---:|
| 0 | 23 | 0 | 573 | 596 |
| 1 | 61 | 4 | 103 | 168 |
| 2 | 36 | 0 | 302 | 338 |

A maior parte dos CEPs dos Clusters 0 e 2 do K-Means foi incorporada à grande região densa do DBSCAN.

O Cluster 1 apresentou maior proporção relativa de observações classificadas como ruído.

## 15. Interpretação final dos modelos

Os dois algoritmos foram utilizados de maneira complementar.

### K-Means

Utilizado como método principal de segmentação.

Vantagens observadas:

- gera grupos de tamanho representativo;
- permite caracterização dos perfis;
- facilita interpretação dos padrões predominantes.

### DBSCAN

Utilizado principalmente como técnica de detecção de observações atípicas.

Vantagens observadas:

- não exige número prévio de clusters;
- identifica regiões densas;
- permite classificar pontos como ruído.

## 16. Conclusão

O K-Means com K=3 foi mantido como principal modelo de segmentação dos perfis de vacinação.

O DBSCAN, com `eps=1.50` e `min_samples=4`, foi utilizado como ferramenta complementar para identificação de CEPs com comportamento pouco frequente ou atípico.

A concordância entre:

- baixo Silhouette no K-Means;
- grande distância ao centróide;
- classificação como ruído no DBSCAN;

foi utilizada como evidência adicional para priorizar observações que merecem investigação.

Os agrupamentos obtidos não devem ser interpretados como categorias demográficas dos territórios, mas como padrões predominantes das aplicações registradas nos CEPs.
