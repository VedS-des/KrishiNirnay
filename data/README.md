# KrishiNirnay Data

## Crop Dataset

crops.csv contains the standardized crop attributes used by the MVP recommendation and crop-details flow.

Fields:

- crop
- soil_type
- water_requirement
- season
- duration_days
- estimated_cost
- expected_yield

## Crop Lifecycle

crop_plans.csv contains lifecycle activities for each crop.

Fields:

- crop
- day
- activity

Each crop has lifecycle records used by the Crop Details API.

## Market Data

market_data.csv contains market records currently available for the MVP.

Fields:

- crop
- name
- price_per_kg
- distance_km
- transport_cost

Only entered market prices should be treated as available data. Do not invent missing market prices.

## Data Sources

data_sources.csv records the source and methodology used for crop attributes.

It is intended to provide provenance for the dataset and distinguish verified values from values that were intentionally not populated.

## Integration

The datasets are consumed by the backend/API layer.

- crops.csv -> crop recommendation and crop details
- crop_plans.csv -> crop lifecycle
- market_data.csv -> market information
- data_sources.csv -> source/provenance reference
