"""
models/market.py
----------------
Pydantic models for market comparison input and response.
"""

from typing import List
from pydantic import BaseModel, Field


class MarketOption(BaseModel):
    """One market option supplied by the user."""

    market_name: str = Field(..., description="Name of the market")
    price_per_unit: float = Field(..., gt=0, description="Price per quintal in INR")
    transportation_cost: float = Field(..., ge=0, description="Transportation cost in INR")


class MarketCompareInput(BaseModel):
    """Input for POST /market/compare."""

    crop: str = Field(..., description="Crop name")
    quantity: float = Field(..., gt=0, description="Quantity to sell in quintals")
    production_cost: float = Field(..., ge=0, description="Total production cost in INR")
    markets: List[MarketOption] = Field(
        ..., min_length=1, description="List of markets to compare (at least 1)"
    )


class MarketResult(BaseModel):
    """Result for one market option after calculation."""

    market_name: str
    price_per_unit: float
    gross_revenue_inr: float
    transportation_cost_inr: float
    total_cost_inr: float
    estimated_profit_inr: float
    rank: int


class MarketCompareResponse(BaseModel):
    """Ranked market comparison result."""

    crop: str
    quantity_quintals: float
    best_market: str
    market_options: List[MarketResult]
    disclaimer: str = (
        "Market prices are based on user-supplied or prototype data. "
        "This endpoint does NOT provide live market prices. "
        "It is designed so real market data can be integrated later."
    )
