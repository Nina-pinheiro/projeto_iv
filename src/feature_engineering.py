# feature_engineering.py

import numpy as np
import pandas as pd


def create_cluster_features(df):

    df = df.copy()

    # Evita divisão por zero
    total = df["total_doses"].replace(0, np.nan)

    # ---------------------------------
    # Perfil por faixa etária
    # ---------------------------------

    df["pct_criancas"] = (
        df["doses_criancas_0a5"] / total
    )

    df["pct_adultos"] = (
        df["doses_adultos_18a59"] / total
    )

    df["pct_idosos"] = (
        df["doses_idosos_60mais"] / total
    )

    # ---------------------------------
    # Perfil por sexo
    # ---------------------------------

    df["pct_feminino"] = (
        df["doses_sexo_feminino"] / total
    )

    df["pct_masculino"] = (
        df["doses_sexo_masculino"] / total
    )

    # ---------------------------------
    # Perfil por imunobiológico
    # ---------------------------------

    df["pct_influenza"] = (
        df["doses_influenza_gripe"] / total
    )

    df["pct_covid"] = (
        df["doses_covid"] / total
    )

    # ---------------------------------
    # Intensidade de vacinação
    # ---------------------------------

    df["doses_por_paciente"] = (
        df["total_doses"] /
        df["total_pacientes_unicos"].replace(0, np.nan)
    )

    # ---------------------------------
    # Transformação do volume
    # ---------------------------------

    # Mantemos informação de volume,
    # mas reduzimos influência dos outliers
    df["log_total_doses"] = np.log1p(
        df["total_doses"]
    )

    # Trata eventuais divisões inválidas
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    return df


CLUSTER_FEATURES = [
    "media_idade",
    "pct_criancas",
    "pct_adultos",
    "pct_idosos",
    "pct_feminino",
    "pct_influenza",
    "pct_covid",
    "doses_por_paciente",
    "log_total_doses",
]

def get_cluster_matrix(df):

    df_features = create_cluster_features(df)

    X = df_features[
        CLUSTER_FEATURES
    ].copy()

    # Caso alguma proporção gere NaN
    X = X.fillna(0)

    return df_features, X