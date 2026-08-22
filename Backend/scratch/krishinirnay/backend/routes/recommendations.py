from fastapi import APIRouter
from models.farm import FarmInput
from models.recommendation import RecommendationResponse
from services.recommendation_service import RecommendationService

router = APIRouter(tags=["Recommendations"])


@router.post("/recommend", response_model=RecommendationResponse, summary="Get Crop Recommendations")
def get_crop_recommendations(farm: FarmInput):
    """
    Receives farmer and farm conditions, runs recommendation logic
    via RecommendationService, and returns suitable crops with profitability & risk metrics.
    """
    recommendations = RecommendationService.get_recommendations(farm)
    return {"recommendations": recommendations}
