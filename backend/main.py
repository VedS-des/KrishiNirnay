"""
main.py
-------
KrishiNirnay Backend — FastAPI Application Entry Point

Run the server with:
    uvicorn main:app --reload

Swagger docs available at:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import farms, recommendations, crops, risks, profit, market

# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------

app = FastAPI(
    title="KrishiNirnay API",
    description=(
        "KrishiNirnay is an AI-powered agricultural decision-support platform. "
        "This backend provides crop recommendations, cultivation plans, "
        "risk assessments, profit calculations, and market comparisons. "
        "\n\n"
        "**Note:** The recommendation engine is currently a rule-based prototype. "
        "It is designed so a trained AI/ML model can replace it in a future sprint."
    ),
    version="1.0.0",
    contact={
        "name": "KrishiNirnay Team",
    },
    license_info={
        "name": "MIT",
    },
)

# ---------------------------------------------------------------------------
# CORS middleware
# Allow all origins during development so the frontend team can connect easily.
# Restrict origins before deploying to production.
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Frontend integration: replace with specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(farms.router, tags=["Farm"])
app.include_router(recommendations.router, tags=["Recommendation"])
app.include_router(crops.router, tags=["Crops"])
app.include_router(risks.router, tags=["Risk Assessment"])
app.include_router(profit.router, tags=["Profit"])
app.include_router(market.router, tags=["Market"])


# ---------------------------------------------------------------------------
# Root health-check endpoint
# ---------------------------------------------------------------------------

@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns a simple status message to confirm the backend is running.",
)
def root():
    """Health check — confirms the API is live."""
    return {"message": "KrishiNirnay Backend is running"}
