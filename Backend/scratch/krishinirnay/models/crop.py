from typing import List
from pydantic import BaseModel, Field


class CropDetailResponse(BaseModel):
    crop: str = Field(..., description="Common crop name")
    scientific_name: str = Field(..., description="Botanical name")
    suitable_soil: List[str] = Field(..., description="List of suitable soil types")
    ideal_ph_range: str = Field(..., description="Ideal pH range")
    water_requirement: str = Field(..., description="Water requirement description")
    suitable_seasons: List[str] = Field(..., description="Suitable agricultural seasons")
    growing_duration_days: int = Field(..., description="Typical duration in days")


class CropPlanStage(BaseModel):
    stage: str = Field(..., description="Cultivation phase name")
    time: str = Field(..., description="Timing or milestone")
    guidance: str = Field(..., description="Actionable advisory for this stage")


class CropPlanResponse(BaseModel):
    crop: str = Field(..., description="Target crop name")
    disclaimer: str = Field(
        default="Prototype/demo guidance only. Not intended as certified agronomic advice.",
        description="Advisory disclaimer"
    )
    stages: List[CropPlanStage]
