# Análise Exploratória dos Dados

## 1. Objetivo

A análise exploratória teve como objetivo compreender a qualidade, distribuição e comportamento das bases antes da aplicação dos modelos de clustering e séries temporais.

## 2. Qualidade das bases

As três bases analisadas apresentaram boa consistência estrutural.

### KPIs

```text
205.852 registros
8 colunas
0 valores nulos
0 duplicados
```

### Séries temporais

```text
22.419 registros
8 colunas
0 valores nulos
0 duplicados
```

Período observado:

```text
01/01/2026 a 31/07/2026
```

Não foram encontradas datas inválidas ou dias completamente ausentes.

### Base de clustering

```text
1.102 CEPs
11 colunas
0 valores nulos
0 duplicados
0 CEPs duplicados
```

Também não foram encontrados valores negativos nas variáveis numéricas analisadas.

## 3. Distribuição das variáveis de clustering

As variáveis de contagem apresentaram forte assimetria à direita.

A maior parte dos CEPs possui volumes relativamente baixos de vacinação, enquanto poucos registros concentram volumes muito elevados.

Em `total_doses`, por exemplo:

- média aproximada: 915 doses;
- mediana: 43,5 doses;
- máximo: 181.688 doses.

Comportamento semelhante foi observado em:

- `total_pacientes_unicos`;
- doses em idosos;
- doses em crianças;
- doses em adultos;
- doses por sexo;
- influenza;
- Covid.

A variável `media_idade` apresentou comportamento mais equilibrado, com média aproximada de 36,7 anos.

## 4. Valores iguais a zero

As maiores proporções de zeros foram observadas em:

- `doses_criancas_0a5`: aproximadamente 23,4%;
- `doses_covid`: aproximadamente 21,6%;
- `doses_idosos_60mais`: aproximadamente 7,8%.

Esses valores não foram tratados automaticamente como dados ausentes, pois podem representar legitimamente ausência de aplicações em determinada categoria.

## 5. Correlação entre variáveis brutas

A matriz de correlação mostrou que praticamente todas as variáveis de contagem apresentavam correlação muito alta entre si, frequentemente entre 0,93 e 1,00.

Isso indicou que as variáveis estavam capturando principalmente o efeito do volume total de vacinação por CEP.

A variável `media_idade` foi a principal exceção, apresentando correlações próximas de zero com várias medidas de volume.

Esse resultado motivou a etapa de engenharia de atributos.

## 6. Engenharia de atributos

Foram transformadas contagens absolutas em indicadores relativos.

As novas variáveis permitiram reduzir a redundância observada anteriormente e representar melhor diferenças de perfil.

Exemplos:

- percentual de aplicações em crianças;
- percentual em adultos;
- percentual em idosos;
- percentual feminino;
- participação de influenza;
- participação de Covid;
- doses por paciente;
- volume total transformado em log.

Após a transformação, as correlações passaram a refletir relações mais interpretáveis.

Exemplos observados:

- `media_idade` × `pct_criancas`: aproximadamente -0,77;
- `media_idade` × `pct_idosos`: aproximadamente 0,75;
- `pct_criancas` × `pct_adultos`: aproximadamente -0,62;
- `pct_idosos` × `pct_covid`: aproximadamente 0,50.

A variável `pct_masculino` foi removida do conjunto final por apresentar correlação de aproximadamente -1,00 com `pct_feminino`.

## 7. Vacinas com maior volume

A análise do volume por imunobiológico mostrou forte concentração em poucas vacinas.

Entre as vacinas com maior volume apareceram:

- INF3;
- INF4;
- COV-19 PFIZER-COMIRN;
- HB;
- dT.

Essa diferença de volume reforça que os modelos de séries temporais devem ser construídos separadamente por vacina.

## 8. Comportamento temporal

A série diária apresentou mudança significativa de nível ao longo do período.

Entre janeiro e março, o volume permaneceu relativamente mais estável.

No final de março e início de abril houve forte crescimento, com pico diário superior a 40 mil doses.

A média móvel de sete dias confirmou que esse aumento não ocorreu apenas em um dia isolado.

Posteriormente foi observada redução gradual, com novo aumento pontual no início de junho.

## 9. Dia da semana

A análise por dia da semana mostrou forte padrão semanal.

O maior volume ocorreu em dias úteis, com redução importante aos finais de semana.

A segunda-feira apresentou o maior volume acumulado, enquanto o domingo apresentou o menor.

Esse comportamento deverá ser considerado na modelagem temporal, pois evidencia sazonalidade semanal.

## 10. Conclusão da EDA

A EDA mostrou que as bases possuem boa qualidade estrutural, mas apresentam:

- forte assimetria nas variáveis de volume;
- presença de observações extremas;
- alta redundância entre contagens absolutas;
- sazonalidade semanal na série temporal;
- mudança de nível ao longo do período.

Esses resultados justificaram:

- criação de variáveis relativas;
- transformação logarítmica do volume;
- padronização das features;
- uso de clustering para identificar perfis;
- uso futuro de modelos temporais capazes de considerar tendência e sazonalidade.
