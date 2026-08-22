from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import farms_router, recommendations_router, crops_router

app = FastAPI(
    title="KrishiNirnay Backend API",
    description="AI-powered Agricultural Decision-Support System Backend (Day 2 prototype)",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farms_router)
app.include_router(recommendations_router)
app.include_router(crops_router)


@app.get("/", summary="System Health & API Overview")
def root():
    return {
        "system": "KrishiNirnay Backend API",
        "version": "0.2.0",
        "status": "online",
        "message": "Welcome to KrishiNirnay agricultural decision-support API.",
        "documentation": "/docs",
        "endpoints": {
            "GET /": "Root status overview",
            "POST /farms": "Register farm profile",
            "POST /recommend": "Get crop suitability recommendations",
            "GET /crops/{crop_name}": "Get crop agronomic details",
            "GET /crops/{crop_name}/plan": "Get cultivation plan stages"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
