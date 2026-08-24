"""
services/market_service.py
--------------------------
Business logic for market comparison.

FUTURE INTEGRATION POINT:
    Replace user-supplied market prices with real-time prices from
    a market data API (e.g., Agmarknet, eNAM) when provided by
    another team member.
"""

from typing import List

from models.market import MarketCompareInput, MarketCompareResponse, MarketResult


def compare_markets(data: MarketCompareInput) -> MarketCompareResponse:
    """
    Calculate net profit for each market option and rank them.

    For each market:
        gross_revenue    = quantity × price_per_unit
        total_cost       = production_cost + transportation_cost
        estimated_profit = gross_revenue - total_cost

    Markets are sorted by estimated_profit (highest first) and assigned a rank.
    """
    results: List[MarketResult] = []

    for market in data.markets:
        gross_revenue = round(data.quantity * market.price_per_unit, 2)
        total_cost = round(data.production_cost + market.transportation_cost, 2)
        estimated_profit = round(gross_revenue - total_cost, 2)

        results.append(
            MarketResult(
                market_name=market.market_name,
                price_per_unit=market.price_per_unit,
                gross_revenue_inr=gross_revenue,
                transportation_cost_inr=market.transportation_cost,
                total_cost_inr=total_cost,
                estimated_profit_inr=estimated_profit,
                rank=0,  # assigned after sorting
            )
        )

    # Sort by estimated profit descending
    results.sort(key=lambda r: r.estimated_profit_inr, reverse=True)

    # Assign ranks
    ranked: List[MarketResult] = []
    for i, result in enumerate(results):
        ranked.append(
            MarketResult(
                market_name=result.market_name,
                price_per_unit=result.price_per_unit,
                gross_revenue_inr=result.gross_revenue_inr,
                transportation_cost_inr=result.transportation_cost_inr,
                total_cost_inr=result.total_cost_inr,
                estimated_profit_inr=result.estimated_profit_inr,
                rank=i + 1,
            )
        )

    best_market = ranked[0].market_name if ranked else "N/A"

    return MarketCompareResponse(
        crop=data.crop,
        quantity_quintals=data.quantity,
        best_market=best_market,
        market_options=ranked,
    )
