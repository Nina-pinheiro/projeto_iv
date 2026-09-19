import pandas as pd
import numpy as np


def basic_validation(df, name):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Shape:", df.shape)

    print("\nDuplicados exatos:")
    print(df.duplicated().sum())

    print("\nNulos:")

    nulls = pd.DataFrame({
        "nulos": df.isna().sum(),
        "percentual": (
            df.isna().mean() * 100
        ).round(2)
    })

    print(
        nulls
        .sort_values(
            "percentual",
            ascending=False
        )
    )


def validate_key(df, key):

    duplicates = df[
        df.duplicated(
            subset=key,
            keep=False
        )
    ]

    return duplicates


def validate_negative_values(df):

    numeric_columns = (
        df
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    results = {}

    for column in numeric_columns:

        results[column] = (
            df[column] < 0
        ).sum()

    return pd.Series(
        results,
        name="valores_negativos"
    )


def validate_constant_columns(df):

    return (
        df
        .nunique()
        .sort_values()
    )


def validate_dates(
    df,
    date_column
):

    dates = df[date_column]

    print(
        "Data mínima:",
        dates.min()
    )

    print(
        "Data máxima:",
        dates.max()
    )

    print(
        "Datas inválidas:",
        dates.isna().sum()
    )


def missing_dates(
    df,
    date_column
):

    dates = pd.DatetimeIndex(
        df[date_column]
        .dropna()
        .unique()
    )

    expected = pd.date_range(
        start=dates.min(),
        end=dates.max(),
        freq="D"
    )

    return expected.difference(
        dates
    )