"""
data/crop_data.py
-----------------
Local prototype dataset for KrishiNirnay.

DISCLAIMER: All yield figures, costs, and prices are approximate demo values
intended for prototype/demo purposes only. They do not represent real-time
or officially published agricultural data.
"""

# ---------------------------------------------------------------------------
# Crop catalogue
# Each entry holds agronomic info used by multiple services.
# ---------------------------------------------------------------------------

CROPS = {
    "Groundnut": {
        "name": "Groundnut",
        "scientific_name": "Arachis hypogaea",
        "suitable_soils": ["red", "sandy loam", "loamy"],
        "ideal_ph_min": 5.5,
        "ideal_ph_max": 7.0,
        "water_requirement": "medium",          # low / medium / high
        "suitable_seasons": ["kharif", "rabi"],
        "growing_duration_days": 110,
        "notes": (
            "Groundnut thrives in light-textured, well-drained soils. "
            "It is a legume that fixes atmospheric nitrogen, improving soil fertility."
        ),
        # Prototype economics (per acre, in INR)
        "estimated_yield_per_acre_quintals": 8.5,
        "estimated_cost_per_acre_inr": 14400,
        "estimated_market_price_per_quintal_inr": 5500,
        "risk_level": "Low",
    },
    "Black Gram": {
        "name": "Black Gram",
        "scientific_name": "Vigna mungo",
        "suitable_soils": ["black", "loamy", "clay loam"],
        "ideal_ph_min": 6.0,
        "ideal_ph_max": 7.5,
        "water_requirement": "medium",
        "suitable_seasons": ["kharif", "rabi"],
        "growing_duration_days": 75,
        "notes": (
            "Black gram is a short-duration pulse crop that enriches soil nitrogen. "
            "It performs well in moderate-rainfall areas."
        ),
        "estimated_yield_per_acre_quintals": 5.0,
        "estimated_cost_per_acre_inr": 10000,
        "estimated_market_price_per_quintal_inr": 6000,
        "risk_level": "Low",
    },
    "Sesame": {
        "name": "Sesame",
        "scientific_name": "Sesamum indicum",
        "suitable_soils": ["red", "sandy loam", "well-drained black"],
        "ideal_ph_min": 5.5,
        "ideal_ph_max": 8.0,
        "water_requirement": "low",
        "suitable_seasons": ["kharif"],
        "growing_duration_days": 90,
        "notes": (
            "Sesame is a drought-tolerant oilseed crop suited to well-drained soils. "
            "It requires minimal irrigation and is profitable at small scale."
        ),
        "estimated_yield_per_acre_quintals": 3.5,
        "estimated_cost_per_acre_inr": 8000,
        "estimated_market_price_per_quintal_inr": 9000,
        "risk_level": "Medium",
    },
    "Rice": {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "suitable_soils": ["clay", "clay loam", "black"],
        "ideal_ph_min": 5.5,
        "ideal_ph_max": 7.0,
        "water_requirement": "high",
        "suitable_seasons": ["kharif"],
        "growing_duration_days": 130,
        "notes": (
            "Rice requires standing water during early growth stages. "
            "Clay soils with good water-retention capacity are ideal."
        ),
        "estimated_yield_per_acre_quintals": 20.0,
        "estimated_cost_per_acre_inr": 20000,
        "estimated_market_price_per_quintal_inr": 2000,
        "risk_level": "Medium",
    },
    "Maize": {
        "name": "Maize",
        "scientific_name": "Zea mays",
        "suitable_soils": ["loamy", "sandy loam", "red"],
        "ideal_ph_min": 5.8,
        "ideal_ph_max": 7.5,
        "water_requirement": "medium",
        "suitable_seasons": ["kharif", "rabi"],
        "growing_duration_days": 95,
        "notes": (
            "Maize is a versatile cereal crop with high yield potential. "
            "It needs well-drained soils and adequate moisture during tasselling."
        ),
        "estimated_yield_per_acre_quintals": 25.0,
        "estimated_cost_per_acre_inr": 16000,
        "estimated_market_price_per_quintal_inr": 1800,
        "risk_level": "Low",
    },
}

# ---------------------------------------------------------------------------
# Cultivation plans
# Each plan lists lifecycle stages with approximate timing and guidance.
# DISCLAIMER: Guidance is prototype/demo data.
# ---------------------------------------------------------------------------

CULTIVATION_PLANS = {
    "Groundnut": [
        {
            "stage": "Land Preparation",
            "time": "Week 1",
            "guidance": (
                "Deep plough 2–3 times to loosen soil. "
                "Apply 10–15 tonnes of farmyard manure per hectare. "
                "Level the field to ensure good drainage."
            ),
        },
        {
            "stage": "Planting",
            "time": "Week 1–2",
            "guidance": (
                "Sow seeds 5 cm deep with 30×10 cm spacing. "
                "Use 80–100 kg seed per hectare. "
                "Treat seeds with Rhizobium culture for nitrogen fixation."
            ),
        },
        {
            "stage": "Early Growth",
            "time": "Week 2–4",
            "guidance": (
                "Apply first irrigation 3 days after sowing. "
                "Thin seedlings to maintain proper spacing. "
                "Apply starter fertiliser (N:P:K as recommended locally)."
            ),
        },
        {
            "stage": "Vegetative Stage",
            "time": "Week 4–7",
            "guidance": (
                "Carry out first weeding at 20 DAS and second at 40 DAS. "
                "Apply gypsum at 500 kg/ha before pegging for calcium supply. "
                "Monitor for leaf-eating caterpillars."
            ),
        },
        {
            "stage": "Flowering & Pegging",
            "time": "Week 6–9",
            "guidance": (
                "Irrigate regularly — this is a critical moisture-sensitive stage. "
                "Avoid water stress. Earth up soil around plants to help peg penetration."
            ),
        },
        {
            "stage": "Pod Development",
            "time": "Week 9–14",
            "guidance": (
                "Maintain soil moisture but avoid waterlogging. "
                "Check for leaf-spot and tikka disease; apply fungicide if needed. "
                "Reduce irrigation frequency two weeks before harvest."
            ),
        },
        {
            "stage": "Harvest",
            "time": "Week 14–16 (~110 days)",
            "guidance": (
                "Harvest when leaves turn yellow and pods show dark veins inside. "
                "Uproot plants carefully to avoid pod loss. "
                "Dry pods in sun for 3–4 days before threshing."
            ),
        },
    ],
    "Black Gram": [
        {
            "stage": "Land Preparation",
            "time": "Week 1",
            "guidance": "Plough field 2 times and apply compost. Ensure good drainage.",
        },
        {
            "stage": "Planting",
            "time": "Week 1",
            "guidance": (
                "Sow seeds at 30×10 cm spacing, 3–4 cm deep. "
                "Use 12–15 kg seed per acre. Seed treat with Rhizobium culture."
            ),
        },
        {
            "stage": "Early Growth",
            "time": "Week 2–3",
            "guidance": "Irrigate if rainfall is insufficient. Thin excess seedlings.",
        },
        {
            "stage": "Vegetative Stage",
            "time": "Week 3–5",
            "guidance": "Weed at 20 DAS. Apply phosphate fertiliser for root nodule formation.",
        },
        {
            "stage": "Flowering",
            "time": "Week 5–7",
            "guidance": "Irrigate at flowering stage. Spray insecticide if pod borers appear.",
        },
        {
            "stage": "Pod Maturity",
            "time": "Week 8–10",
            "guidance": "Pods turn black when mature. Reduce watering. Watch for premature shattering.",
        },
        {
            "stage": "Harvest",
            "time": "Week 10–11 (~75 days)",
            "guidance": "Harvest pods in 2–3 pickings as they mature. Dry and thresh.",
        },
    ],
    "Sesame": [
        {
            "stage": "Land Preparation",
            "time": "Week 1",
            "guidance": "Plough thoroughly. Sesame needs a fine, firm seedbed. Apply compost.",
        },
        {
            "stage": "Planting",
            "time": "Week 1",
            "guidance": (
                "Broadcast or drill seeds at 5 kg/ha. Mix seeds with sand for even distribution. "
                "Do not bury seeds too deep — 1–2 cm is sufficient."
            ),
        },
        {
            "stage": "Early Growth",
            "time": "Week 2–3",
            "guidance": "Thin to 10–15 cm between plants. Apply one light irrigation if dry.",
        },
        {
            "stage": "Vegetative Stage",
            "time": "Week 3–6",
            "guidance": "Weed at 20 DAS. Apply nitrogen fertiliser. Monitor for phyllody disease.",
        },
        {
            "stage": "Flowering",
            "time": "Week 6–8",
            "guidance": "Avoid waterlogging during flowering. One irrigation at this stage is beneficial.",
        },
        {
            "stage": "Capsule Development",
            "time": "Week 8–11",
            "guidance": "Reduce irrigation. Capsules develop from bottom up. Avoid lodging.",
        },
        {
            "stage": "Harvest",
            "time": "Week 11–13 (~90 days)",
            "guidance": "Harvest when lower leaves yellow and lowest capsules begin to crack. Bundle and dry upright.",
        },
    ],
    "Rice": [
        {
            "stage": "Nursery & Land Preparation",
            "time": "Week 1–3",
            "guidance": (
                "Prepare nursery bed. Sow pre-germinated seeds. "
                "Plough and puddled main field. Maintain 5 cm standing water."
            ),
        },
        {
            "stage": "Transplanting",
            "time": "Week 3–4",
            "guidance": "Transplant 21-day seedlings in rows of 20×15 cm. 2–3 seedlings per hill.",
        },
        {
            "stage": "Early Tillering",
            "time": "Week 4–6",
            "guidance": "Apply basal fertiliser (NPK). Maintain 2–5 cm water level. Weed at 20 DAS.",
        },
        {
            "stage": "Active Tillering",
            "time": "Week 6–8",
            "guidance": "Apply nitrogen top-dressing. Control leaf folder and blast disease.",
        },
        {
            "stage": "Panicle Initiation",
            "time": "Week 8–10",
            "guidance": "Critical stage — ensure adequate water. Apply potassium fertiliser.",
        },
        {
            "stage": "Flowering & Grain Filling",
            "time": "Week 10–14",
            "guidance": "Maintain water level. Avoid any moisture stress. Monitor for neck blast.",
        },
        {
            "stage": "Harvest",
            "time": "Week 17–19 (~130 days)",
            "guidance": "Harvest when 80% grains turn golden yellow. Drain field 7–10 days before harvest.",
        },
    ],
    "Maize": [
        {
            "stage": "Land Preparation",
            "time": "Week 1",
            "guidance": "Deep plough once and harrow twice. Apply 8–10 tonnes FYM per hectare.",
        },
        {
            "stage": "Planting",
            "time": "Week 1",
            "guidance": (
                "Sow seeds 3–5 cm deep at 60×25 cm spacing. "
                "Use 8–10 kg seed per acre. Treat with fungicide."
            ),
        },
        {
            "stage": "Early Growth",
            "time": "Week 2–4",
            "guidance": "First irrigation at knee-high stage. Apply starter nitrogen dose.",
        },
        {
            "stage": "Vegetative Stage",
            "time": "Week 4–7",
            "guidance": "Weed at 20 and 40 DAS. Apply nitrogen top-dressing at 30 DAS.",
        },
        {
            "stage": "Tasselling & Silking",
            "time": "Week 7–9",
            "guidance": (
                "Critical stage — ensure adequate moisture. "
                "Pollination failure due to drought here causes yield loss."
            ),
        },
        {
            "stage": "Grain Filling",
            "time": "Week 9–12",
            "guidance": "Maintain soil moisture. Apply potassium if not applied earlier. Monitor for stem borer.",
        },
        {
            "stage": "Harvest",
            "time": "Week 13–14 (~95 days)",
            "guidance": "Harvest when husks turn brown and grain moisture is ~20%. Dry cobs to 12% moisture.",
        },
    ],
}

# List of all supported crop names (used for validation)
SUPPORTED_CROPS = list(CROPS.keys())
