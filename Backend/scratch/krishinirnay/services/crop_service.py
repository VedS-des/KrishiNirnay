from typing import Dict, Optional
from models.crop import CropDetailResponse, CropPlanResponse, CropPlanStage

CROPS_DATABASE: Dict[str, Dict] = {
    "groundnut": {
        "crop": "Groundnut",
        "scientific_name": "Arachis hypogaea",
        "suitable_soil": ["Red Sandy Loam", "Sandy Loam", "Well-drained Loam"],
        "ideal_ph_range": "6.0 - 7.5",
        "water_requirement": "Low to Medium (500 - 700 mm)",
        "suitable_seasons": ["Kharif", "Rabi", "Summer"],
        "growing_duration_days": 120,
        "plan_stages": [
            {
                "stage": "Land Preparation",
                "time": "Before planting (Day -15 to Day -1)",
                "guidance": "Plough field 2-3 times to create a fine tilth. Incorporate well-decomposed FYM/compost and ensure proper drainage."
            },
            {
                "stage": "Planting & Sowing",
                "time": "Day 0",
                "guidance": "Treat seeds with Rhizobium culture and Trichoderma. Sow at depth of 5 cm with row spacing of 30 cm and plant spacing of 10 cm."
            },
            {
                "stage": "Vegetative Growth",
                "time": "Day 1 to 40",
                "guidance": "Maintain weed-free conditions with light hoeing. Apply gypsum at 30-35 days to boost calcium availability for pod development."
            },
            {
                "stage": "Flowering & Pegging",
                "time": "Day 40 to 70",
                "guidance": "Critical moisture stage. Ensure adequate soil moisture for peg penetration; avoid disturbing soil during pegging."
            },
            {
                "stage": "Pod Development & Maturity",
                "time": "Day 70 to 110",
                "guidance": "Monitor for leaf spot (Tikka) and rust. Withhold irrigation 7-10 days before harvesting."
            },
            {
                "stage": "Harvest",
                "time": "Approximately Day 120",
                "guidance": "Harvest when leaves turn yellow and inner shell turns brownish-black. Dry pods thoroughly to <8% moisture before storage."
            }
        ]
    },
    "black gram": {
        "crop": "Black Gram",
        "scientific_name": "Vigna mungo",
        "suitable_soil": ["Loam", "Clay Loam", "Black Cotton Soil"],
        "ideal_ph_range": "6.5 - 7.5",
        "water_requirement": "Low (350 - 450 mm)",
        "suitable_seasons": ["Kharif", "Rabi", "Summer"],
        "growing_duration_days": 80,
        "plan_stages": [
            {
                "stage": "Land Preparation",
                "time": "Before planting",
                "guidance": "Prepare a weed-free seedbed with one deep ploughing followed by two harrowings."
            },
            {
                "stage": "Planting",
                "time": "Day 0",
                "guidance": "Treat seeds with Rhizobium and Fungicide. Sow in rows 30 cm apart with 10 cm plant spacing."
            },
            {
                "stage": "Vegetative Growth",
                "time": "Day 1 to 30",
                "guidance": "Perform one weeding around 20 days after sowing. Maintain soil aeration."
            },
            {
                "stage": "Flowering & Pod Formation",
                "time": "Day 30 to 60",
                "guidance": "Provide light irrigation at flowering and pod filling if dry spell occurs."
            },
            {
                "stage": "Harvest",
                "time": "Approximately Day 80",
                "guidance": "Harvest when 80-85% of pods turn black. Thresh, clean, and dry seeds."
            }
        ]
    },
    "sesame": {
        "crop": "Sesame",
        "scientific_name": "Sesamum indicum",
        "suitable_soil": ["Sandy Loam", "Light Loam", "Alluvial"],
        "ideal_ph_range": "5.5 - 8.0",
        "water_requirement": "Low (300 - 400 mm)",
        "suitable_seasons": ["Kharif", "Summer", "Zaid"],
        "growing_duration_days": 90,
        "plan_stages": [
            {
                "stage": "Land Preparation",
                "time": "Before planting",
                "guidance": "Fine seedbed is required due to small seed size. Level land carefully to avoid waterlogging."
            },
            {
                "stage": "Planting",
                "time": "Day 0",
                "guidance": "Mix seed with fine sand for uniform broadcasting or drill in lines 30 cm apart."
            },
            {
                "stage": "Vegetative Growth & Thinning",
                "time": "Day 1 to 35",
                "guidance": "Thin seedlings at 15-20 days to maintain 15 cm spacing between plants. Keep weed-free."
            },
            {
                "stage": "Flowering & Capsule Development",
                "time": "Day 35 to 70",
                "guidance": "Protect from phyllody disease and caterpillar pests. Ensure good drainage."
            },
            {
                "stage": "Harvest",
                "time": "Approximately Day 90",
                "guidance": "Harvest when leaves turn yellow and lower capsules turn yellowish-brown before bursting."
            }
        ]
    },
    "rice": {
        "crop": "Rice",
        "scientific_name": "Oryza sativa",
        "suitable_soil": ["Clay", "Clay Loam", "Alluvial", "Heavy Silt Loam"],
        "ideal_ph_range": "5.5 - 7.5",
        "water_requirement": "High (1200 - 1500 mm)",
        "suitable_seasons": ["Kharif", "Rabi", "Monsoon"],
        "growing_duration_days": 135,
        "plan_stages": [
            {
                "stage": "Nursery & Land Preparation",
                "time": "Before planting (Day -25 to Day 0)",
                "guidance": "Raise healthy seedlings in nursery. Puddle the main field thoroughly and level evenly."
            },
            {
                "stage": "Transplanting",
                "time": "Day 0 (20-25 day old seedlings)",
                "guidance": "Transplant 2-3 seedlings per hill at 2-3 cm depth with 20x15 cm spacing."
            },
            {
                "stage": "Tillering & Vegetative",
                "time": "Day 1 to 50",
                "guidance": "Apply top-dressing Nitrogen. Maintain shallow standing water (2-3 cm)."
            },
            {
                "stage": "Panicle Initiation & Flowering",
                "time": "Day 50 to 95",
                "guidance": "Maintain continuous 5 cm water layer. Monitor for stem borer and blast disease."
            },
            {
                "stage": "Grain Filling & Ripening",
                "time": "Day 95 to 125",
                "guidance": "Drain water 10-14 days before harvest to facilitate uniform ripening."
            },
            {
                "stage": "Harvest",
                "time": "Approximately Day 135",
                "guidance": "Harvest when 85% of grains turn golden yellow and grain moisture is around 20%."
            }
        ]
    },
    "maize": {
        "crop": "Maize",
        "scientific_name": "Zea mays",
        "suitable_soil": ["Loam", "Sandy Loam", "Alluvial", "Well-drained Red Soil"],
        "ideal_ph_range": "5.8 - 7.5",
        "water_requirement": "Medium (500 - 800 mm)",
        "suitable_seasons": ["Kharif", "Rabi", "Summer", "Zaid"],
        "growing_duration_days": 105,
        "plan_stages": [
            {
                "stage": "Land Preparation",
                "time": "Before planting",
                "guidance": "Deep ploughing followed by harrowing. Form ridges and furrows for irrigation."
            },
            {
                "stage": "Planting & Sowing",
                "time": "Day 0",
                "guidance": "Sow certified hybrid seeds at 60 cm row spacing and 20 cm plant spacing at 4-5 cm depth."
            },
            {
                "stage": "Vegetative Growth & Knee-High Stage",
                "time": "Day 1 to 40",
                "guidance": "Apply first top-dressing of nitrogen at knee-high stage (30 days). Earthing up to prevent lodging."
            },
            {
                "stage": "Tasseling & Silking",
                "time": "Day 40 to 70",
                "guidance": "Critical water requirement phase. Avoid moisture stress; monitor for Fall Armyworm."
            },
            {
                "stage": "Grain Formation & Maturity",
                "time": "Day 70 to 95",
                "guidance": "Apply final light irrigation if needed. Monitor cob maturity."
            },
            {
                "stage": "Harvest",
                "time": "Approximately Day 105",
                "guidance": "Harvest when husk leaves turn dry and paper-like with a black layer visible at seed base."
            }
        ]
    }
}


def get_crop_details(crop_name: str) -> Optional[CropDetailResponse]:
    key = crop_name.strip().lower()
    data = CROPS_DATABASE.get(key)
    if not data:
        return None
    return CropDetailResponse(
        crop=data["crop"],
        scientific_name=data["scientific_name"],
        suitable_soil=data["suitable_soil"],
        ideal_ph_range=data["ideal_ph_range"],
        water_requirement=data["water_requirement"],
        suitable_seasons=data["suitable_seasons"],
        growing_duration_days=data["growing_duration_days"]
    )


def get_crop_plan(crop_name: str) -> Optional[CropPlanResponse]:
    key = crop_name.strip().lower()
    data = CROPS_DATABASE.get(key)
    if not data:
        return None
    
    stages = [CropPlanStage(**stage) for stage in data["plan_stages"]]
    return CropPlanResponse(
        crop=data["crop"],
        disclaimer="Prototype/demo guidance only. Not intended as certified agronomic advice.",
        stages=stages
    )
