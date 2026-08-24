"""
services/recommendation_service.py
----------------------------------
AI-powered crop recommendation service.

This service connects the FastAPI backend with the reusable
recommendation engine in ai/recommendation_engine.py.
"""

import json
from pathlib import Path
from typing import List

from models.recommendation import RecommendationInput, CropRecommendation
from ai.recommendation_engine import (
    calculate_overall_score,
    generate_reason,
)


# Load AI crop dataset
CROP_DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "ai"
    / "data"
    / "crops.json"
)

with open(CROP_DATA_PATH, "r", encoding="utf-8") as file:
    AI_CROPS = json.load(file)


def get_crop_recommendations(
    farm: RecommendationInput,
) -> List[CropRecommendation]:
    """
    Generate crop recommendations using the AI recommendation engine.

    The engine evaluates:
    - Soil type
    - Soil pH
    - Water availability
    - Season

    Economic estimates are calculated using the existing backend
    crop dataset.
    """

    results: List[CropRecommendation] = []

    for crop in AI_CROPS:

        # Build farmer data expected by the AI engine
        farmer = {
            "location": farm.location,
            "area": farm.area,
            "soil_type": farm.soil_type,
            "soil_ph": farm.soil_ph,
            "water_availability": farm.water_availability,
            "budget": farm.budget,
            "season": farm.season,
        }

        # AI suitability score
        suitability_score = calculate_overall_score(
            farmer,
            crop,
        )

        # AI-generated reasons
        reasons = generate_reason(
            farmer,
            crop,
        )

        # Find matching economic data from backend dataset
        crop_name = crop["name"]

        from data.crop_data import CROPS

        backend_crop = CROPS.get(crop_name)

        if backend_crop is None:
            continue

        # Economic calculations
        cost_per_acre = backend_crop[
            "estimated_cost_per_acre_inr"
        ]

        total_cost = cost_per_acre * farm.area

        yield_total = (
            backend_crop["estimated_yield_per_acre_quintals"]
            * farm.area
        )

        revenue = (
            yield_total
            * backend_crop["estimated_market_price_per_quintal_inr"]
        )

        profit = revenue - total_cost

        results.append(
            CropRecommendation(
                crop=crop_name,
                suitability_score=round(
                    suitability_score
                ),
                reason="; ".join(reasons)
                if reasons
                else "Crop evaluated based on farm conditions",
                estimated_yield_per_acre=backend_crop[
                    "estimated_yield_per_acre_quintals"
                ],
                estimated_cost_inr=round(
                    total_cost,
                    2,
                ),
                estimated_revenue_inr=round(
                    revenue,
                    2,
                ),
                estimated_profit_inr=round(
                    profit,
                    2,
                ),
                risk_level=backend_crop[
                    "risk_level"
                ],
            )
        )

    # Highest AI suitability first
    results.sort(
        key=lambda r: r.suitability_score,
        reverse=True,
    )

    return results