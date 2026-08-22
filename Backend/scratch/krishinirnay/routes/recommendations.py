from fastapi import APIRouter
from models.farm import FarmInput
from models.recommendation import RecommendationResponse
from services.recommendation_service import get_crop_recommendations

router = APIRouter(prefix="/recommend", tags=["Recommendations"])


@router.post("", response_model=RecommendationResponse, summary="Get crop recommendations for a farm")
def recommend_crops(farm_data: FarmInput):
    return get_crop_recommendations(farm_data)
