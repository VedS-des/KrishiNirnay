"""
models/risk.py
--------------
Pydantic models for risk assessment input and response.
"""

from typing import List
from pydantic import BaseModel, Field


class RiskAssessmentInput(BaseModel):
    """Input for POST /risk-assessment."""

    crop: str = Field(..., description="Crop name, e.g. 'Groundnut'")
    location: str = Field(..., description="Location name")
    soil_type: str = Field(..., description="Soil type")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH")
    water_availability: str = Field(..., description="'low', 'medium', or 'high'")
    season: str = Field(..., description="'kharif' or 'rabi'")


class RiskDetail(BaseModel):
    """One specific risk factor identified for the crop."""

    type: str = Field(..., description="Risk category, e.g. 'Water Risk'")
    level: str = Field(..., description="'Low', 'Medium', or 'High'")
    description: str
    preventive_measure: str


class RiskAssessmentResponse(BaseModel):
    """Full risk assessment result."""

    crop: str
    location: str
    overall_risk: str = Field(..., description="'Low', 'Medium', or 'High'")
    risk_score: int = Field(..., description="Composite risk score 0–100 (lower is better)")
    risks: List[RiskDetail]
    disclaimer: str = (
        "This is a prototype rule-based risk assessment. "
        "It does NOT use real-time weather, satellite, or soil sensor data. "
        "Always consult local agricultural experts before making decisions."
    )
