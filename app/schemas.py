"""
Pydantic schemas for request/response validation.
Defines the data structures for API input and output.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum


class SeverityLevel(str, Enum):
    """Enum for flood severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# Flood Event Schemas

class FloodEventBase(BaseModel):
    """Base schema with common flood event fields."""
    location_name: str = Field(..., description="Name of the location")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    description: Optional[str] = Field(None, description="Additional details")


class FloodEventCreate(FloodEventBase):
    """
    Schema for creating a new flood event.
    Risk score and severity are calculated automatically.
    """
    # Optional fields that can be provided or will be fetched
    rainfall_mm: Optional[float] = Field(None, ge=0, description="Rainfall in mm")
    elevation_m: Optional[float] = Field(None, description="Elevation in meters")


class FloodEventResponse(FloodEventBase):
    """
    Schema for flood event responses.
    Includes all fields including calculated risk data.
    """
    id: int
    severity: SeverityLevel
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    timestamp: datetime
    rainfall_mm: Optional[float]
    elevation_m: Optional[float]
    
    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy models


class FloodEventUpdate(BaseModel):
    """Schema for updating flood event (optional, for future use)."""
    location_name: Optional[str] = None
    description: Optional[str] = None


# Risk Calculation Schemas

class RiskCalculationRequest(BaseModel):
    """Request schema for calculating flood risk."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_name: Optional[str] = Field(None)


class RiskCalculationResponse(BaseModel):
    """Response schema for flood risk calculation."""
    latitude: float
    longitude: float
    location_name: Optional[str]
    risk_score: float = Field(..., ge=0, le=100)
    severity: SeverityLevel
    rainfall_mm: float
    elevation_m: float
    factors: dict = Field(default_factory=dict, description="Breakdown of risk factors")


# Authentication Schemas (Optional)

class UserBase(BaseModel):
    """Base user schema."""
    email: str = Field(..., description="User email")
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="User password")


class UserResponse(UserBase):
    """Schema for user responses."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    username: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


# General Response Schemas

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None
    status_code: int


# Alert Subscription Schemas

class AlertSubscriptionBase(BaseModel):
    """Base schema for alert subscriptions."""
    email: Optional[str] = Field(None, description="Email for alerts")
    phone: Optional[str] = Field(None, description="Phone number for SMS alerts (+1234567890)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude to monitor")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude to monitor")
    radius_km: float = Field(5.0, ge=0.1, le=50, description="Alert radius in km")
    min_severity: str = Field("Medium", description="Minimum severity (Low/Medium/High/Critical)")


class AlertSubscriptionCreate(AlertSubscriptionBase):
    """Schema for creating alert subscription."""
    pass


class AlertSubscriptionResponse(AlertSubscriptionBase):
    """Schema for alert subscription response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlertSubscriptionUpdate(BaseModel):
    """Schema for updating alert subscription."""
    email: Optional[str] = None
    phone: Optional[str] = None
    radius_km: Optional[float] = None
    min_severity: Optional[str] = None
    is_active: Optional[bool] = None


# Notification Schemas

class NotificationTest(BaseModel):
    """Schema for testing notifications."""
    email: Optional[str] = Field(None, description="Email to test")
    phone: Optional[str] = Field(None, description="Phone to test SMS")


class NotificationResult(BaseModel):
    """Schema for notification results."""
    sms_sent: int = 0
    sms_failed: int = 0
    emails_sent: int = 0
    emails_failed: int = 0
    message: str = "Notifications processed"

