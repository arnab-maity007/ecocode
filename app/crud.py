"""
CRUD operations for database models.
Provides functions for Create, Read, Update, Delete operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from . import models, schemas
from datetime import datetime


# Flood Event CRUD Operations

def create_flood_event(
    db: Session,
    flood_event: schemas.FloodEventCreate,
    risk_score: float,
    severity: str,
    rainfall_mm: float,
    elevation_m: float
) -> models.FloodEvent:
    """
    Create a new flood event in the database.
    
    Args:
        db: Database session
        flood_event: Flood event data from request
        risk_score: Calculated risk score (0-100)
        severity: Calculated severity level
        rainfall_mm: Rainfall amount in mm
        elevation_m: Elevation in meters
    
    Returns:
        Created FloodEvent model instance
    """
    db_flood_event = models.FloodEvent(
        location_name=flood_event.location_name,
        latitude=flood_event.latitude,
        longitude=flood_event.longitude,
        severity=severity,
        risk_score=risk_score,
        rainfall_mm=rainfall_mm,
        elevation_m=elevation_m,
        description=flood_event.description,
        timestamp=datetime.utcnow()
    )
    db.add(db_flood_event)
    db.commit()
    db.refresh(db_flood_event)
    return db_flood_event


def get_flood_event(db: Session, flood_id: int) -> Optional[models.FloodEvent]:
    """
    Get a single flood event by ID.
    
    Args:
        db: Database session
        flood_id: ID of the flood event
    
    Returns:
        FloodEvent model instance or None if not found
    """
    return db.query(models.FloodEvent).filter(models.FloodEvent.id == flood_id).first()


def get_flood_events(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None
) -> List[models.FloodEvent]:
    """
    Get a list of flood events with optional filtering.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        severity: Optional filter by severity level
    
    Returns:
        List of FloodEvent model instances
    """
    query = db.query(models.FloodEvent)
    
    # Filter by severity if provided
    if severity:
        query = query.filter(models.FloodEvent.severity == severity)
    
    # Order by most recent first
    query = query.order_by(desc(models.FloodEvent.timestamp))
    
    return query.offset(skip).limit(limit).all()


def get_flood_events_by_location(
    db: Session,
    latitude: float,
    longitude: float,
    radius_km: float = 5.0
) -> List[models.FloodEvent]:
    """
    Get flood events near a specific location (simplified version).
    For production, use PostGIS for proper geographic queries.
    
    Args:
        db: Database session
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Radius in kilometers
    
    Returns:
        List of FloodEvent model instances
    """
    # Simplified bounding box calculation (not accurate for large areas)
    # For production, use PostGIS ST_Distance_Sphere or similar
    lat_delta = radius_km / 111.0  # Approximate km per degree latitude
    lon_delta = radius_km / (111.0 * abs(float(latitude)))  # Adjust for latitude
    
    return db.query(models.FloodEvent).filter(
        models.FloodEvent.latitude.between(latitude - lat_delta, latitude + lat_delta),
        models.FloodEvent.longitude.between(longitude - lon_delta, longitude + lon_delta)
    ).order_by(desc(models.FloodEvent.timestamp)).all()


def delete_flood_event(db: Session, flood_id: int) -> bool:
    """
    Delete a flood event by ID.
    
    Args:
        db: Database session
        flood_id: ID of the flood event to delete
    
    Returns:
        True if deleted, False if not found
    """
    flood_event = get_flood_event(db, flood_id)
    if flood_event:
        db.delete(flood_event)
        db.commit()
        return True
    return False


# User CRUD Operations (Optional, for authentication)

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str) -> models.User:
    """
    Create a new user account.
    
    Args:
        db: Database session
        user: User registration data
        hashed_password: Bcrypt hashed password
    
    Returns:
        Created User model instance
    """
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        is_active=1,
        is_admin=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get list of users."""
    return db.query(models.User).offset(skip).limit(limit).all()


# Alert Subscription CRUD Operations

def create_subscription(
    db: Session,
    subscription: schemas.AlertSubscriptionCreate
) -> models.AlertSubscription:
    """
    Create a new alert subscription.
    
    Args:
        db: Database session
        subscription: Subscription data
    
    Returns:
        Created AlertSubscription model instance
    """
    db_subscription = models.AlertSubscription(
        email=subscription.email,
        phone=subscription.phone,
        latitude=subscription.latitude,
        longitude=subscription.longitude,
        radius_km=subscription.radius_km,
        min_severity=subscription.min_severity,
        is_active=1
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def get_subscription(db: Session, subscription_id: int) -> Optional[models.AlertSubscription]:
    """Get subscription by ID."""
    return db.query(models.AlertSubscription).filter(
        models.AlertSubscription.id == subscription_id
    ).first()


def get_subscriptions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
) -> List[models.AlertSubscription]:
    """Get list of subscriptions."""
    query = db.query(models.AlertSubscription)
    
    if active_only:
        query = query.filter(models.AlertSubscription.is_active == 1)
    
    return query.offset(skip).limit(limit).all()


def get_subscriptions_near_location(
    db: Session,
    latitude: float,
    longitude: float,
    min_severity: str = "Low"
) -> List[models.AlertSubscription]:
    """
    Get subscriptions that should be notified for a location.
    
    Args:
        db: Database session
        latitude: Event latitude
        longitude: Event longitude
        min_severity: Event severity level
    
    Returns:
        List of subscriptions within radius
    """
    # Severity order: Low < Medium < High < Critical
    severity_order = {"Low": 0, "Medium": 1, "High": 2, "Critical": 3}
    event_severity_level = severity_order.get(min_severity, 0)
    
    subscriptions = db.query(models.AlertSubscription).filter(
        models.AlertSubscription.is_active == 1
    ).all()
    
    # Filter subscriptions within radius and matching severity
    matching_subs = []
    for sub in subscriptions:
        # Calculate approximate distance (simplified)
        lat_diff = abs(sub.latitude - latitude)
        lon_diff = abs(sub.longitude - longitude)
        approx_dist_km = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111  # Rough km conversion
        
        sub_severity_level = severity_order.get(sub.min_severity, 0)
        
        if approx_dist_km <= sub.radius_km and event_severity_level >= sub_severity_level:
            matching_subs.append(sub)
    
    return matching_subs


def update_subscription(
    db: Session,
    subscription_id: int,
    subscription_update: schemas.AlertSubscriptionUpdate
) -> Optional[models.AlertSubscription]:
    """Update subscription."""
    db_subscription = get_subscription(db, subscription_id)
    if not db_subscription:
        return None
    
    update_data = subscription_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subscription, field, value)
    
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, subscription_id: int) -> bool:
    """Delete subscription."""
    subscription = get_subscription(db, subscription_id)
    if subscription:
        db.delete(subscription)
        db.commit()
        return True
    return False
