"""
SQLAlchemy ORM models for the Flood Forecaster application.
Defines the database schema for flood events and future user management.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base


class SeverityLevel(str, enum.Enum):
    """Enum for flood severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class FloodEvent(Base):
    """
    Model for storing flood events and predictions.
    
    Attributes:
        id: Primary key
        location_name: Human-readable location name (e.g., "Main Street, Downtown")
        latitude: Geographic latitude coordinate
        longitude: Geographic longitude coordinate
        severity: Risk level (Low, Medium, High, Critical)
        risk_score: Numerical risk score (0-100)
        timestamp: When the event was recorded/predicted
        rainfall_mm: Rainfall amount in millimeters
        elevation_m: Elevation above sea level in meters
        description: Optional additional details
    """
    __tablename__ = "flood_events"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    severity = Column(SQLEnum(SeverityLevel), nullable=False)
    risk_score = Column(Float, nullable=False)  # 0-100 scale
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Additional weather and terrain data
    rainfall_mm = Column(Float, nullable=True)  # Rainfall in mm
    elevation_m = Column(Float, nullable=True)  # Elevation in meters
    description = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<FloodEvent(id={self.id}, location='{self.location_name}', severity={self.severity}, score={self.risk_score})>"


# Future: User model for authentication
class User(Base):
    """
    Model for user accounts (optional, for future authentication).
    
    Attributes:
        id: Primary key
        email: User email (unique)
        username: User username (unique)
        hashed_password: Bcrypt hashed password
        is_active: Whether the account is active
        is_admin: Whether the user has admin privileges
        created_at: Account creation timestamp
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    is_admin = Column(Integer, default=0)  # 1 = admin, 0 = regular user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class AlertSubscription(Base):
    """
    Model for user alert subscriptions.
    
    Attributes:
        id: Primary key
        email: Subscriber email (optional)
        phone: Subscriber phone number (optional)
        latitude: Location latitude to monitor
        longitude: Location longitude to monitor
        radius_km: Alert radius in kilometers
        min_severity: Minimum severity to trigger alert (Low/Medium/High/Critical)
        is_active: Whether subscription is active
        created_at: Subscription creation timestamp
    """
    __tablename__ = "alert_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_km = Column(Float, default=5.0)  # Alert radius
    min_severity = Column(String, default="Medium")  # Low, Medium, High, Critical
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AlertSubscription(id={self.id}, email='{self.email}', location=({self.latitude}, {self.longitude}))>"

