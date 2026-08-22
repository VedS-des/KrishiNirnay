from typing import Optional
from pydantic import BaseModel, Field


class FarmInput(BaseModel):
    location: str = Field(
        ...,
        min_length=1,
        description="Location/village/district of the farm",
        examples=["Mandya, Karnataka"]
    )
    latitude: Optional[float] = Field(
        None,
        description="GPS Latitude if available",
        examples=[12.52]
    )
    longitude: Optional[float] = Field(
        None,
        description="GPS Longitude if available",
        examples=[76.89]
    )
    area: float = Field(
        ...,
        gt=0,
        description="Farm area in acres/hectares (must be > 0)",
        examples=[2.5]
    )
    soil_type: str = Field(
        ...,
        min_length=1,
        description="Type of soil (e.g., Red Sandy Loam, Clay, Black, Alluvial)",
        examples=["Red Sandy Loam"]
    )
    soil_ph: float = Field(
        ...,
        ge=0.0,
        le=14.0,
        description="Soil pH value (between 0.0 and 14.0)",
        examples=[6.5]
    )
    water_availability: str = Field(
        ...,
        min_length=1,
        description="Water availability level (e.g., High, Medium, Low, Irrigated, Rainfed)",
        examples=["Medium"]
    )
    budget: float = Field(
        ...,
        ge=0.0,
        description="Farmer budget in INR (must be >= 0)",
        examples=[25000.0]
    )
    season: str = Field(
        ...,
        min_length=1,
        description="Cultivation season (e.g., Kharif, Rabi, Summer, Zaid)",
        examples=["Kharif"]
    )
    previous_crop: Optional[str] = Field(
        None,
        description="Crop grown in the previous cycle",
        examples=["Paddy"]
    )


class FarmResponse(BaseModel):
    status: str = "success"
    message: str
    data: FarmInput
