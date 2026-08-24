"""
services/recommendation_service.py
------------------------------------
Business logic for crop recommendations.

ARCHITECTURE NOTE:
    This service provides the interface between the route layer and the
    recommendation engine. The current implementation uses a simple
    rule-based prototype engine.

    FUTURE INTEGRATION POINT:
    When another team member provides a trained AI/ML model, replace
    the body of `get_crop_recommendations()` with a call to the ML model.
    The function signature and return type should remain the same so the
    route layer does not need to change.

DISCLAIMER:
    The current logic is a rule-based prototype. It is NOT a trained
    AI/ML model and should not be presented as one.
"""

from typing import List

from data.crop_data import CROPS
from models.recommendation import RecommendationInput, CropRecommendation


def get_crop_recommendations(farm: RecommendationInput) -> List[CropRecommendation]:
    """
    Generate crop recommendations for the given farm data.

    Current implementation: rule-based prototype that scores each supported
    crop against the farm's soil type, pH, water availability, season, and
    budget.

    Returns a list of CropRecommendation objects sorted by suitability score
    (highest first).
    """
    results: List[CropRecommendation] = []

    for crop_name, crop in CROPS.items():
        score = 0
        reasons = []

        # --- Season match ---
        if farm.season.lower() in crop["suitable_seasons"]:
            score += 30
            reasons.append(f"suitable for {farm.season} season")
        else:
            reasons.append(f"not ideal for {farm.season} season")

        # --- Soil type match ---
        if farm.soil_type.lower() in [s.lower() for s in crop["suitable_soils"]]:
            score += 25
            reasons.append(f"grows well in {farm.soil_type} soil")
        else:
            reasons.append(f"not optimal for {farm.soil_type} soil")

        # --- pH match ---
        if crop["ideal_ph_min"] <= farm.soil_ph <= crop["ideal_ph_max"]:
            score += 20
            reasons.append(f"soil pH {farm.soil_ph} is within ideal range")
        elif abs(farm.soil_ph - crop["ideal_ph_min"]) <= 0.5 or abs(farm.soil_ph - crop["ideal_ph_max"]) <= 0.5:
            score += 10
            reasons.append(f"soil pH {farm.soil_ph} is close to ideal range")
        else:
            reasons.append(f"soil pH {farm.soil_ph} is outside ideal range")

        # --- Water availability match ---
        water_map = {"low": 1, "medium": 2, "high": 3}
        farm_water = water_map.get(farm.water_availability.lower(), 2)
        crop_water = water_map.get(crop["water_requirement"].lower(), 2)
        if farm_water >= crop_water:
            score += 15
            reasons.append(f"water availability is sufficient")
        else:
            reasons.append(f"water availability may be insufficient for this crop")

        # --- Budget check ---
        cost_per_acre = crop["estimated_cost_per_acre_inr"]
        total_cost = cost_per_acre * farm.area
        if farm.budget >= total_cost:
            score += 10
            reasons.append(f"within budget")
        elif farm.budget >= total_cost * 0.8:
            score += 5
            reasons.append(f"slightly over budget — manageable")
        else:
            reasons.append(f"budget may be insufficient for full area")

        # Build economics estimates
        yield_total = crop["estimated_yield_per_acre_quintals"] * farm.area
        revenue = yield_total * crop["estimated_market_price_per_quintal_inr"]
        profit = revenue - total_cost

        results.append(
            CropRecommendation(
                crop=crop_name,
                suitability_score=min(score, 100),
                reason="; ".join(reasons),
                estimated_yield_per_acre=crop["estimated_yield_per_acre_quintals"],
                estimated_cost_inr=round(total_cost, 2),
                estimated_revenue_inr=round(revenue, 2),
                estimated_profit_inr=round(profit, 2),
                risk_level=crop["risk_level"],
            )
        )

    # Sort by suitability score descending
    results.sort(key=lambda r: r.suitability_score, reverse=True)
    return results
