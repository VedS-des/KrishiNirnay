from typing import List
from models.farm import FarmInput
from models.recommendation import RecommendationItem

CROP_KNOWLEDGE = [
    {
        "crop": "Groundnut",
        "suitable_soils": ["red sandy loam", "sandy loam", "loam", "red soil"],
        "min_ph": 5.5,
        "max_ph": 7.5,
        "suitable_seasons": ["kharif", "summer", "rabi"],
        "water_levels": ["low", "medium", "rainfed"],
        "duration_days": 120,
        "min_budget": 15000,
        "reason": "Well-suited for sandy/loamy soil with moderate water availability."
    },
    {
        "crop": "Black Gram",
        "suitable_soils": ["loam", "clay loam", "black soil", "alluvial"],
        "min_ph": 6.0,
        "max_ph": 7.5,
        "suitable_seasons": ["kharif", "rabi", "summer"],
        "water_levels": ["low", "medium", "rainfed"],
        "duration_days": 80,
        "min_budget": 10000,
        "reason": "Short duration pulse ideal for low-to-medium water conditions and soil fertility enrichment."
    },
    {
        "crop": "Sesame",
        "suitable_soils": ["sandy loam", "loam", "alluvial", "red soil"],
        "min_ph": 5.5,
        "max_ph": 8.0,
        "suitable_seasons": ["kharif", "summer", "zaid"],
        "water_levels": ["low", "rainfed"],
        "duration_days": 90,
        "min_budget": 8000,
        "reason": "Drought-tolerant oilseed crop with low capital and water requirements."
    },
    {
        "crop": "Rice",
        "suitable_soils": ["clay", "clay loam", "alluvial", "black soil"],
        "min_ph": 5.0,
        "max_ph": 8.0,
        "suitable_seasons": ["kharif", "rabi", "monsoon"],
        "water_levels": ["high", "irrigated", "medium"],
        "duration_days": 135,
        "min_budget": 25000,
        "reason": "High yield potential in moisture-retentive clayey/alluvial soils with sufficient water."
    },
    {
        "crop": "Maize",
        "suitable_soils": ["loam", "sandy loam", "alluvial", "red sandy loam"],
        "min_ph": 5.8,
        "max_ph": 7.8,
        "suitable_seasons": ["kharif", "rabi", "zaid", "summer"],
        "water_levels": ["medium", "high", "irrigated"],
        "duration_days": 105,
        "min_budget": 18000,
        "reason": "Versatile cereal crop adaptable across diverse soils with moderate water availability."
    }
]


def evaluate_crop_suitability(farm_data: FarmInput) -> List[RecommendationItem]:
    results: List[RecommendationItem] = []
    
    farm_soil = farm_data.soil_type.lower()
    farm_season = farm_data.season.lower()
    farm_water = farm_data.water_availability.lower()
    farm_ph = farm_data.soil_ph
    
    for crop_info in CROP_KNOWLEDGE:
        score = 0.50
        reasons = []
        
        # Soil match
        if any(soil in farm_soil or farm_soil in soil for soil in crop_info["suitable_soils"]):
            score += 0.20
            reasons.append(f"Compatible with {farm_data.soil_type} soil")
        
        # pH match
        if crop_info["min_ph"] <= farm_ph <= crop_info["max_ph"]:
            score += 0.15
            reasons.append(f"pH {farm_ph} is within ideal range ({crop_info['min_ph']}-{crop_info['max_ph']})")
        else:
            score -= 0.10
        
        # Season match
        if any(season in farm_season or farm_season in season for season in crop_info["suitable_seasons"]):
            score += 0.10
            reasons.append(f"Suitable for {farm_data.season} season")
        
        # Water match
        if any(w in farm_water or farm_water in w for w in crop_info["water_levels"]):
            score += 0.05
        
        final_score = max(0.10, min(0.98, round(score, 2)))
        
        if final_score >= 0.75:
            suitability = "High"
        elif final_score >= 0.55:
            suitability = "Moderate"
        else:
            suitability = "Low"
            
        final_reason = "; ".join(reasons) if reasons else crop_info["reason"]
        
        results.append(
            RecommendationItem(
                crop=crop_info["crop"],
                confidence_score=final_score,
                suitability=suitability,
                reason=f"{crop_info['reason']} ({final_reason})",
                estimated_duration_days=crop_info["duration_days"]
            )
        )
        
    results.sort(key=lambda x: x.confidence_score, reverse=True)
    return results
