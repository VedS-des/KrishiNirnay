"""
routes/crops.py
---------------
Routes:
    GET /crops                      — list all supported crops
    GET /crops/{crop_name}          — get information about a specific crop
    GET /crops/{crop_name}/plan     — get cultivation plan for a specific crop
"""

from fastapi import APIRouter, HTTPException
from typing import List

from models.crop import CropInfo, CultivationPlan
from services.crop_service import get_all_crops, get_crop_info, get_cultivation_plan

router = APIRouter()


@router.get(
    "/crops",
    response_model=List[str],
    summary="List All Supported Crops",
    description="Returns the names of all crops supported by the prototype dataset.",
)
def list_crops() -> List[str]:
    """Return all supported crop names."""
    return get_all_crops()


@router.get(
    "/crops/{crop_name}",
    response_model=CropInfo,
    summary="Get Crop Information",
    description=(
        "Returns agronomic details for the specified crop including soil requirements, "
        "pH range, water needs, growing duration, and notes. "
        "Returns 404 if the crop is not in the dataset."
    ),
)
def get_crop(crop_name: str) -> CropInfo:
    """Return detailed information for a single crop."""
    info = get_crop_info(crop_name)
    if info is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Crop '{crop_name}' is not in the prototype dataset. "
                "Use GET /crops to see supported crops."
            ),
        )
    return info


@router.get(
    "/crops/{crop_name}/plan",
    response_model=CultivationPlan,
    summary="Get Cultivation Plan",
    description=(
        "Returns a stage-by-stage cultivation lifecycle plan for the specified crop. "
        "Returns 404 if the crop is not in the dataset."
    ),
)
def get_plan(crop_name: str) -> CultivationPlan:
    """Return the cultivation plan for a single crop."""
    plan = get_cultivation_plan(crop_name)
    if plan is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No cultivation plan found for '{crop_name}'. "
                "Use GET /crops to see supported crops."
            ),
        )
    return plan
