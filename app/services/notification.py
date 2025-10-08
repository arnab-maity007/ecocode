"""
Notification service for sending alerts via email, SMS, and push notifications.
Integrates with Twilio for SMS and SMTP for email.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from ..config import settings
import httpx


class NotificationService:
    """Service for sending notifications to users."""
    
    def __init__(self):
        self.twilio_sid = settings.TWILIO_ACCOUNT_SID
        self.twilio_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone = settings.TWILIO_PHONE_NUMBER
        self.smtp_server = getattr(settings, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_email = getattr(settings, 'SMTP_EMAIL', None)
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', None)
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send SMS notification via Twilio.
        
        Args:
            to_phone: Phone number with country code (e.g., +1234567890)
            message: Message content
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not all([self.twilio_sid, self.twilio_token, self.twilio_phone]):
            print("⚠️ Twilio credentials not configured. SMS not sent.")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
                
                response = await client.post(
                    url,
                    auth=(self.twilio_sid, self.twilio_token),
                    data={
                        "From": self.twilio_phone,
                        "To": to_phone,
                        "Body": message
                    },
                    timeout=10.0
                )
                
                if response.status_code == 201:
                    print(f"✅ SMS sent to {to_phone}")
                    return True
                else:
                    print(f"❌ SMS failed: {response.text}")
                    return False
        
        except Exception as e:
            print(f"❌ SMS error: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send email notification via SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text body
            html_body: Optional HTML body
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not all([self.smtp_email, self.smtp_password]):
            print("⚠️ SMTP credentials not configured. Email not sent.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach HTML if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False
    
    async def send_flood_alert(
        self,
        location_name: str,
        risk_level: str,
        risk_score: float,
        latitude: float,
        longitude: float,
        phone_numbers: Optional[List[str]] = None,
        emails: Optional[List[str]] = None
    ) -> dict:
        """
        Send flood alert notifications to subscribed users.
        
        Args:
            location_name: Name of the location
            risk_level: Severity level (Low/Medium/High/Critical)
            risk_score: Risk score (0-100)
            latitude: Location latitude
            longitude: Location longitude
            phone_numbers: List of phone numbers to notify
            emails: List of emails to notify
        
        Returns:
            Dictionary with notification results
        """
        # Create message content
        sms_message = (
            f"🌊 FLOOD ALERT: {risk_level} risk at {location_name}\n"
            f"Risk Score: {risk_score:.1f}/100\n"
            f"Location: {latitude:.4f}, {longitude:.4f}\n"
            f"Take necessary precautions."
        )
        
        email_subject = f"🌊 Flood Alert: {risk_level} Risk at {location_name}"
        
        email_body = f"""
Flood Risk Alert

Location: {location_name}
Risk Level: {risk_level}
Risk Score: {risk_score:.1f}/100
Coordinates: {latitude:.4f}, {longitude:.4f}

Please take necessary precautions and stay safe.

This is an automated alert from the Hyperlocal Urban Flood Forecaster.
"""
        
        email_html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center;">
        <h1 style="color: white; margin: 0;">🌊 Flood Risk Alert</h1>
    </div>
    
    <div style="padding: 20px; background-color: #f8f9fa;">
        <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: {'#dc3545' if risk_level in ['High', 'Critical'] else '#ffc107' if risk_level == 'Medium' else '#28a745'};">
                {risk_level} Risk Level
            </h2>
            <p><strong>Location:</strong> {location_name}</p>
            <p><strong>Risk Score:</strong> {risk_score:.1f}/100</p>
            <p><strong>Coordinates:</strong> {latitude:.4f}, {longitude:.4f}</p>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
            <p style="margin: 0; color: #856404;">
                ⚠️ Please take necessary precautions and stay alert. Monitor local authorities for updates.
            </p>
        </div>
    </div>
    
    <div style="background: #343a40; padding: 15px; text-align: center; color: white;">
        <p style="margin: 0; font-size: 12px;">
            Hyperlocal Urban Flood Forecaster - Automated Alert System
        </p>
    </div>
</body>
</html>
"""
        
        results = {
            "sms_sent": 0,
            "sms_failed": 0,
            "emails_sent": 0,
            "emails_failed": 0
        }
        
        # Send SMS notifications
        if phone_numbers:
            for phone in phone_numbers:
                success = await self.send_sms(phone, sms_message)
                if success:
                    results["sms_sent"] += 1
                else:
                    results["sms_failed"] += 1
        
        # Send email notifications
        if emails:
            for email in emails:
                success = self.send_email(email, email_subject, email_body, email_html)
                if success:
                    results["emails_sent"] += 1
                else:
                    results["emails_failed"] += 1
        
        return results
    
    async def send_test_notification(self, phone: Optional[str] = None, email: Optional[str] = None) -> dict:
        """
        Send test notification to verify setup.
        
        Args:
            phone: Phone number to test SMS
            email: Email to test email
        
        Returns:
            Test results
        """
        results = {"sms_success": False, "email_success": False}
        
        if phone:
            results["sms_success"] = await self.send_sms(
                phone,
                "🌊 Test notification from Flood Forecaster. Your alerts are configured correctly!"
            )
        
        if email:
            results["email_success"] = self.send_email(
                email,
                "🌊 Test Notification - Flood Forecaster",
                "This is a test notification from the Hyperlocal Urban Flood Forecaster.\n\nYour email alerts are configured correctly!",
                "<h2>🌊 Test Notification</h2><p>Your email alerts are configured correctly!</p>"
            )
        
        return results


# Global notification service instance
notification_service = NotificationService()
