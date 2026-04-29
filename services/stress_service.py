"""Stress testing services for portfolio scenario analysis."""

import numpy as np
from pandas import DataFrame


def apply_correlation_stress(corr_matrix: DataFrame) -> DataFrame:
    """Shift correlations toward 0.9 to simulate crisis co-movement."""
    stressed_corr = corr_matrix + (0.9 - corr_matrix) * 0.5
    stressed_values = np.array(stressed_corr.to_numpy(), dtype=float, copy=True)
    stressed_values = (stressed_values + stressed_values.T) / 2.0
    np.fill_diagonal(stressed_values, 1.0)
    stressed_values = np.clip(stressed_values, a_min=-1.0, a_max=1.0)
    return DataFrame(stressed_values, index=corr_matrix.index, columns=corr_matrix.columns)


def apply_volatility_stress(returns_df: DataFrame, factor: float = 1.5) -> DataFrame:
    """Scale returns to represent volatility expansion under stress."""
    return returns_df * factor


def apply_joint_stress(returns_df: DataFrame, stressed_corr: DataFrame) -> DataFrame:
    """Apply correlation + volatility stress to return series."""
    means = returns_df.mean()
    stds = returns_df.std(ddof=1).replace(0.0, 1e-8)
    standardized = (returns_df - means) / stds

    original_corr = returns_df.corr().to_numpy()
    target_corr = stressed_corr.to_numpy()

    jitter = 1e-8
    original_chol = np.linalg.cholesky(original_corr + np.eye(len(original_corr)) * jitter)
    target_chol = np.linalg.cholesky(target_corr + np.eye(len(target_corr)) * jitter)

    whitened = standardized.to_numpy() @ np.linalg.inv(original_chol.T)
    corr_stressed_standardized = whitened @ target_chol.T

    corr_stressed_returns = DataFrame(
        corr_stressed_standardized,
        index=returns_df.index,
        columns=returns_df.columns,
    )
    corr_stressed_returns = corr_stressed_returns.mul(stds, axis=1).add(means, axis=1)
    return apply_volatility_stress(corr_stressed_returns, factor=1.5)
