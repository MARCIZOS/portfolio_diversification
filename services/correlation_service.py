"""Services for correlation computation and portfolio correlation insights."""

from pandas import DataFrame


def compute_correlation_matrix(returns_df: DataFrame) -> DataFrame:
    """Compute the asset return correlation matrix."""
    return returns_df.corr()


def get_high_correlation_pairs(
    corr_matrix: DataFrame, threshold: float = 0.7
) -> list[tuple[str, str, float]]:
    """Return unique asset pairs with correlation above the given threshold.

    Args:
        corr_matrix: Square correlation matrix with ticker labels.
        threshold: Minimum correlation value to include a pair.

    Returns:
        List of tuples in the form (ticker_a, ticker_b, correlation_value).
    """
    pairs: list[tuple[str, str, float]] = []
    columns = list(corr_matrix.columns)

    for left_idx in range(len(columns)):
        for right_idx in range(left_idx + 1, len(columns)):
            left_ticker = columns[left_idx]
            right_ticker = columns[right_idx]
            correlation_value = float(corr_matrix.iloc[left_idx, right_idx])
            if correlation_value > threshold:
                pairs.append((left_ticker, right_ticker, round(correlation_value, 4)))

    return pairs
