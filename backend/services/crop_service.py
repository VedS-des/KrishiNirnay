"""
services/crop_service.py
------------------------
Business logic for crop information and cultivation plan retrieval.
"""

from typing import List, Optional

from data.crop_data import CROPS, CULTIVATION_PLANS, SUPPORTED_CROPS
from models.crop import CropInfo, CultivationPlan, CultivationStage


def get_all_crops() -> List[str]:
    """Return list of all supported crop names."""
    return SUPPORTED_CROPS


def get_crop_info(crop_name: str) -> Optional[CropInfo]:
    """
    Return detailed information for a crop.
    Returns None if the crop is not in the dataset.
    """
    # Normalise: try exact match first, then case-insensitive
    data = CROPS.get(crop_name)
    if data is None:
        for key in CROPS:
            if key.lower() == crop_name.lower():
                data = CROPS[key]
                break

    if data is None:
        return None

    return CropInfo(
        name=data["name"],
        scientific_name=data["scientific_name"],
        suitable_soils=data["suitable_soils"],
        ideal_ph_min=data["ideal_ph_min"],
        ideal_ph_max=data["ideal_ph_max"],
        water_requirement=data["water_requirement"],
        suitable_seasons=data["suitable_seasons"],
        growing_duration_days=data["growing_duration_days"],
        notes=data["notes"],
    )


def get_cultivation_plan(crop_name: str) -> Optional[CultivationPlan]:
    """
    Return the cultivation plan for a crop.
    Returns None if the crop is not in the dataset.
    """
    # Normalise case
    plan_data = CULTIVATION_PLANS.get(crop_name)
    if plan_data is None:
        for key in CULTIVATION_PLANS:
            if key.lower() == crop_name.lower():
                plan_data = CULTIVATION_PLANS[key]
                crop_name = key
                break

    if plan_data is None:
        return None

    stages = [
        CultivationStage(
            stage=stage["stage"],
            time=stage["time"],
            guidance=stage["guidance"],
        )
        for stage in plan_data
    ]

    return CultivationPlan(crop=crop_name, stages=stages)
