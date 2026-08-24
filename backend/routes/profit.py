"""
routes/profit.py
----------------
Route: POST /profit
Calculates estimated profit from farm and market data.
"""

from fastapi import APIRouter
from models.profit import ProfitInput, ProfitResponse
from services.profit_service import calculate_profit

router = APIRouter()


@router.post(
    "/profit",
    response_model=ProfitResponse,
    summary="Calculate Profit Estimate",
    description=(
        "Calculates expected production, gross revenue, total cost, "
        "estimated profit, and profit margin based on user-supplied values. "
        "All results are estimates."
    ),
)
def profit_estimate(data: ProfitInput) -> ProfitResponse:
    """Calculate and return profit estimates."""
    return calculate_profit(data)
