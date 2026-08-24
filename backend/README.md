# KrishiNirnay Backend

**KrishiNirnay** is an AI-powered agricultural decision-support platform.  
This is the **backend API** built with **FastAPI (Python)**.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ (tested on Python 3.14) |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | Pytest + httpx |

---

## Folder Structure

```
backend/
│
├── main.py                        # FastAPI app — entry point
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
│
├── models/                        # Pydantic data models (input/output shapes)
│   ├── farm.py
│   ├── recommendation.py
│   ├── crop.py
│   ├── risk.py
│   ├── profit.py
│   └── market.py
│
├── routes/                        # HTTP route handlers (thin layer)
│   ├── farms.py
│   ├── recommendations.py
│   ├── crops.py
│   ├── risks.py
│   ├── profit.py
│   └── market.py
│
├── services/                      # Business logic (rules, calculations)
│   ├── recommendation_service.py
│   ├── crop_service.py
│   ├── risk_service.py
│   ├── profit_service.py
│   └── market_service.py
│
├── data/                          # Local prototype datasets
│   └── crop_data.py
│
└── tests/                         # Automated tests
    └── test_backend.py
```

---

## Installation

> Make sure you have **Python 3.10+** installed.

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
# Make sure the virtual environment is activated first (see above)
# Then, from inside the backend/ folder:
uvicorn main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

---

## Swagger API Documentation

Once the server is running, open your browser and go to:

**http://127.0.0.1:8000/docs**

You can test every endpoint directly from the browser here.

---

## How to Run Tests

```bash
# From inside the backend/ folder, with .venv activated:
pytest tests/ -v
```

---

## All API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check — confirms backend is running |
| POST | `/farms` | Submit and validate farm details |
| POST | `/recommend` | Get crop recommendations for given farm conditions |
| GET | `/crops` | List all supported crops |
| GET | `/crops/{crop_name}` | Get agronomic info for a specific crop |
| GET | `/crops/{crop_name}/plan` | Get cultivation plan for a specific crop |
| POST | `/risk-assessment` | Get rule-based risk assessment |
| POST | `/profit` | Calculate estimated profit |
| POST | `/market/compare` | Compare market options by profitability |

---

## Sample Requests

### POST /farms
```json
{
    "location": "Tamil Nadu",
    "latitude": 11.0168,
    "longitude": 76.9558,
    "area": 5,
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "budget": 150000,
    "season": "kharif",
    "previous_crop": "groundnut"
}
```

### POST /recommend
```json
{
    "location": "Tamil Nadu",
    "area": 5,
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "budget": 150000,
    "season": "kharif"
}
```

### POST /risk-assessment
```json
{
    "crop": "Groundnut",
    "location": "Tamil Nadu",
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "season": "kharif"
}
```

### POST /profit
```json
{
    "crop": "Groundnut",
    "farm_area": 5,
    "expected_yield_per_acre": 8.5,
    "market_price_per_unit": 5500,
    "estimated_cost": 72000,
    "transportation_cost": 5000
}
```

### POST /market/compare
```json
{
    "crop": "Groundnut",
    "quantity": 42.5,
    "production_cost": 72000,
    "markets": [
        {
            "market_name": "Local Market",
            "price_per_unit": 5000,
            "transportation_cost": 2000
        },
        {
            "market_name": "Regional Market",
            "price_per_unit": 5500,
            "transportation_cost": 6000
        }
    ]
}
```

---

## Architecture

```
Farmer
   ↓
Frontend (another team member)
   ↓
FastAPI API (main.py)
   ↓
Route (routes/) — handles HTTP request/response
   ↓
Pydantic Model (models/) — validates input/output
   ↓
Service (services/) — contains all business logic
   ↓
Rule Engine / Local Data  ←→  (Future: ML Model / Weather API / Market API)
   ↓
JSON Response
   ↓
Frontend
```

### Layer Responsibilities

| Layer | Responsibility |
|-------|---------------|
| `main.py` | App setup, CORS, router registration |
| `routes/` | HTTP request/response handling only |
| `models/` | Input validation + output structure (Pydantic) |
| `services/` | All business logic and calculations |
| `data/` | Local prototype crop data |

---

## ⚠️ Prototype / Demo Data Disclaimer

This project uses **prototype/demo data** in the following areas:

- **Crop recommendations:** Generated by a rule-based engine, NOT a trained AI/ML model.
- **Yield estimates:** Approximate demo values sourced from general agricultural references.
- **Cost and revenue estimates:** Prototype figures for demonstration only.
- **Risk assessment:** Rule-based heuristics — NOT real-time weather or sensor data.
- **Market prices:** No live market data is fetched. User-supplied or prototype values only.

---

## Future Integration Points

| Feature | Current State | Future Plan |
|---------|--------------|-------------|
| Crop recommendation | Rule-based prototype | Replace `services/recommendation_service.py` with ML model |
| Risk assessment | Rule-based heuristics | Add real-time weather API in `services/risk_service.py` |
| Market prices | User-supplied | Integrate Agmarknet / eNAM API in `services/market_service.py` |

---

## Frontend Integration Notes

- **CORS** is configured to allow all origins during development (`allow_origins=["*"]`).
- All endpoints return **JSON**.
- Error responses use standard HTTP status codes with a `detail` field.
- Use **http://127.0.0.1:8000/docs** to explore and test all endpoints.
- Validation errors return **HTTP 422** with a detailed list of field errors.

---

## Supported Crops (Prototype Dataset)

| Crop | Season | Water Requirement |
|------|--------|------------------|
| Groundnut | Kharif, Rabi | Medium |
| Black Gram | Kharif, Rabi | Medium |
| Sesame | Kharif | Low |
| Rice | Kharif | High |
| Maize | Kharif, Rabi | Medium |

---

*Built by Member 3 — KrishiNirnay Team*
