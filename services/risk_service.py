"""Risk metric calculation services for portfolio analytics."""

import numpy as np
from pandas import DataFrame, Series

TRADING_DAYS_PER_YEAR = 252


def calculate_portfolio_returns(returns_df: DataFrame, weights: list[float]) -> Series:
    """Compute weighted daily portfolio returns from asset return matrix."""
    if returns_df.empty:
        raise ValueError("Returns data is empty.")
    if len(weights) != len(returns_df.columns):
        raise ValueError("Weights length must match number of assets.")

    weight_array = np.asarray(weights, dtype=float)
    portfolio_values = returns_df.to_numpy() @ weight_array
    return Series(portfolio_values, index=returns_df.index, name="portfolio_return")


def calculate_volatility(portfolio_returns: Series) -> float:
    """Compute annualized portfolio volatility from daily return standard deviation."""
    daily_std = float(portfolio_returns.std(ddof=1))
    return daily_std * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_var(portfolio_returns: Series, confidence: float = 0.95) -> float:
    """Compute historical Value at Risk (VaR) at a given confidence level."""
    percentile = (1.0 - confidence) * 100.0
    return float(np.percentile(portfolio_returns, percentile))


def calculate_cvar(portfolio_returns: Series, confidence: float = 0.95) -> float:
    """Compute historical Conditional VaR (Expected Shortfall)."""
    var_value = calculate_var(portfolio_returns, confidence=confidence)
    tail_losses = portfolio_returns[portfolio_returns <= var_value]
    if tail_losses.empty:
        return var_value
    return float(tail_losses.mean())


def calculate_drawdown(portfolio_returns: Series) -> float:
    """Compute maximum drawdown from cumulative portfolio returns."""
    cumulative = (1.0 + portfolio_returns).cumprod()
    running_peak = cumulative.cummax()
    drawdown = (cumulative / running_peak) - 1.0
    return float(drawdown.min())
