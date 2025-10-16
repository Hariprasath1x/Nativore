"""
Nativore - Tamil Nadu Food Analytics Platform
Main FastAPI application file.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Import database initialization
from database import init_db

# Import routers
from routes import auth, restaurants, analytics, recommendations

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Nativore API",
    description="AI-powered food market analytics platform for Tamil Nadu",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(restaurants.router)
app.include_router(analytics.router)
app.include_router(recommendations.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("🚀 Starting Nativore API...")
    init_db()
    print("✅ Database initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("👋 Shutting down Nativore API...")


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "message": "Welcome to Nativore API",
        "description": "Tamil Nadu Food Market Analytics Platform",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "authentication": "/api/auth",
            "restaurants": "/api/restaurants",
            "analytics": "/api/analytics",
            "recommendations": "/api/recommendations"
        },
        "cities": [
            "Chennai",
            "Coimbatore",
            "Tiruppur",
            "Madurai",
            "Thoothukudi"
        ]
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "Nativore API",
        "version": "1.0.0"
    }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True") == "True"
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug
    )
