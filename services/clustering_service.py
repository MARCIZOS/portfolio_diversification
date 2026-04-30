"""Service functions for correlation-based asset clustering."""

from collections import defaultdict

import numpy as np
from pandas import DataFrame
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform


def perform_clustering(corr_matrix: DataFrame) -> dict[int, list[str]]:
    """Group assets into hierarchical clusters from correlation.

    The function converts correlation into distance with:
        distance = 1 - correlation
    and applies Ward hierarchical linkage.

    Args:
        corr_matrix: Correlation matrix indexed/columned by asset tickers.

    Returns:
        Mapping of cluster label -> list of tickers in that cluster.
    """
    if corr_matrix.empty:
        return {}

    tickers = list(corr_matrix.columns)
    if len(tickers) == 1:
        return {1: [tickers[0]]}

    distance_matrix = 1.0 - corr_matrix.clip(-1.0, 1.0)
    distance_values = np.array(distance_matrix.values, dtype=float, copy=True)
    np.fill_diagonal(distance_values, 0.0)
    distance_values = np.clip(distance_values, a_min=0.0, a_max=None)

    condensed_distance = squareform(distance_values, checks=False)
    linkage_matrix = linkage(condensed_distance, method="ward")

    # Dynamic threshold from merge-distance scale avoids hardcoded cluster count.
    threshold = float(np.median(linkage_matrix[:, 2]))
    if threshold <= 0:
        threshold = float(np.mean(linkage_matrix[:, 2]))
    if threshold <= 0:
        threshold = 0.5

    labels = fcluster(linkage_matrix, t=threshold, criterion="distance")

    grouped: dict[int, list[str]] = defaultdict(list)
    for ticker, cluster_id in zip(tickers, labels):
        grouped[int(cluster_id)].append(ticker)

    return {cluster_id: members for cluster_id, members in sorted(grouped.items())}
