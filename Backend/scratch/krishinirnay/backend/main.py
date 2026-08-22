from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.farms import router as farms_router
from routes.recommendations import router as recommendations_router

app = FastAPI(
    title="KrishiNirnay Backend API",
    description="AI-powered agricultural decision-support platform backend API",
    version="1.0.0",
)

# Enable CORS so Frontend team can connect without CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"], summary="Backend Health Check")
def health_check():
    """
    Health check endpoint to verify that the backend server is running.
    """
    return {"message": "KrishiNirnay Backend is running!"}


# Register route modules
app.include_router(farms_router)
app.include_router(recommendations_router)
