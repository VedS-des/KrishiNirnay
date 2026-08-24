"""
models/farm.py
--------------
Pydantic models for farm data input and response.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class FarmInput(BaseModel):
    """Input model for farm registration / recommendation request."""

    location: str = Field(..., description="Location name, e.g. 'Tamil Nadu'")
    latitude: Optional[float] = Field(None, description="GPS latitude (optional)")
    longitude: Optional[float] = Field(None, description="GPS longitude (optional)")
    area: float = Field(..., gt=0, description="Farm area in acres (must be > 0)")
    soil_type: str = Field(..., description="Soil type, e.g. 'red', 'black', 'loamy'")
    soil_ph: float = Field(..., description="Soil pH (0–14 scale)")
    water_availability: str = Field(
        ..., description="Water availability: 'low', 'medium', or 'high'"
    )
    budget: float = Field(..., ge=0, description="Available budget in INR (must be >= 0)")
    season: str = Field(..., description="Crop season: 'kharif' or 'rabi'")
    previous_crop: Optional[str] = Field(None, description="Previous crop grown on this farm")

    @field_validator("location")
    @classmethod
    def location_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("location must not be empty")
        return v.strip()

    @field_validator("soil_type")
    @classmethod
    def soil_type_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("soil_type must not be empty")
        return v.strip().lower()

    @field_validator("soil_ph")
    @classmethod
    def ph_must_be_in_range(cls, v: float) -> float:
        if not (0.0 <= v <= 14.0):
            raise ValueError("soil_ph must be between 0 and 14")
        return v

    @field_validator("water_availability")
    @classmethod
    def water_must_be_valid(cls, v: str) -> str:
        allowed = {"low", "medium", "high"}
        if v.strip().lower() not in allowed:
            raise ValueError(f"water_availability must be one of: {allowed}")
        return v.strip().lower()

    @field_validator("season")
    @classmethod
    def season_must_be_valid(cls, v: str) -> str:
        allowed = {"kharif", "rabi"}
        if v.strip().lower() not in allowed:
            raise ValueError(f"season must be one of: {allowed}")
        return v.strip().lower()


class FarmResponse(BaseModel):
    """Response returned after farm data is accepted."""

    message: str
    farm_data: FarmInput
