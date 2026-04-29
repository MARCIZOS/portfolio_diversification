"""Pydantic models for portfolio input payloads."""

from pydantic import BaseModel, Field


class Asset(BaseModel):
    """Represents one portfolio asset and its allocation weight."""

    ticker: str = Field(..., description="Asset ticker symbol")
    weight: float = Field(..., description="Asset weight in the portfolio")


class PortfolioRequest(BaseModel):
    """Request model containing a list of portfolio assets."""

    assets: list[Asset] = Field(..., description="List of portfolio assets")
    debug_rag: bool = Field(False, description="Return RAG debug context when true")
