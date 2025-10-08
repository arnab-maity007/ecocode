"""
Notifications API router.
Provides endpoints for managing alert subscriptions and sending notifications.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from ..services.notification import notification_service

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.post("/subscribe", response_model=schemas.AlertSubscriptionResponse, status_code=201)
async def subscribe_to_alerts(
    subscription: schemas.AlertSubscriptionCreate,
    db: Session = Depends(get_db)
):
    """
    Subscribe to flood alerts for a specific location.
    
    **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "phone": "+1234567890",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "radius_km": 5.0,
        "min_severity": "Medium"
    }
    ```
    
    **Note:** Provide either email, phone, or both.
    
    **Returns:**
    Created subscription with ID.
    """
    # Validate at least one contact method
    if not subscription.email and not subscription.phone:
        raise HTTPException(
            status_code=400,
            detail="At least one contact method (email or phone) is required"
        )
    
    # Create subscription
    db_subscription = crud.create_subscription(db, subscription)
    
    # Send confirmation notification
    if subscription.email:
        notification_service.send_email(
            to_email=subscription.email,
            subject="🌊 Flood Alert Subscription Confirmed",
            body=f"You're now subscribed to flood alerts for location ({subscription.latitude}, {subscription.longitude}) within {subscription.radius_km}km radius.",
            html_body=f"""
            <h2>🌊 Subscription Confirmed</h2>
            <p>You're now subscribed to flood alerts for:</p>
            <ul>
                <li><strong>Location:</strong> {subscription.latitude}, {subscription.longitude}</li>
                <li><strong>Radius:</strong> {subscription.radius_km} km</li>
                <li><strong>Minimum Severity:</strong> {subscription.min_severity}</li>
            </ul>
            <p>You'll receive alerts via email when floods are detected in your area.</p>
            """
        )
    
    return db_subscription


@router.get("/subscriptions", response_model=List[schemas.AlertSubscriptionResponse])
async def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get list of alert subscriptions.
    
    **Query Parameters:**
    - skip: Pagination offset
    - limit: Maximum results
    - active_only: Show only active subscriptions
    """
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit, active_only=active_only)
    return subscriptions


@router.get("/subscriptions/{subscription_id}", response_model=schemas.AlertSubscriptionResponse)
async def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    """Get specific subscription by ID."""
    subscription = crud.get_subscription(db, subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription


@router.put("/subscriptions/{subscription_id}", response_model=schemas.AlertSubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    subscription_update: schemas.AlertSubscriptionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update subscription settings.
    
    **Request Body:**
    ```json
    {
        "email": "newemail@example.com",
        "radius_km": 10.0,
        "min_severity": "High",
        "is_active": true
    }
    ```
    """
    updated = crud.update_subscription(db, subscription_id, subscription_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return updated


@router.delete("/subscriptions/{subscription_id}", response_model=schemas.MessageResponse)
async def delete_subscription(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    """Unsubscribe from alerts."""
    success = crud.delete_subscription(db, subscription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    return schemas.MessageResponse(
        message="Successfully unsubscribed from alerts",
        detail=f"Deleted subscription ID {subscription_id}"
    )


@router.post("/test", response_model=dict)
async def test_notifications(test: schemas.NotificationTest):
    """
    Test notification system.
    
    **Request Body:**
    ```json
    {
        "email": "test@example.com",
        "phone": "+1234567890"
    }
    ```
    
    **Returns:**
    Results of test notifications.
    """
    if not test.email and not test.phone:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one contact method to test"
        )
    
    results = await notification_service.send_test_notification(
        phone=test.phone,
        email=test.email
    )
    
    return {
        "message": "Test notifications sent",
        "results": results
    }


@router.post("/send-alert", response_model=schemas.NotificationResult)
async def send_alert_notifications(
    flood_id: int,
    db: Session = Depends(get_db)
):
    """
    Send notifications for a specific flood event to subscribed users.
    
    **Parameters:**
    - flood_id: ID of the flood event
    
    **Returns:**
    Notification results (emails and SMS sent/failed)
    """
    # Get flood event
    flood_event = crud.get_flood_event(db, flood_id)
    if not flood_event:
        raise HTTPException(status_code=404, detail="Flood event not found")
    
    # Get subscriptions near this location
    subscriptions = crud.get_subscriptions_near_location(
        db,
        latitude=flood_event.latitude,
        longitude=flood_event.longitude,
        min_severity=flood_event.severity
    )
    
    if not subscriptions:
        return schemas.NotificationResult(
            message="No subscriptions found for this location"
        )
    
    # Collect contact information
    emails = [sub.email for sub in subscriptions if sub.email]
    phones = [sub.phone for sub in subscriptions if sub.phone]
    
    # Send notifications
    results = await notification_service.send_flood_alert(
        location_name=flood_event.location_name,
        risk_level=flood_event.severity,
        risk_score=flood_event.risk_score,
        latitude=flood_event.latitude,
        longitude=flood_event.longitude,
        phone_numbers=phones if phones else None,
        emails=emails if emails else None
    )
    
    return schemas.NotificationResult(
        sms_sent=results.get("sms_sent", 0),
        sms_failed=results.get("sms_failed", 0),
        emails_sent=results.get("emails_sent", 0),
        emails_failed=results.get("emails_failed", 0),
        message=f"Notified {len(subscriptions)} subscriptions"
    )
