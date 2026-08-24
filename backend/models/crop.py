"""
models/crop.py
--------------
Pydantic models for crop information and cultivation plan responses.
"""

from typing import List
from pydantic import BaseModel


class CropInfo(BaseModel):
    """Basic crop information returned by GET /crops/{crop_name}."""

    name: str
    scientific_name: str
    suitable_soils: List[str]
    ideal_ph_min: float
    ideal_ph_max: float
    water_requirement: str
    suitable_seasons: List[str]
    growing_duration_days: int
    notes: str


class CultivationStage(BaseModel):
    """One stage in a crop's cultivation lifecycle."""

    stage: str
    time: str
    guidance: str


class CultivationPlan(BaseModel):
    """Full cultivation plan for a crop."""

    crop: str
    stages: List[CultivationStage]
    disclaimer: str = (
        "This cultivation plan is prototype/demo guidance only. "
        "Always consult a local agricultural extension officer for region-specific advice."
    )
