"""Diversification analysis services for portfolio concentration detection."""

import numpy as np


def calculate_enb(weights: list[float]) -> float:
    """Calculate Effective Number of Bets (ENB)."""
    weight_array = np.asarray(weights, dtype=float)
    denominator = float(np.sum(np.square(weight_array)))
    if denominator <= 0:
        raise ValueError("Weights must produce a positive ENB denominator.")
    return 1.0 / denominator


def calculate_cluster_concentration(
    clusters: dict[int, list[str]], weights_map: dict[str, float]
) -> dict[str, float]:
    """Aggregate total portfolio weight assigned to each correlation cluster."""
    concentration: dict[str, float] = {}
    for cluster_id, tickers in clusters.items():
        cluster_weight = sum(weights_map.get(ticker, 0.0) for ticker in tickers)
        concentration[f"cluster_{cluster_id}"] = round(float(cluster_weight), 6)
    return concentration


def calculate_diversification_score(enb: float, total_assets: int) -> float:
    """Calculate diversification score as ENB normalized by asset count."""
    if total_assets <= 0:
        raise ValueError("Total assets must be greater than zero.")
    return enb / float(total_assets)
