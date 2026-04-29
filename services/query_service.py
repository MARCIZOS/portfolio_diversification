"""Build semantic search queries from portfolio metrics."""

from __future__ import annotations


def _format_cluster_concentration(cluster_concentration: dict[str, float]) -> str:
    if not cluster_concentration:
        return "No cluster concentration data provided."

    top_cluster = max(cluster_concentration.items(), key=lambda item: item[1])
    cluster_label, cluster_weight = top_cluster
    return f"Top cluster {cluster_label} weight {cluster_weight:.2%}."


def build_query(metrics: dict) -> str:
    """Convert portfolio metrics into a semantic search query."""
    max_drawdown = metrics.get("max_drawdown")
    diversification_score = metrics.get("diversification_score")
    cluster_concentration = metrics.get("cluster_concentration", {})
    stress = metrics.get("stress", {})
    stressed_cvar = stress.get("stressed_cvar")

    drawdown_text = (
        f"Max drawdown {max_drawdown:.2%}." if max_drawdown is not None else "Max drawdown unknown."
    )
    diversification_text = (
        f"Diversification score {diversification_score:.2f}."
        if diversification_score is not None
        else "Diversification score unknown."
    )
    cluster_text = _format_cluster_concentration(cluster_concentration)
    stressed_cvar_text = (
        f"Stress CVaR {stressed_cvar:.4f}." if stressed_cvar is not None else "Stress CVaR unknown."
    )

    return (
        "Portfolio risk interpretation for a retail investor. "
        f"{drawdown_text} {diversification_text} {cluster_text} {stressed_cvar_text} "
        "Explain diversification, concentration risk, tail risk, and stress exposure. "
        "Provide actionable mitigation ideas."
    )
