from typing import Dict, List


def calculate_soil_score(farmer: Dict, crop: Dict) -> float:
    score = 0

    if farmer["soil_type"].lower() in [s.lower() for s in crop["soil_types"]]:
        score += 70

    if crop["ph_min"] <= farmer["soil_ph"] <= crop["ph_max"]:
        score += 30

    return score


def calculate_water_score(farmer: Dict, crop: Dict) -> float:
    farmer_water = farmer["water_availability"].lower()
    crop_water = crop["water_requirement"].lower()

    if farmer_water == crop_water:
        return 100

    if farmer_water == "medium" and crop_water == "low":
        return 80

    if farmer_water == "high" and crop_water == "medium":
        return 90

    if farmer_water == "high" and crop_water == "low":
        return 100

    return 30


def calculate_season_score(farmer: Dict, crop: Dict) -> float:
    if farmer["season"].lower() in [s.lower() for s in crop["seasons"]]:
        return 100

    return 30


def calculate_overall_score(farmer: Dict, crop: Dict) -> float:
    soil_score = calculate_soil_score(farmer, crop)
    water_score = calculate_water_score(farmer, crop)
    season_score = calculate_season_score(farmer, crop)

    return (
        soil_score * 0.40
        + water_score * 0.30
        + season_score * 0.30
    )


def generate_reason(farmer: Dict, crop: Dict) -> List[str]:
    reasons = []

    soil_score = calculate_soil_score(farmer, crop)
    water_score = calculate_water_score(farmer, crop)
    season_score = calculate_season_score(farmer, crop)

    if soil_score >= 70:
        reasons.append("Suitable soil")

    if crop["ph_min"] <= farmer["soil_ph"] <= crop["ph_max"]:
        reasons.append("Suitable soil pH")

    if water_score >= 80:
        reasons.append("Suitable water availability")

    if season_score == 100:
        reasons.append("Suitable season")

    return reasons


def calculate_final_score(suitability_score: float, profit: float) -> float:
    profit_score = max(0, min(100, (profit / 50000) * 100))

    return (
        suitability_score * 0.70
        + profit_score * 0.30
    )


def recommend_crops(farmer: Dict, crops: List[Dict]) -> List[Dict]:
    recommendations = []

    for crop in crops:
        suitability_score = calculate_overall_score(farmer, crop)

        recommendations.append({
            "name": crop["name"],
            "suitability_score": suitability_score,
            "reasons": generate_reason(farmer, crop)
        })

    recommendations.sort(
        key=lambda x: x["suitability_score"],
        reverse=True
    )

    return recommendations