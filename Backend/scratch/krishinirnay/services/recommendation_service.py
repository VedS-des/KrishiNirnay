from models.farm import FarmInput
from models.recommendation import RecommendationResponse
from services.recommendation_engine import evaluate_crop_suitability


def get_crop_recommendations(farm_data: FarmInput) -> RecommendationResponse:
    recommendations = evaluate_crop_suitability(farm_data)
    
    return RecommendationResponse(
        status="success",
        total_recommendations=len(recommendations),
        recommendations=recommendations,
        farm_summary=farm_data,
        note="Prototype rule-based recommendations. Real AI/ML recommendation engine integration interface ready."
    )
