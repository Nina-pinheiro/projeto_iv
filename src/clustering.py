# clustering.py

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import (
    silhouette_score,
    silhouette_samples
)
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


# ============================================================
# 1. PADRONIZAÇÃO DAS FEATURES
# ============================================================

def scale_features(X):
    """
    Padroniza as features utilizando StandardScaler.

    Parâmetros
    ----------
    X : DataFrame ou array
        Matriz de features.

    Retorna
    -------
    X_scaled : array
        Matriz padronizada.

    scaler : StandardScaler
        Objeto treinado para transformação.
    """

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


# ============================================================
# 2. AVALIAÇÃO DO NÚMERO DE CLUSTERS - K-MEANS
# ============================================================

def evaluate_kmeans(
    X_scaled,
    k_min=2,
    k_max=10
):
    """
    Avalia diferentes valores de K utilizando:

    - Inércia
    - Silhouette Score
    """

    resultados = []

    for k in range(k_min, k_max + 1):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20
        )

        labels = model.fit_predict(
            X_scaled
        )

        silhouette = silhouette_score(
            X_scaled,
            labels
        )

        resultados.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette": silhouette
        })

    return pd.DataFrame(resultados)


# ============================================================
# 3. TREINAMENTO DO K-MEANS
# ============================================================

def train_kmeans(
    X_scaled,
    k
):
    """
    Treina o K-Means para o número de clusters escolhido.
    """

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(
        X_scaled
    )

    return model, labels


# ============================================================
# 4. COMPARAÇÃO DE SOLUÇÕES K-MEANS
# ============================================================

def compare_cluster_solutions(
    df_features,
    X_scaled,
    features,
    ks=(2, 3, 5)
):
    """
    Compara diferentes soluções de K-Means.

    Para cada valor de K retorna:

    - modelo
    - labels
    - perfil médio dos clusters
    - tamanho dos clusters
    """

    resultados = {}

    for k in ks:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20
        )

        labels = model.fit_predict(
            X_scaled
        )

        df_temp = df_features.copy()

        df_temp["cluster"] = labels

        perfil = (
            df_temp
            .groupby("cluster")[features]
            .mean()
            .round(3)
        )

        tamanhos = (
            df_temp["cluster"]
            .value_counts()
            .sort_index()
        )

        resultados[k] = {
            "modelo": model,
            "labels": labels,
            "perfil": perfil,
            "tamanhos": tamanhos
        }

    return resultados


# ============================================================
# 5. PERFIL DOS CLUSTERS
# ============================================================

def cluster_profile(
    df,
    features,
    cluster_col="cluster"
):
    """
    Retorna:

    - quantidade de CEPs por cluster
    - média das features
    - mediana das features
    """

    tamanho = (
        df[cluster_col]
        .value_counts()
        .sort_index()
        .rename("quantidade_ceps")
    )

    media = (
        df
        .groupby(cluster_col)[features]
        .mean()
        .round(3)
    )

    mediana = (
        df
        .groupby(cluster_col)[features]
        .median()
        .round(3)
    )

    return tamanho, media, mediana


# ============================================================
# 6. PCA PARA VISUALIZAÇÃO
# ============================================================

def pca_projection(
    X_scaled,
    labels
):
    """
    Reduz os dados para duas dimensões com PCA.

    O PCA é usado apenas para visualização.
    O K-Means continua sendo treinado com todas as features.
    """

    pca = PCA(
        n_components=2
    )

    X_pca = pca.fit_transform(
        X_scaled
    )

    df_pca = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "cluster": labels
    })

    return df_pca, pca


# ============================================================
# 7. SILHOUETTE INDIVIDUAL
# ============================================================

def silhouette_by_sample(
    X_scaled,
    labels,
    df_features
):
    """
    Calcula o Silhouette Score para cada CEP.

    Interpretação geral:

    > 0  : observação relativamente bem alocada
    ~ 0  : observação na fronteira entre clusters
    < 0  : observação potencialmente mais próxima de outro grupo
    """

    values = silhouette_samples(
        X_scaled,
        labels
    )

    result = df_features[
        ["cep_prefixo_5digitos"]
    ].copy()

    result["cluster"] = labels
    result["silhouette"] = values

    return result


# ============================================================
# 8. DISTÂNCIA AO CENTRÓIDE
# ============================================================

def distance_to_centroid(
    X_scaled,
    labels,
    model,
    df_features
):
    """
    Calcula a distância de cada observação ao centróide
    do cluster atribuído pelo K-Means.

    Valores maiores indicam CEPs mais distantes
    do comportamento típico do cluster.
    """

    distances = np.zeros(
        len(X_scaled)
    )

    for i in range(len(X_scaled)):

        cluster = labels[i]

        distances[i] = np.linalg.norm(
            X_scaled[i]
            - model.cluster_centers_[cluster]
        )

    result = df_features[
        ["cep_prefixo_5digitos"]
    ].copy()

    result["cluster"] = labels
    result["distancia_centroide"] = distances

    return result


# ============================================================
# 9. CEPs POR CLUSTER
# ============================================================

def ceps_by_cluster(
    df_features,
    cluster_col="cluster",
    cep_col="cep_prefixo_5digitos"
):
    """
    Retorna um dicionário com os CEPs
    pertencentes a cada cluster.
    """

    resultado = {}

    for cluster in sorted(
        df_features[cluster_col].unique()
    ):

        resultado[cluster] = (
            df_features[
                df_features[cluster_col] == cluster
            ][cep_col]
            .tolist()
        )

    return resultado


# ============================================================
# 10. PRINCIPAIS CEPs POR VOLUME
# ============================================================

def top_ceps_by_cluster(
    df_features,
    n=10,
    cluster_col="cluster"
):
    """
    Retorna os CEPs com maior volume de doses
    dentro de cada cluster.
    """

    resultado = (
        df_features
        .sort_values(
            [cluster_col, "total_doses"],
            ascending=[True, False]
        )
        .groupby(cluster_col)
        .head(n)
    )

    return resultado[
        [
            "cep_prefixo_5digitos",
            cluster_col,
            "total_doses",
            "total_pacientes_unicos"
        ]
    ]


# ============================================================
# 11. K-DISTANCE PARA ESCOLHA DO EPS - DBSCAN
# ============================================================

def dbscan_k_distance(
    X_scaled,
    min_samples=10
):
    """
    Calcula a distância de cada observação
    até seu k-ésimo vizinho mais próximo.

    É utilizada como apoio para definição do eps
    do DBSCAN.
    """

    neighbors = NearestNeighbors(
        n_neighbors=min_samples
    )

    neighbors.fit(
        X_scaled
    )

    distances, _ = neighbors.kneighbors(
        X_scaled
    )

    k_distances = np.sort(
        distances[:, -1]
    )

    return k_distances


# ============================================================
# 12. TREINAMENTO DO DBSCAN
# ============================================================

def train_dbscan(
    X_scaled,
    eps,
    min_samples
):
    """
    Treina o DBSCAN.

    O label -1 representa observações classificadas
    como ruído.
    """

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples
    )

    labels = model.fit_predict(
        X_scaled
    )

    return model, labels


# ============================================================
# 13. AVALIAÇÃO DE PARÂMETROS DO DBSCAN
# ============================================================

def evaluate_dbscan(
    X_scaled,
    eps_values,
    min_samples_values
):
    """
    Avalia diversas combinações de:

    - eps
    - min_samples

    Retorna:

    - número de clusters
    - quantidade de ruídos
    - percentual de ruído
    - Silhouette Score dos pontos não classificados como ruído
    """

    resultados = []

    for min_samples in min_samples_values:

        for eps in eps_values:

            model = DBSCAN(
                eps=eps,
                min_samples=min_samples
            )

            labels = model.fit_predict(
                X_scaled
            )

            n_noise = np.sum(
                labels == -1
            )

            n_clusters = len(
                set(labels) - {-1}
            )

            pct_noise = (
                n_noise /
                len(labels)
            ) * 100

            silhouette = np.nan

            mask = labels != -1

            labels_validos = labels[
                mask
            ]

            if (
                n_clusters >= 2
                and len(set(labels_validos)) >= 2
            ):

                silhouette = silhouette_score(
                    X_scaled[mask],
                    labels_validos
                )

            resultados.append({
                "eps": eps,
                "min_samples": min_samples,
                "n_clusters": n_clusters,
                "n_noise": n_noise,
                "pct_noise": round(
                    pct_noise,
                    2
                ),
                "silhouette": silhouette
            })

    return pd.DataFrame(
        resultados
    )


# ============================================================
# 14. RESUMO DO DBSCAN
# ============================================================

def dbscan_summary(
    df_features,
    labels,
    features
):
    """
    Adiciona os clusters do DBSCAN ao DataFrame
    e gera:

    - tamanho dos grupos
    - perfil médio

    Cluster -1 representa ruído.
    """

    df_result = df_features.copy()

    df_result["cluster_dbscan"] = labels

    tamanho = (
        df_result[
            "cluster_dbscan"
        ]
        .value_counts()
        .sort_index()
    )

    perfil = (
        df_result
        .groupby(
            "cluster_dbscan"
        )[features]
        .mean()
        .round(3)
    )

    return (
        df_result,
        tamanho,
        perfil
    )


# ============================================================
# 15. RUÍDOS IDENTIFICADOS PELO DBSCAN
# ============================================================

def dbscan_noise(
    df_result
):
    """
    Retorna somente as observações classificadas
    como ruído pelo DBSCAN.
    """

    return (
        df_result[
            df_result["cluster_dbscan"] == -1
        ]
        .copy()
    )


# ============================================================
# 16. COMPARAÇÃO K-MEANS X DBSCAN
# ============================================================

def compare_kmeans_dbscan(
    df_features,
    kmeans_labels,
    dbscan_labels
):
    """
    Compara a classificação de cada CEP
    entre K-Means e DBSCAN.
    """

    resultado = df_features[
        ["cep_prefixo_5digitos"]
    ].copy()

    resultado["cluster_kmeans"] = (
        kmeans_labels
    )

    resultado["cluster_dbscan"] = (
        dbscan_labels
    )

    return resultado