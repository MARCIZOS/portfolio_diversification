"""Lightweight RAG service using sentence-transformers + FAISS."""

from __future__ import annotations

import logging
import threading
from typing import Iterable

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
logger = logging.getLogger(__name__)

_KNOWLEDGE_BASE: list[dict[str, str]] = [
    {"title": "Diversification principle", "content": "Diversification reduces risk when assets have low or negative correlation."},
    {"title": "False diversification", "content": "Holding many assets does not ensure diversification if they are highly correlated."},
    {"title": "Sector concentration risk", "content": "Concentrating investments in a single sector increases exposure to sector-specific risks."},
    {"title": "Geographic diversification", "content": "International exposure reduces dependence on a single economy."},
    {"title": "Asset class diversification", "content": "Combining equities, bonds, and commodities improves portfolio stability."},
    {"title": "Correlation risk", "content": "Highly correlated assets tend to move together, reducing diversification benefits."},
    {"title": "Correlation in crises", "content": "Asset correlations often increase during market stress, reducing diversification."},
    {"title": "Low correlation assets", "content": "Assets with low correlation improve portfolio resilience."},
    {"title": "Hidden correlation", "content": "Assets in the same industry often have hidden correlations."},
    {"title": "Cluster concentration risk", "content": "High cluster concentration indicates exposure to a single risk factor."},
    {"title": "Cluster diversification", "content": "Diversifying across clusters improves portfolio robustness."},
    {"title": "Single cluster exposure", "content": "Portfolios concentrated in one cluster behave like a single asset."},
    {"title": "Volatility interpretation", "content": "Higher volatility indicates greater uncertainty in returns."},
    {"title": "VaR meaning", "content": "Value at Risk estimates the worst expected loss at a given confidence level."},
    {"title": "CVaR meaning", "content": "CVaR measures the average loss beyond the VaR threshold."},
    {"title": "Tail risk", "content": "Tail risk refers to extreme losses in rare scenarios."},
    {"title": "Drawdown definition", "content": "Maximum drawdown measures the largest peak-to-trough loss."},
    {"title": "Drawdown risk", "content": "Large drawdowns can significantly erode capital and require high recovery returns."},
    {"title": "Stress scenario", "content": "Stress testing evaluates portfolio performance under extreme conditions."},
    {"title": "Stress correlation", "content": "During stress, correlations increase and diversification weakens."},
    {"title": "Volatility spike", "content": "Market crises often lead to sharp increases in volatility."},
    {"title": "Balanced portfolio", "content": "Balanced portfolios combine growth and defensive assets."},
    {"title": "Risk-return tradeoff", "content": "Higher expected returns usually come with higher risk."},
    {"title": "Position sizing", "content": "Proper position sizing helps control portfolio risk."},
    {"title": "Overconcentration", "content": "Large allocations to a few assets increase portfolio risk."},
    {"title": "Bond diversification", "content": "Bonds reduce volatility and provide stability in portfolios."},
    {"title": "Flight to safety", "content": "Investors move to bonds during market stress."},
    {"title": "Interest rate risk", "content": "Bond prices fall when interest rates rise."},
    {"title": "Gold hedge", "content": "Gold often performs well during economic uncertainty."},
    {"title": "Inflation hedge", "content": "Gold can protect against inflation risks."},
    {"title": "Equity volatility", "content": "Equities are more volatile than bonds but offer higher returns."},
    {"title": "Growth stock risk", "content": "Growth stocks are sensitive to interest rate changes."},
    {"title": "Market beta", "content": "High beta stocks amplify market movements."},
    {"title": "ENB meaning", "content": "Effective Number of Bets measures true diversification."},
    {"title": "ENB limitation", "content": "ENB can overstate diversification if assets are correlated."},
    {"title": "Diversification score", "content": "Diversification score reflects distribution of risk across assets."},
    {"title": "Risk budgeting", "content": "Risk budgeting allocates capital based on risk contribution."},
    {"title": "Stop loss strategy", "content": "Stop losses limit downside risk."},
    {"title": "Rebalancing", "content": "Rebalancing maintains desired portfolio allocation."},
    {"title": "Market cycles", "content": "Markets go through expansion, peak, contraction, and recovery phases."},
    {"title": "Liquidity risk", "content": "Low liquidity assets are harder to sell during stress."},
    {"title": "Drawdown recovery", "content": "Large losses require higher gains to recover."},
    {"title": "Sharpe ratio", "content": "Sharpe ratio measures return per unit of risk."},
    {"title": "Systematic risk", "content": "Systematic risk affects the entire market."},
    {"title": "Idiosyncratic risk", "content": "Idiosyncratic risk is asset-specific and can be diversified away."},
    {"title": "Defensive allocation", "content": "Defensive assets reduce portfolio downside risk."},
    {"title": "Aggressive allocation", "content": "Aggressive portfolios focus on growth but carry higher risk."},
    {"title": "Portfolio optimization", "content": "Optimization seeks best risk-return combination."},
]

_index_lock = threading.Lock()
_index: faiss.Index | None = None
_documents: list[str] | None = None
_model: SentenceTransformer | None = None


def _build_documents(knowledge_base: Iterable[dict[str, str]]) -> list[str]:
    documents: list[str] = []
    for item in knowledge_base:
        title = item.get("title", "").strip()
        content = item.get("content", "").strip()
        if not content:
            continue
        header = f"{title}: " if title else ""
        documents.append(f"{header}{content}")
    return documents


def _get_index() -> tuple[faiss.Index, list[str], SentenceTransformer]:
    global _index, _documents, _model
    if _index is not None and _documents is not None and _model is not None:
        return _index, _documents, _model

    with _index_lock:
        if _index is not None and _documents is not None and _model is not None:
            return _index, _documents, _model

        logger.info("Initializing RAG index with model %s", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)
        _documents = _build_documents(_KNOWLEDGE_BASE)
        if not _documents:
            raise RuntimeError("RAG knowledge base is empty.")

        embeddings = _model.encode(_documents, normalize_embeddings=True)
        embeddings = np.asarray(embeddings, dtype="float32")

        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        _index = index
        return _index, _documents, _model


def retrieve_context(query: str, k: int = 3) -> str:
    """Retrieve top-k relevant documents as a single string."""
    if not query:
        return ""

    try:
        index, documents, model = _get_index()
        query_vector = model.encode([query], normalize_embeddings=True)
        query_vector = np.asarray(query_vector, dtype="float32")

        scores, indices = index.search(query_vector, k)
        matches: list[str] = []
        for idx in indices[0]:
            if idx < 0 or idx >= len(documents):
                continue
            matches.append(documents[idx])

        return "\n\n".join(matches)
    except Exception as exc:  # pragma: no cover - defensive against runtime model issues
        logger.exception("RAG retrieval failed: %s", exc)
        return ""
