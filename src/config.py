PROJECT_ID = "pi4-vacinacao-poa"

TABLES = {
    "kpis": "pi4-vacinacao-poa.pni_gold.tb_visao_geral_kpis",
    "series": "pi4-vacinacao-poa.pni_gold.tb_series_temporais_doses",
    "cluster": "pi4-vacinacao-poa.pni_gold.tb_clustering_espacial_cep",
}

KEYS = {
    "kpis": [
        "mes_aplicacao",
        "nome_estabelecimento",
        "faixa_etaria",
        "sexo_paciente",
        "raca_cor_paciente",
        "sigla_vacina",
        "tipo_dose",
    ],

    "series": [
        "data_aplicacao",
        "sigla_vacina",
        "tipo_dose",
    ],

    "cluster": [
        "cep_prefixo_5digitos"
    ],
}