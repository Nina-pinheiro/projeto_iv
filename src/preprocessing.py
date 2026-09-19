import pandas as pd


def prepare_kpis(df):

    df = df.copy()

    return df


def prepare_series(df):

    df = df.copy()

    df["data_aplicacao"] = pd.to_datetime(
        df["data_aplicacao"],
        errors="coerce"
    )

    return df


def prepare_cluster(df):

    df = df.copy()

    df["cep_prefixo_5digitos"] = (
        df["cep_prefixo_5digitos"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )

    return df


def prepare_all(
    df_kpis,
    df_series,
    df_cluster
):

    df_kpis = prepare_kpis(df_kpis)

    df_series = prepare_series(df_series)

    df_cluster = prepare_cluster(df_cluster)

    return (
        df_kpis,
        df_series,
        df_cluster
    )