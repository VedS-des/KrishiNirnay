from fastapi import APIRouter
from models.farm import FarmInput, FarmResponse

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post("", response_model=FarmResponse, summary="Register or validate farm profile")
def create_farm(farm_data: FarmInput):
    return FarmResponse(
        status="success",
        message="Farm profile registered successfully.",
        data=farm_data
    )
