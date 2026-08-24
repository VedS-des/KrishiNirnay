"""
routes/market.py
----------------
Route: POST /market/compare
Compares market options and ranks them by estimated profit.
"""

from fastapi import APIRouter
from models.market import MarketCompareInput, MarketCompareResponse
from services.market_service import compare_markets

router = APIRouter()


@router.post(
    "/market/compare",
    response_model=MarketCompareResponse,
    summary="Compare Market Options",
    description=(
        "Compares multiple market options for a given crop and quantity. "
        "Calculates gross revenue, total cost, and estimated profit for each market, "
        "then ranks them from best to worst. "
        "Uses user-supplied prices — does NOT fetch live market data."
    ),
)
def market_compare(data: MarketCompareInput) -> MarketCompareResponse:
    """Compare markets and return ranked results."""
    return compare_markets(data)
