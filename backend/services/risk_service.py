"""
services/risk_service.py
------------------------
Rule-based prototype risk assessment service.

DISCLAIMER:
    This is a prototype rule engine based on agronomic heuristics.
    It does NOT use real-time weather, satellite imagery, or sensor data.
    It is NOT a trained ML/AI model.

FUTURE INTEGRATION POINT:
    Replace or extend this service with real weather API data when
    another team member provides integration credentials and endpoints.
"""

from typing import List

from data.crop_data import CROPS
from models.risk import RiskAssessmentInput, RiskAssessmentResponse, RiskDetail


def _assess_water_risk(crop_water: str, farm_water: str) -> RiskDetail:
    """Compare crop water requirement with farm water availability."""
    water_map = {"low": 1, "medium": 2, "high": 3}
    crop_level = water_map.get(crop_water.lower(), 2)
    farm_level = water_map.get(farm_water.lower(), 2)

    if farm_level >= crop_level:
        return RiskDetail(
            type="Water Risk",
            level="Low",
            description=f"Farm water availability ({farm_water}) meets crop requirement ({crop_water}).",
            preventive_measure="Maintain consistent irrigation schedule during critical growth stages.",
        )
    elif farm_level == crop_level - 1:
        return RiskDetail(
            type="Water Risk",
            level="Medium",
            description=(
                f"Farm water availability ({farm_water}) is below the crop's requirement ({crop_water}). "
                "Yield may be reduced without supplementary irrigation."
            ),
            preventive_measure=(
                "Install drip or sprinkler irrigation. "
                "Irrigate at critical stages: germination, flowering, and grain filling."
            ),
        )
    else:
        return RiskDetail(
            type="Water Risk",
            level="High",
            description=(
                f"Farm water availability ({farm_water}) is significantly below crop requirement ({crop_water}). "
                "Crop failure is likely without a reliable water source."
            ),
            preventive_measure=(
                "Consider a different crop with lower water requirements, "
                "or invest in a reliable water source before planting."
            ),
        )


def _assess_soil_risk(suitable_soils: List[str], farm_soil: str) -> RiskDetail:
    """Check whether the farm's soil type is suitable for the crop."""
    if farm_soil.lower() in [s.lower() for s in suitable_soils]:
        return RiskDetail(
            type="Soil Suitability Risk",
            level="Low",
            description=f"Soil type '{farm_soil}' is suitable for this crop.",
            preventive_measure="Maintain organic matter. Carry out soil testing before each season.",
        )
    else:
        return RiskDetail(
            type="Soil Suitability Risk",
            level="Medium",
            description=(
                f"Soil type '{farm_soil}' is not in the preferred list {suitable_soils}. "
                "Crop may still grow but with reduced efficiency."
            ),
            preventive_measure=(
                "Improve soil structure with organic amendments. "
                "Carry out a soil test and adjust pH and nutrients accordingly."
            ),
        )


def _assess_ph_risk(ph_min: float, ph_max: float, farm_ph: float) -> RiskDetail:
    """Check whether the farm's soil pH is within the crop's ideal range."""
    if ph_min <= farm_ph <= ph_max:
        return RiskDetail(
            type="Soil pH Risk",
            level="Low",
            description=f"Soil pH {farm_ph} is within the ideal range ({ph_min}–{ph_max}).",
            preventive_measure="Monitor pH seasonally. Avoid excess chemical fertiliser application.",
        )
    elif abs(farm_ph - ph_min) <= 0.5 or abs(farm_ph - ph_max) <= 0.5:
        return RiskDetail(
            type="Soil pH Risk",
            level="Medium",
            description=(
                f"Soil pH {farm_ph} is slightly outside the ideal range ({ph_min}–{ph_max}). "
                "Nutrient availability may be slightly affected."
            ),
            preventive_measure=(
                "Apply lime to raise pH or sulphur to lower pH as needed. "
                "Re-test soil after 3 months."
            ),
        )
    else:
        return RiskDetail(
            type="Soil pH Risk",
            level="High",
            description=(
                f"Soil pH {farm_ph} is well outside the ideal range ({ph_min}–{ph_max}). "
                "Significant nutrient deficiency or toxicity is likely."
            ),
            preventive_measure=(
                "Do not plant without correcting soil pH. "
                "Consult a local agricultural officer for soil amendment strategy."
            ),
        )


def _assess_seasonal_risk(suitable_seasons: List[str], farm_season: str) -> RiskDetail:
    """Check season suitability."""
    if farm_season.lower() in [s.lower() for s in suitable_seasons]:
        return RiskDetail(
            type="Seasonal Risk",
            level="Low",
            description=f"This crop is well-suited to the {farm_season} season.",
            preventive_measure="Follow the recommended sowing calendar for your region.",
        )
    else:
        return RiskDetail(
            type="Seasonal Risk",
            level="High",
            description=(
                f"This crop is typically grown in {suitable_seasons}, not in {farm_season}. "
                "Growing outside the recommended season significantly increases risk."
            ),
            preventive_measure=(
                "Strongly consider waiting for the correct season, or choose a crop "
                f"that is recommended for the {farm_season} season."
            ),
        )


def _assess_pest_risk(crop_name: str) -> RiskDetail:
    """
    Provide generic pest/disease risk guidance.

    FUTURE INTEGRATION POINT:
    Replace with real-time pest/disease alerts from an external API
    or ML-based prediction model when available.
    """
    # Prototype: return a standard medium risk with crop-specific note
    pest_notes = {
        "Groundnut": "Monitor for leaf spot, tikka disease, and stem rot.",
        "Black Gram": "Watch for pod borers, leaf-eating caterpillars, and yellow mosaic virus.",
        "Sesame": "Monitor for phyllody disease and gall midge. Remove infected plants promptly.",
        "Rice": "Common risks include blast, brown planthopper, and stem borer.",
        "Maize": "Monitor for fall armyworm and stem borer, especially in early growth.",
    }
    note = pest_notes.get(crop_name, "Monitor regularly for common pests and diseases in your region.")

    return RiskDetail(
        type="Pest & Disease Risk",
        level="Medium",
        description=(
            f"Pest and disease risk is assessed as Medium for {crop_name} (prototype estimate). "
            f"{note}"
        ),
        preventive_measure=(
            "Practice crop rotation. Use certified disease-free seeds. "
            "Apply appropriate pesticides/fungicides only when necessary. "
            "Consult local extension services for region-specific alerts."
        ),
    )


# Level → score mapping
_LEVEL_SCORE = {"Low": 10, "Medium": 30, "High": 60}


def get_risk_assessment(data: RiskAssessmentInput) -> RiskAssessmentResponse:
    """
    Run rule-based risk assessment for the given crop and farm conditions.

    Returns a RiskAssessmentResponse with individual risk details and
    an overall composite risk score.
    """
    crop = CROPS.get(data.crop)
    # Fallback: case-insensitive search
    if crop is None:
        for key in CROPS:
            if key.lower() == data.crop.lower():
                crop = CROPS[key]
                data = data.model_copy(update={"crop": key})
                break

    if crop is None:
        # Unknown crop — return a generic medium risk response
        risks = [
            RiskDetail(
                type="Unknown Crop Risk",
                level="High",
                description=f"'{data.crop}' is not in the prototype dataset. Risk cannot be assessed.",
                preventive_measure="Use one of the supported crops or consult an agricultural expert.",
            )
        ]
        return RiskAssessmentResponse(
            crop=data.crop,
            location=data.location,
            overall_risk="High",
            risk_score=80,
            risks=risks,
        )

    risks: List[RiskDetail] = [
        _assess_water_risk(crop["water_requirement"], data.water_availability),
        _assess_soil_risk(crop["suitable_soils"], data.soil_type),
        _assess_ph_risk(crop["ideal_ph_min"], crop["ideal_ph_max"], data.soil_ph),
        _assess_seasonal_risk(crop["suitable_seasons"], data.season),
        _assess_pest_risk(data.crop),
    ]

    # Calculate composite score (average of individual risk scores, capped at 100)
    total_score = sum(_LEVEL_SCORE.get(r.level, 30) for r in risks)
    avg_score = min(int(total_score / len(risks)), 100)

    if avg_score <= 15:
        overall = "Low"
    elif avg_score <= 35:
        overall = "Medium"
    else:
        overall = "High"

    return RiskAssessmentResponse(
        crop=data.crop,
        location=data.location,
        overall_risk=overall,
        risk_score=avg_score,
        risks=risks,
    )
