"""Business logic for validating and normalizing portfolio data."""

from models.portfolio import Asset, PortfolioRequest

WEIGHT_TOLERANCE = 1e-6


def validate_portfolio(portfolio: PortfolioRequest) -> PortfolioRequest:
    """Validate portfolio constraints and normalize weights when needed.

    Args:
        portfolio: Incoming portfolio request payload.

    Returns:
        PortfolioRequest: Validated (and potentially normalized) portfolio.

    Raises:
        ValueError: If any validation rule is violated.
    """
    if not portfolio.assets:
        raise ValueError("Portfolio must not be empty.")

    total_weight = 0.0
    cleaned_assets: list[Asset] = []

    for asset in portfolio.assets:
        ticker = asset.ticker.strip()
        if not ticker:
            raise ValueError("Ticker must be a non-empty string.")
        if asset.weight < 0:
            raise ValueError(f"Negative weight is not allowed for ticker '{ticker}'.")

        total_weight += asset.weight
        cleaned_assets.append(Asset(ticker=ticker, weight=asset.weight))

    if total_weight <= 0:
        raise ValueError("Total weight must be greater than zero.")

    if abs(total_weight - 1.0) > WEIGHT_TOLERANCE:
        raise ValueError("Total weight must equal 1 within tolerance.")

    # Normalize to ensure numerical stability for downstream consumers.
    normalized_assets = [
        Asset(ticker=asset.ticker, weight=asset.weight / total_weight)
        for asset in cleaned_assets
    ]
    return PortfolioRequest(assets=normalized_assets)
