from typing import List, Optional
from pydantic import BaseModel, Field
from models.farm import FarmInput


class RecommendationItem(BaseModel):
    crop: str = Field(..., description="Recommended crop name")
    confidence_score: float = Field(..., description="Suitability score (0.0 - 1.0)")
    suitability: str = Field(..., description="Suitability category (e.g. High, Moderate)")
    reason: str = Field(..., description="Rationale for the recommendation")
    estimated_duration_days: int = Field(..., description="Estimated days to harvest")


class RecommendationResponse(BaseModel):
    status: str = "success"
    total_recommendations: int
    recommendations: List[RecommendationItem]
    farm_summary: FarmInput
    note: str = Field(
        default="Prototype rule-based recommendations. Real AI/ML recommendation engine integration interface ready.",
        description="System note"
    )
