"""
routes/farms.py
---------------
Route: POST /farms
Accepts and validates farm data.
"""

from fastapi import APIRouter
from models.farm import FarmInput, FarmResponse

router = APIRouter()


@router.post(
    "/farms",
    response_model=FarmResponse,
    status_code=201,
    summary="Register Farm Data",
    description=(
        "Submit farm details such as location, soil type, pH, water availability, "
        "budget, and season. Returns the validated farm data."
    ),
)
def register_farm(farm: FarmInput) -> FarmResponse:
    """
    Accept and validate farm information.

    The frontend can call this endpoint first to ensure data is valid,
    then call POST /recommend with the same data to get crop recommendations.
    """
    return FarmResponse(
        message="Farm data received and validated successfully.",
        farm_data=farm,
    )
