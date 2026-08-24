"""
services/profit_service.py
--------------------------
Business logic for profit calculation.
"""

from models.profit import ProfitInput, ProfitResponse


def calculate_profit(data: ProfitInput) -> ProfitResponse:
    """
    Calculate profit from user-supplied farm and market data.

    Formula:
        expected_production = farm_area × expected_yield_per_acre
        gross_revenue       = expected_production × market_price_per_unit
        total_cost          = estimated_cost + transportation_cost
        estimated_profit    = gross_revenue - total_cost
        profit_margin_%     = (estimated_profit / gross_revenue) × 100
                              (returns 0.0 if gross_revenue is zero to avoid division by zero)
    """
    expected_production = round(data.farm_area * data.expected_yield_per_acre, 4)
    gross_revenue = round(expected_production * data.market_price_per_unit, 2)
    total_cost = round(data.estimated_cost + data.transportation_cost, 2)
    estimated_profit = round(gross_revenue - total_cost, 2)

    # Safely calculate margin — avoid division by zero
    if gross_revenue > 0:
        profit_margin = round((estimated_profit / gross_revenue) * 100, 2)
    else:
        profit_margin = 0.0

    return ProfitResponse(
        crop=data.crop,
        farm_area_acres=data.farm_area,
        expected_production_quintals=expected_production,
        gross_revenue_inr=gross_revenue,
        total_cost_inr=total_cost,
        estimated_profit_inr=estimated_profit,
        profit_margin_percent=profit_margin,
    )
