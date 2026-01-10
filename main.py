"""
Main FastAPI application entry point.
Hyperlocal Urban Flood Forecaster Backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import init_db
from app.config import settings
from app.routers import floods
from app.routers import auth
from app.routers import notifications
from app.routers import map
from app.routers import alerts
from app.routers import route_verdict
from app.routers import chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Handles startup and shutdown tasks.
    """
    # Startup: Initialize database
    print("🚀 Starting Hyperlocal Urban Flood Forecaster API...")
    print(f"📊 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("⚠️  API will run with mock data fallback")
        print("⚠️  To fix: Update DATABASE_URL in .env with valid credentials")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    # Hyperlocal Urban Flood Forecaster API
    
    A comprehensive backend API for predicting street-level flood risks using:
    - 🌧️ Real-time weather data (OpenWeatherMap)
    - 🗺️ Elevation data (Google Elevation API)
    - 🤖 AI-powered risk calculation
    - 📍 Geospatial flood event tracking
    
    ## Features
    - Create and retrieve flood events
    - Calculate real-time flood risk scores
    - Query nearby flood events by location
    - User authentication with JWT (optional)
    
    ## Quick Start
    1. Configure `.env` file with API keys
    2. Set up PostgreSQL database
    3. Run migrations: `alembic upgrade head`
    4. Start server: `uvicorn main:app --reload`
    
    ## Frontend Integration
    All endpoints return JSON responses ready for React/Vue/Angular frontends.
    CORS is enabled for specified origins.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS for frontend integration
# Support both localhost for development and production URLs
cors_origins = settings.cors_origins
# Add common Netlify patterns
if any("localhost" in o for o in cors_origins):
    cors_origins.extend([
        "https://*.netlify.app",
        "https://floodauraaa.netlify.app",
        "https://floodaura.netlify.app",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now (update for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(floods.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(map.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(route_verdict.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/")
async def root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "message": "Hyperlocal Urban Flood Forecaster API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "floods": "/api/v1/floods",
            "calculate_risk": "/api/v1/floods/calculate-risk",
            "auth": "/api/v1/auth"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "flood-forecaster-api",
        "database": "connected"
    }


@app.get("/api/test-connection")
async def test_connection():
    """
    Test endpoint to verify frontend-backend connection.
    """
    return {
        "status": "success",
        "message": "Backend connected successfully!",
        "timestamp": "2026-01-10T00:00:00Z",
        "cors_enabled": True,
        "api_version": "1.0.0"
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 error handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": "The requested resource was not found",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 error handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "message": "Please contact support if this persists"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
