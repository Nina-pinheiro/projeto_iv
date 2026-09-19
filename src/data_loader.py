from google.cloud import bigquery

from config import PROJECT_ID, TABLES


def get_client():
    return bigquery.Client(project=PROJECT_ID)


def load_table(client, table_name):

    query = f"""
    SELECT *
    FROM `{table_name}`
    """

    return client.query(query).to_dataframe()


def load_all():

    client = get_client()

    df_kpis = load_table(
        client,
        TABLES["kpis"]
    )

    df_series = load_table(
        client,
        TABLES["series"]
    )

    df_cluster = load_table(
        client,
        TABLES["cluster"]
    )

    return df_kpis, df_series, df_cluster