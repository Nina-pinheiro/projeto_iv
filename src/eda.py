import matplotlib.pyplot as plt


def doses_by_vaccine(
    df,
    top_n=15
):

    result = (
        df
        .groupby("sigla_vacina")[
            "total_doses"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    result.head(top_n).sort_values().plot(
        kind="barh",
        figsize=(10, 6)
    )

    plt.title(
        f"{top_n} vacinas com maior número de doses"
    )

    plt.xlabel("Doses")
    plt.ylabel("Vacina")

    plt.show()

    return result


def doses_by_age(df):

    result = (
        df
        .groupby("faixa_etaria")[
            "total_doses"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    result.plot(
        kind="bar",
        figsize=(10, 5)
    )

    plt.title(
        "Doses por faixa etária"
    )

    plt.ylabel("Doses")

    plt.xticks(
        rotation=45
    )

    plt.show()

    return result


def daily_series(df):

    result = (
        df
        .groupby("data_aplicacao")[
            "total_doses_aplicadas"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "data_aplicacao"
        )
    )

    result["media_movel_7d"] = (
        result[
            "total_doses_aplicadas"
        ]
        .rolling(7)
        .mean()
    )

    plt.figure(
        figsize=(14, 5)
    )

    plt.plot(
        result["data_aplicacao"],
        result["total_doses_aplicadas"],
        alpha=0.4,
        label="Diário"
    )

    plt.plot(
        result["data_aplicacao"],
        result["media_movel_7d"],
        label="Média móvel 7 dias"
    )

    plt.title(
        "Evolução das doses aplicadas"
    )

    plt.legend()

    plt.show()

    return result


def vaccine_ranking(df):

    return (
        df
        .groupby("sigla_vacina")[
            "total_doses_aplicadas"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )


def cluster_summary(df):

    numeric = (
        df
        .select_dtypes(
            include="number"
        )
    )

    return numeric.describe().T

import pandas as pd
import matplotlib.pyplot as plt


def resumo_cluster(df):
    cols = df.select_dtypes(include="number").columns

    print("\nResumo estatístico:")
    print(df[cols].describe().T)

    print("\nPercentual de zeros:")
    zeros = (
        (df[cols] == 0)
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    print(zeros.round(2))

    return zeros


def distribuicao_cluster(df):
    cols = df.select_dtypes(include="number").columns

    for col in cols:
        plt.figure(figsize=(8, 4))

        plt.hist(
            df[col],
            bins=30
        )

        plt.title(f"Distribuição - {col}")
        plt.xlabel(col)
        plt.ylabel("Frequência")

        plt.show()


def correlacao_cluster(df):
    cols = df.select_dtypes(include="number").columns

    corr = df[cols].corr()

    print(corr.round(2))

    return corr


def top_ceps(df, n=20):
    resultado = (
        df[
            [
                "cep_prefixo_5digitos",
                "total_doses"
            ]
        ]
        .sort_values(
            "total_doses",
            ascending=False
        )
        .head(n)
    )

    print(resultado)

    return resultado


def ranking_vacinas(df, n=20):
    resultado = (
        df
        .groupby("sigla_vacina")[
            "total_doses_aplicadas"
        ]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    resultado.sort_values().plot(
        kind="barh",
        figsize=(10, 7)
    )

    plt.title("Vacinas com maior volume")
    plt.xlabel("Doses aplicadas")
    plt.ylabel("Vacina")

    plt.show()

    return resultado


def serie_temporal_geral(df):
    serie = (
        df
        .groupby("data_aplicacao")[
            "total_doses_aplicadas"
        ]
        .sum()
        .reset_index()
        .sort_values("data_aplicacao")
    )

    serie["media_movel_7d"] = (
        serie["total_doses_aplicadas"]
        .rolling(7)
        .mean()
    )

    plt.figure(figsize=(14, 5))

    plt.plot(
        serie["data_aplicacao"],
        serie["total_doses_aplicadas"],
        alpha=0.4,
        label="Doses diárias"
    )

    plt.plot(
        serie["data_aplicacao"],
        serie["media_movel_7d"],
        label="Média móvel 7 dias"
    )

    plt.title("Doses aplicadas ao longo do tempo")
    plt.xlabel("Data")
    plt.ylabel("Doses")
    plt.legend()

    plt.show()

    return serie


def doses_por_dia_semana(df):
    resultado = (
        df
        .groupby("dia_semana")[
            "total_doses_aplicadas"
        ]
        .sum()
        .sort_index()
    )

    resultado.plot(
        kind="bar",
        figsize=(8, 4)
    )

    plt.title("Doses por dia da semana")
    plt.xlabel("Dia da semana")
    plt.ylabel("Doses")

    plt.show()

    return resultado