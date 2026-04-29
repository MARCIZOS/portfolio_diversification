"""Data ingestion and return-calculation services for market data."""

from typing import List

import pandas as pd
import yfinance as yf
from pandas import DataFrame


def _fetch_single_ticker_history(ticker: str) -> pd.Series:
    """Fetch adjusted close series for one ticker."""
    history = yf.Ticker(ticker).history(
        period="1y",
        interval="1d",
        auto_adjust=False,
        timeout=20,
    )
    if history.empty or "Adj Close" not in history.columns:
        return pd.Series(dtype="float64", name=ticker)
    series = history["Adj Close"].copy()
    series.name = ticker
    return series


def get_historical_prices(tickers: List[str]) -> DataFrame:
    """Fetch one year of daily adjusted close prices for given tickers.

    Args:
        tickers: List of ticker symbols.

    Returns:
        DataFrame: Daily adjusted close prices indexed by date.

    Raises:
        ValueError: If tickers are empty or data is missing for all tickers.
        RuntimeError: If external data fetching fails.
    """
    if not tickers:
        raise ValueError("Ticker list cannot be empty.")

    try:
        raw_data = yf.download(
            tickers=tickers,
            period="1y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            group_by="column",
            threads=True,
            timeout=20,
        )
    except Exception as exc:  # pragma: no cover - external API behavior
        raise RuntimeError("Failed to fetch market data from provider.") from exc

    if raw_data.empty:
        raise RuntimeError("No market data returned by provider.")

    if isinstance(raw_data.columns, pd.MultiIndex):
        if "Adj Close" not in raw_data.columns.get_level_values(0):
            raise RuntimeError("Adjusted close prices are unavailable.")
        price_df = raw_data["Adj Close"].copy()
    else:
        # Single ticker shape from yfinance.
        if "Adj Close" not in raw_data.columns:
            raise RuntimeError("Adjusted close prices are unavailable.")
        single_ticker = tickers[0]
        price_df = raw_data[["Adj Close"]].rename(columns={"Adj Close": single_ticker})

    if isinstance(price_df, pd.Series):
        price_df = price_df.to_frame(name=tickers[0])

    price_df = price_df.sort_index()
    price_df = price_df.ffill()
    price_df = price_df.dropna(how="all")

    missing_tickers = [ticker for ticker in tickers if ticker not in price_df.columns]
    if missing_tickers:
        raise ValueError(f"Invalid or unavailable tickers: {', '.join(missing_tickers)}")

    # Retry empty series once per ticker (helps when batched download misses symbols).
    no_data_tickers = [ticker for ticker in tickers if price_df[ticker].isna().all()]
    for ticker in no_data_tickers:
        retry_series = _fetch_single_ticker_history(ticker)
        if not retry_series.empty:
            price_df[ticker] = price_df[ticker].combine_first(retry_series)

    # Remove assets with no valid data points across the full period.
    no_data_tickers = [ticker for ticker in tickers if price_df[ticker].isna().all()]
    if no_data_tickers:
        raise ValueError(f"No data found for tickers: {', '.join(no_data_tickers)}")

    return price_df[tickers]


def calculate_returns(price_df: DataFrame) -> DataFrame:
    """Calculate daily percentage returns from a price DataFrame."""
    returns = price_df.pct_change()
    return returns.dropna(how="any")
