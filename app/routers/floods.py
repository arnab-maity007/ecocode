"""
Flood events API router.
Provides endpoints for creating and retrieving flood predictions.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db
from ..services.flood_risk import flood_risk_service
from ..services.notification import notification_service

router = APIRouter(
    prefix="/floods",
    tags=["floods"]
)


@router.get("/", response_model=List[schemas.FloodEventResponse])
async def get_flood_events(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records to return"),
    severity: Optional[str] = Query(None, description="Filter by severity (Low, Medium, High, Critical)"),
    db: Session = Depends(get_db)
):
    """
    Get a list of flood events with optional filtering.
    
    **Query Parameters:**
    - skip: Pagination offset (default: 0)
    - limit: Maximum results (default: 100, max: 500)
    - severity: Filter by severity level (optional)
    
    **Returns:**
    List of flood events ordered by most recent first.
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "location_name": "Main Street, Downtown",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "severity": "High",
            "risk_score": 67.5,
            "timestamp": "2025-10-08T10:30:00Z",
            "rainfall_mm": 35.2,
            "elevation_m": 15.5,
            "description": "Heavy rainfall expected"
        }
    ]
    ```
    """
    flood_events = crud.get_flood_events(db, skip=skip, limit=limit, severity=severity)
    return flood_events


@router.get("/{flood_id}", response_model=schemas.FloodEventResponse)
async def get_flood_event(
    flood_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific flood event by ID.
    
    **Parameters:**
    - flood_id: ID of the flood event
    
    **Returns:**
    Single flood event details.
    
    **Errors:**
    - 404: Flood event not found
    """
    flood_event = crud.get_flood_event(db, flood_id)
    if flood_event is None:
        raise HTTPException(status_code=404, detail="Flood event not found")
    return flood_event


@router.post("/", response_model=schemas.FloodEventResponse, status_code=201)
async def create_flood_event(
    flood_event: schemas.FloodEventCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new flood event with automatic risk calculation.
    
    **Request Body:**
    ```json
    {
        "location_name": "Main Street, Downtown",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Intersection near river",
        "rainfall_mm": null,  // Optional: auto-fetched if null
        "elevation_m": null   // Optional: auto-fetched if null
    }
    ```
    
    **Process:**
    1. Fetches real-time rainfall data from OpenWeatherMap
    2. Fetches elevation data from Google Elevation API (or uses mock data)
    3. Calculates risk score (0-100) based on rainfall and elevation
    4. Determines severity level (Low/Medium/High/Critical)
    5. Stores event in database
    
    **Returns:**
    Created flood event with calculated risk data.
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "location_name": "Main Street, Downtown",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "severity": "High",
        "risk_score": 67.5,
        "timestamp": "2025-10-08T10:30:00Z",
        "rainfall_mm": 35.2,
        "elevation_m": 15.5,
        "description": "Intersection near river"
    }
    ```
    """
    # Calculate flood risk using the service
    risk_data = await flood_risk_service.calculate_flood_risk(
        latitude=flood_event.latitude,
        longitude=flood_event.longitude,
        rainfall_override=flood_event.rainfall_mm,
        elevation_override=flood_event.elevation_m
    )
    
    # Create flood event in database
    db_flood_event = crud.create_flood_event(
        db=db,
        flood_event=flood_event,
        risk_score=risk_data["risk_score"],
        severity=risk_data["severity"],
        rainfall_mm=risk_data["rainfall_mm"],
        elevation_m=risk_data["elevation_m"]
    )
    
    # Auto-send notifications if severity is High or Critical
    if risk_data["severity"] in ["High", "Critical"]:
        subscriptions = crud.get_subscriptions_near_location(
            db,
            latitude=flood_event.latitude,
            longitude=flood_event.longitude,
            min_severity=risk_data["severity"]
        )
        
        if subscriptions:
            emails = [sub.email for sub in subscriptions if sub.email]
            phones = [sub.phone for sub in subscriptions if sub.phone]
            
            # Send notifications asynchronously
            await notification_service.send_flood_alert(
                location_name=flood_event.location_name,
                risk_level=risk_data["severity"],
                risk_score=risk_data["risk_score"],
                latitude=flood_event.latitude,
                longitude=flood_event.longitude,
                phone_numbers=phones if phones else None,
                emails=emails if emails else None
            )
    
    return db_flood_event


@router.get("/nearby/", response_model=List[schemas.FloodEventResponse])
async def get_nearby_flood_events(
    latitude: float = Query(..., ge=-90, le=90, description="Center latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Center longitude"),
    radius_km: float = Query(5.0, ge=0.1, le=50, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Get flood events near a specific location.
    
    **Query Parameters:**
    - latitude: Center point latitude
    - longitude: Center point longitude
    - radius_km: Search radius in kilometers (default: 5km, max: 50km)
    
    **Returns:**
    List of flood events within the specified radius.
    
    **Note:** This uses a simplified bounding box search. For production,
    consider using PostGIS for accurate geographic queries.
    """
    flood_events = crud.get_flood_events_by_location(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km
    )
    return flood_events


@router.post("/calculate-risk", response_model=schemas.RiskCalculationResponse)
async def calculate_flood_risk(
    request: schemas.RiskCalculationRequest
):
    """
    Calculate flood risk for a location without saving to database.
    
    **Request Body:**
    ```json
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "location_name": "Main Street"
    }
    ```
    
    **Returns:**
    Risk calculation details including score, severity, and contributing factors.
    
    **Example Response:**
    ```json
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "location_name": "Main Street",
        "risk_score": 67.5,
        "severity": "High",
        "rainfall_mm": 35.2,
        "elevation_m": 15.5,
        "factors": {
            "rainfall_contribution": "High",
            "elevation_contribution": "High risk",
            "explanation": "Risk is elevated due to heavy rainfall and low elevation."
        }
    }
    ```
    """
    # Calculate risk without saving
    risk_data = await flood_risk_service.calculate_flood_risk(
        latitude=request.latitude,
        longitude=request.longitude
    )
    
    return schemas.RiskCalculationResponse(
        latitude=request.latitude,
        longitude=request.longitude,
        location_name=request.location_name,
        risk_score=risk_data["risk_score"],
        severity=risk_data["severity"],
        rainfall_mm=risk_data["rainfall_mm"],
        elevation_m=risk_data["elevation_m"],
        factors=risk_data["factors"]
    )


@router.delete("/{flood_id}", response_model=schemas.MessageResponse)
async def delete_flood_event(
    flood_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a flood event by ID.
    
    **Parameters:**
    - flood_id: ID of the flood event to delete
    
    **Returns:**
    Success message.
    
    **Errors:**
    - 404: Flood event not found
    """
    success = crud.delete_flood_event(db, flood_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flood event not found")
    
    return schemas.MessageResponse(
        message="Flood event deleted successfully",
        detail=f"Deleted flood event with ID {flood_id}"
    )
