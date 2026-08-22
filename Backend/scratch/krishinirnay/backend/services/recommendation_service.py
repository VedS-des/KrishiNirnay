from typing import List
from models.farm import FarmInput
from models.recommendation import CropRecommendation


class RecommendationService:
    """
    RecommendationService handles crop recommendation business logic.
    
    ARCHITECTURE NOTE:
    Currently, this service returns validated dummy recommendation data.
    When Member 2 (AI/ML engineer) builds the actual prediction model,
    replace the dummy list below with model inference calls:
    
        Frontend -> POST /recommend -> FastAPI -> RecommendationService -> AI/ML Model -> Response
    """

    @staticmethod
    def get_recommendations(farm_data: FarmInput) -> List[CropRecommendation]:
        # Currently returning structured dummy data for frontend/testing integration
        # In future: Pass farm_data to ML model pipeline
        return [
            CropRecommendation(
                crop="Groundnut",
                score=91,
                expected_yield=8.5,
                estimated_cost=72000.0,
                expected_revenue=145000.0,
                expected_profit=73000.0,
                risk="Low",
            ),
            CropRecommendation(
                crop="Black Gram",
                score=84,
                expected_yield=5.2,
                estimated_cost=55000.0,
                expected_revenue=105000.0,
                expected_profit=50000.0,
                risk="Low",
            ),
            CropRecommendation(
                crop="Sesame",
                score=78,
                expected_yield=4.5,
                estimated_cost=50000.0,
                expected_revenue=95000.0,
                expected_profit=45000.0,
                risk="Medium",
            ),
        ]
