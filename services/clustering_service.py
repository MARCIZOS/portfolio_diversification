"""Service functions for correlation-based asset clustering."""

from collections import defaultdict
import numpy as np
from pandas import DataFrame

def perform_clustering(corr_matrix: DataFrame) -> dict[int, list[str]]:
    """Group assets into clusters using a simple correlation threshold.
    
    This implementation avoids heavy dependencies like scipy to stay 
    under Vercel's deployment size limits. It uses a greedy grouping 
    approach based on a correlation threshold.

    Args:
        corr_matrix: Correlation matrix indexed/columned by asset tickers.

    Returns:
        Mapping of cluster label -> list of tickers in that cluster.
    """
    if corr_matrix.empty:
        return {}

    tickers = list(corr_matrix.columns)
    if len(tickers) <= 1:
        return {1: tickers} if tickers else {}

    # Threshold for grouping (higher = more clusters, lower = fewer)
    threshold = 0.6
    
    clusters = {}
    cluster_id = 1
    assigned = set()

    for i, ticker in enumerate(tickers):
        if ticker in assigned:
            continue
            
        # Start a new cluster
        current_cluster = [ticker]
        assigned.add(ticker)
        
        # Find all other unassigned tickers with high correlation to this one
        for j in range(i + 1, len(tickers)):
            other_ticker = tickers[j]
            if other_ticker not in assigned:
                correlation = corr_matrix.iloc[i, j]
                if correlation >= threshold:
                    current_cluster.append(other_ticker)
                    assigned.add(other_ticker)
        
        clusters[cluster_id] = current_cluster
        cluster_id += 1
        
    return clusters
