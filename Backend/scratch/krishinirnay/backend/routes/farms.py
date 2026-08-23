from fastapi import APIRouter
from models.farm import FarmInput, FarmResponse

router = APIRouter(tags=["Farms"])


@router.post("/farms", response_model=FarmResponse, summary="Submit Farm Details")
def submit_farm_details(farm: FarmInput):
    """
    Receives farmer and farm profile, validates input fields,
    and returns a success confirmation with the received data.
    """
    return {
        "message": "Farm details received successfully",
        "farm": farm,
    }
