from fastapi import APIRouter, HTTPException, status
from models.crop import CropDetailResponse, CropPlanResponse
from services.crop_service import get_crop_details, get_crop_plan

router = APIRouter(prefix="/crops", tags=["Crops"])


@router.get("/{crop_name}", response_model=CropDetailResponse, summary="Get crop botanical and soil details")
def read_crop_details(crop_name: str):
    crop = get_crop_details(crop_name)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop '{crop_name}' not found in database. Supported crops: Groundnut, Black Gram, Sesame, Rice, Maize."
        )
    return crop


@router.get("/{crop_name}/plan", response_model=CropPlanResponse, summary="Get crop stage-by-stage cultivation plan")
def read_crop_plan(crop_name: str):
    plan = get_crop_plan(crop_name)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cultivation plan for crop '{crop_name}' not found. Supported crops: Groundnut, Black Gram, Sesame, Rice, Maize."
        )
    return plan
