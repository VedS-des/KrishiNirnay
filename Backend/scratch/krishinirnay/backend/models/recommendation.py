from typing import List
from pydantic import BaseModel, Field


class CropRecommendation(BaseModel):
    crop: str = Field(..., description="Name of the recommended crop", example="Groundnut")
    score: int = Field(..., description="Suitability score (0-100)", example=91)
    expected_yield: float = Field(..., description="Expected yield per acre (in quintals/tons)", example=8.5)
    estimated_cost: float = Field(..., description="Estimated cost of cultivation in INR", example=72000.0)
    expected_revenue: float = Field(..., description="Expected market revenue in INR", example=145000.0)
    expected_profit: float = Field(..., description="Expected net profit in INR", example=73000.0)
    risk: str = Field(..., description="Risk assessment level (Low, Medium, High)", example="Low")


class RecommendationResponse(BaseModel):
    recommendations: List[CropRecommendation]
