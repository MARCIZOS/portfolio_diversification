"""API routes for portfolio operations."""

import logging

from fastapi import APIRouter, HTTPException, status

from models.portfolio import PortfolioRequest
from services.ai_service import generate_portfolio_explanation
from services.clustering_service import perform_clustering
from services.correlation_service import (
    compute_correlation_matrix,
    get_high_correlation_pairs,
)
from services.data_service import calculate_returns, get_historical_prices
from services.diversification_service import (
    calculate_cluster_concentration,
    calculate_diversification_score,
    calculate_enb,
)
from services.portfolio_service import validate_portfolio
from services.risk_service import (
    calculate_cvar,
    calculate_drawdown,
    calculate_portfolio_returns,
    calculate_var,
    calculate_volatility,
)
from services.stress_service import (
    apply_correlation_stress,
    apply_joint_stress,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/portfolio")
def create_portfolio(portfolio: PortfolioRequest) -> dict[str, object]:
    """Accept and validate a portfolio payload."""
    try:
        validated = validate_portfolio(portfolio)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    tickers = [asset.ticker for asset in validated.assets]
    weights = [asset.weight for asset in validated.assets]
    weights_map = {asset.ticker: asset.weight for asset in validated.assets}

    try:
        price_df = get_historical_prices(tickers)
        returns_df = calculate_returns(price_df)
        corr_matrix = compute_correlation_matrix(returns_df)
        high_corr_pairs = get_high_correlation_pairs(corr_matrix, threshold=0.7)
        clusters = perform_clustering(corr_matrix)
        portfolio_returns = calculate_portfolio_returns(returns_df, weights)
        volatility = calculate_volatility(portfolio_returns)
        var_95 = calculate_var(portfolio_returns, confidence=0.95)
        cvar_95 = calculate_cvar(portfolio_returns, confidence=0.95)
        max_drawdown = calculate_drawdown(portfolio_returns)
        stressed_corr_matrix = apply_correlation_stress(corr_matrix)
        stressed_returns_df = apply_joint_stress(returns_df, stressed_corr_matrix)
        stressed_portfolio_returns = calculate_portfolio_returns(stressed_returns_df, weights)
        stressed_var_95 = calculate_var(stressed_portfolio_returns, confidence=0.95)
        stressed_cvar_95 = calculate_cvar(stressed_portfolio_returns, confidence=0.95)
        enb = calculate_enb(weights)
        cluster_concentration = calculate_cluster_concentration(clusters, weights_map)
        diversification_score = calculate_diversification_score(enb, len(tickers))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    logger.debug(
        "Portfolio analysis complete for tickers=%s | rows(prices)=%d rows(returns)=%d clusters=%d high_corr_pairs=%d",
        tickers,
        len(price_df),
        len(returns_df),
        len(clusters),
        len(high_corr_pairs),
    )
    logger.debug(
        "Risk metrics volatility=%.6f var95=%.6f cvar95=%.6f max_drawdown=%.6f stressed_var95=%.6f stressed_cvar95=%.6f enb=%.6f",
        volatility,
        var_95,
        cvar_95,
        max_drawdown,
        stressed_var_95,
        stressed_cvar_95,
        enb,
    )

    llm_input = {
        "volatility": volatility,
        "var": var_95,
        "cvar": cvar_95,
        "max_drawdown": max_drawdown,
        "clusters": {str(cluster_id): members for cluster_id, members in clusters.items()},
        "enb": enb,
        "diversification_score": diversification_score,
        "cluster_concentration": cluster_concentration,
        "stress": {
            "normal_var": var_95,
            "stressed_var": stressed_var_95,
            "normal_cvar": cvar_95,
            "stressed_cvar": stressed_cvar_95,
        },
    }
    if getattr(portfolio, "debug_rag", False):
        llm_input["debug_rag"] = True

    ai_result = generate_portfolio_explanation(llm_input)
    ai_explanation = str(ai_result.get("explanation", ""))
    rag_debug = ai_result.get("rag_debug")
    logger.debug(
        "Generated AI explanation for tickers=%s with response_length=%d",
        tickers,
        len(ai_explanation),
    )

    response_payload: dict[str, object] = {
        "message": "Analysis complete",
        "metrics": {
            "volatility": round(volatility, 6),
            "var": round(var_95, 6),
            "cvar": round(cvar_95, 6),
            "max_drawdown": round(max_drawdown, 6),
        },
        "clusters": {str(cluster_id): members for cluster_id, members in clusters.items()},
        "high_correlation_pairs": high_corr_pairs,
        "correlation_matrix": corr_matrix.to_dict(),
        "assets": [{"ticker": ticker, "weight": weight} for ticker, weight in weights_map.items()],
        "diversification": {
            "enb": round(enb, 6),
            "diversification_score": round(diversification_score, 6),
            "cluster_concentration": cluster_concentration,
        },
        "stress": {
            "normal_var": round(var_95, 6),
            "stressed_var": round(stressed_var_95, 6),
            "normal_cvar": round(cvar_95, 6),
            "stressed_cvar": round(stressed_cvar_95, 6),
        },
        "ai_explanation": ai_explanation,
    }

    if rag_debug:
        response_payload["rag_debug"] = rag_debug

    return response_payload
