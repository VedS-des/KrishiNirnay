from typing import Optional
from pydantic import BaseModel, Field


class FarmInput(BaseModel):
    location: str = Field(..., description="Location/State/District of the farm", example="Tamil Nadu")
    latitude: Optional[float] = Field(default=None, description="Latitude coordinate", example=11.0168)
    longitude: Optional[float] = Field(default=None, description="Longitude coordinate", example=76.9558)
    area: float = Field(..., description="Farm area in acres", example=5.0)
    soil_type: str = Field(..., description="Type of soil (e.g., red, black, alluvial)", example="red")
    soil_ph: Optional[float] = Field(default=None, description="pH level of soil", example=6.8)
    water_availability: str = Field(..., description="Water availability level (e.g., low, medium, high)", example="medium")
    budget: float = Field(..., description="Available budget in INR", example=150000.0)
    season: str = Field(..., description="Cropping season (e.g., kharif, rabi, zaid)", example="kharif")
    previous_crop: Optional[str] = Field(default=None, description="Previous crop grown in the field", example="groundnut")


class FarmResponse(BaseModel):
    message: str = Field(..., example="Farm details received successfully")
    farm: FarmInput
