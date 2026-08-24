"""
models/profit.py
----------------
Pydantic models for profit calculation input and response.
"""

from pydantic import BaseModel, Field, field_validator


class ProfitInput(BaseModel):
    """Input for POST /profit."""

    crop: str = Field(..., description="Crop name")
    farm_area: float = Field(..., gt=0, description="Farm area in acres")
    expected_yield_per_acre: float = Field(
        ..., gt=0, description="Expected yield in quintals per acre"
    )
    market_price_per_unit: float = Field(
        ..., gt=0, description="Market price per quintal in INR"
    )
    estimated_cost: float = Field(..., ge=0, description="Total cultivation cost in INR")
    transportation_cost: float = Field(..., ge=0, description="Transportation cost in INR")

    @field_validator("estimated_cost", "transportation_cost", "market_price_per_unit")
    @classmethod
    def must_not_be_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Cost and price values must not be negative")
        return v


class ProfitResponse(BaseModel):
    """Detailed profit calculation result."""

    crop: str
    farm_area_acres: float
    expected_production_quintals: float
    gross_revenue_inr: float
    total_cost_inr: float
    estimated_profit_inr: float
    profit_margin_percent: float
    disclaimer: str = (
        "All profit figures are estimates based on user-supplied inputs. "
        "Actual results may vary due to weather, market fluctuations, and other factors."
    )
