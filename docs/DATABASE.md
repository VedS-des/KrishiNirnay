# KrishiNirnay Database Design

## 1. FARMS

Stores information about the farmer's farm.

| Field | Data Type | Description |
|---|---|---|
| id | Integer | Unique farm ID |
| location | String | Farm location |
| latitude | Decimal | GPS latitude |
| longitude | Decimal | GPS longitude |
| area_acres | Decimal | Total farm area in acres |
| soil_type | String | Type of soil |
| water_availability | String | Low / Moderate / High |
| budget | Decimal | Available farming budget in ₹ |
| season | String | Farming season |

---

## 2. CROPS

Stores basic information about available crops.

| Field | Data Type | Description |
|---|---|---|
| id | Integer | Unique crop ID |
| name | String | Crop name |
| duration_days | Integer | Approximate crop duration |
| water_requirement | String | Low / Moderate / High |

---

## 3. CROP_PLANS

Stores the crop growth lifecycle and activities.

| Field | Data Type | Description |
|---|---|---|
| id | Integer | Unique plan ID |
| crop_id | Integer | ID of the related crop |
| day | Integer | Day of the crop lifecycle |
| activity | String | Activity to be performed |

Example:

| id | crop_id | day | activity |
|---:|---:|---:|---|
| 1 | 1 | 0 | Sowing |
| 2 | 1 | 25 | Crop management |
| 3 | 1 | 40 | Pest monitoring |
| 4 | 1 | 110 | Harvest |

---

## 4. MARKETS

Stores information about available agricultural markets.

| Field | Data Type | Description |
|---|---|---|
| id | Integer | Unique market ID |
| name | String | Market name |
| location | String | Market location |

---

## 5. MARKET_PRICES

Stores crop prices at different markets.

| Field | Data Type | Description |
|---|---|---|
| id | Integer | Unique price record ID |
| crop_id | Integer | ID of the crop |
| market_id | Integer | ID of the market |
| price_per_kg | Decimal | Current price in ₹/kg |
| date | Date | Date of the recorded price |

---

## 6. DATA TYPES

### Integer
Used for:
- IDs
- Number of days

### Decimal
Used for:
- Farm area
- Budget
- Prices
- Latitude
- Longitude

### String
Used for:
- Names
- Locations
- Soil types
- Water availability
- Seasons
- Activities

### Date
Used for:
- Market price date

---

## 7. RELATIONSHIPS

### CROPS → CROP_PLANS

One crop can have multiple crop lifecycle activities.

```text
CROPS
  |
  | crop_id
  ↓
CROP_PLANS

