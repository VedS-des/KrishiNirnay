# KrishiNirnay API Contract

This document defines the communication format between the frontend,
backend, recommendation engine and other services.

---

## 1. Crop Recommendation

### Endpoint

POST /api/recommend

### Request

```json
{
  "location": "Villupuram, Tamil Nadu",
  "area_acres": 5,
  "soil_type": "red",
  "water_availability": "moderate",
  "budget": 150000,
  "season": "kharif"
}
{
  "recommendations": [
    {
      "crop": "Groundnut",
      "score": 91,
      "expected_yield": 850,
      "estimated_cost": 72000,
      "expected_revenue": 145000,
      "expected_profit": 73000,
      "risk": "Low"
    },
    {
      "crop": "Black Gram",
      "score": 84,
      "expected_yield": 700,
      "estimated_cost": 60000,
      "expected_revenue": 121000,
      "expected_profit": 61000,
      "risk": "Low"
    }
  ]
}
{
  "crop": "Groundnut",
  "duration_days": 110,
  "water_requirement": "Moderate",
  "soil_types": [
    "Red",
    "Sandy Loam"
  ],
  "lifecycle": [
    {
      "day": 0,
      "activity": "Sowing"
    },
    {
      "day": 7,
      "activity": "First irrigation"
    },
    {
      "day": 25,
      "activity": "Fertilizer application"
    },
    {
      "day": 40,
      "activity": "Pest monitoring"
    },
    {
      "day": 110,
      "activity": "Harvest"
    }
  ]
}
{
  "crop": "Groundnut",
  "markets": [
    {
      "name": "Local Mandi",
      "price_per_kg": 60,
      "distance_km": 20,
      "transport_cost": 3000,
      "estimated_net_return": 120000
    },
    {
      "name": "Chennai",
      "price_per_kg": 68,
      "distance_km": 180,
      "transport_cost": 12000,
      "estimated_net_return": 125000
    }
  ]
}
{
  "location": "Villupuram",
  "temperature": 29,
  "rain_probability": 70,
  "humidity": 78,
  "risk": "Medium",
  "alert": "Rain expected"
}
{
  "production_kg": 850,
  "selling_price_per_kg": 60,
  "cultivation_cost": 72000,
  "transport_cost": 12000,
  "other_cost": 5000
}
{
  "gross_revenue": 51000,
  "total_cost": 89000,
  "net_profit": -38000
}
```

---

## 2. Crop Details

### Endpoint

GET /api/crop/{cropName}

### Example

GET /api/crop/Groundnut

### Response

```json
{
  "crop": "Groundnut",
  "duration_days": 110,
  "water_requirement": "Moderate",
  "soil_types": [
    "Red",
    "Sandy Loam"
  ],
  "lifecycle": [
    {
      "day": 0,
      "activity": "Sowing"
    },
    {
      "day": 7,
      "activity": "First irrigation"
    },
    {
      "day": 25,
      "activity": "Fertilizer application"
    },
    {
      "day": 40,
      "activity": "Pest monitoring"
    },
    {
      "day": 110,
      "activity": "Harvest"
    }
  ]
}
```

---

## 3. Market Information

### Endpoint

GET /api/market/{cropName}

### Example

GET /api/market/Groundnut

### Response

```json
{
  "crop": "Groundnut",
  "markets": [
    {
      "name": "Local Mandi",
      "price_per_kg": 60,
      "distance_km": 20,
      "transport_cost": 3000,
      "estimated_net_return": 120000
    },
    {
      "name": "Chennai",
      "price_per_kg": 68,
      "distance_km": 180,
      "transport_cost": 12000,
      "estimated_net_return": 125000
    }
  ]
}
```
---

## 4. Weather Information

### Endpoint

GET /api/weather/{location}

### Example

GET /api/weather/Villupuram

### Response

```json
{
  "location": "Villupuram",
  "temperature": 29,
  "rain_probability": 70,
  "humidity": 78,
  "risk": "Medium",
  "alert": "Rain expected"
}
```
