"""
Flood risk calculation service.
Integrates with OpenWeatherMap API and Google Elevation API to calculate flood risk scores.
"""

import httpx
from typing import Tuple, Optional, Dict
from ..config import settings
from ..schemas import SeverityLevel


class FloodRiskService:
    """
    Service for calculating flood risk based on weather and terrain data.
    
    Risk Score Calculation (MVP):
    - Rainfall contribution: 0-60 points (higher rainfall = higher risk)
    - Elevation contribution: 0-40 points (lower elevation = higher risk)
    - Total: 0-100 points
    
    Severity Levels:
    - Low: 0-25
    - Medium: 26-50
    - High: 51-75
    - Critical: 76-100
    """
    
    def __init__(self):
        self.openweather_api_key = settings.OPENWEATHERMAP_API_KEY
        self.google_elevation_api_key = settings.GOOGLE_ELEVATION_API_KEY
        self.openweather_base_url = "https://api.openweathermap.org/data/2.5"
        self.google_elevation_base_url = "https://maps.googleapis.com/maps/api/elevation/json"
    
    async def get_rainfall_data(self, latitude: float, longitude: float) -> float:
        """
        Fetch current rainfall data from OpenWeatherMap API.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            Rainfall amount in mm (last hour or current)
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get current weather data
                url = f"{self.openweather_base_url}/weather"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.openweather_api_key,
                    "units": "metric"
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Extract rainfall data (rain in last 1 hour)
                rainfall = 0.0
                if "rain" in data:
                    rainfall = data["rain"].get("1h", 0.0)  # mm in last hour
                
                # If no current rain, check forecast for precipitation
                if rainfall == 0.0:
                    rainfall = await self._get_forecast_rainfall(latitude, longitude)
                
                return rainfall
        
        except httpx.HTTPError as e:
            print(f"Error fetching rainfall data: {e}")
            # Return mock data for development/testing
            return 5.0  # Default moderate rainfall
        except Exception as e:
            print(f"Unexpected error in get_rainfall_data: {e}")
            return 5.0
    
    async def _get_forecast_rainfall(self, latitude: float, longitude: float) -> float:
        """
        Get forecasted rainfall from OpenWeatherMap forecast API.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            Predicted rainfall in mm
        """
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.openweather_base_url}/forecast"
                params = {
                    "lat": latitude,
                    "lon": longitude,
                    "appid": self.openweather_api_key,
                    "units": "metric",
                    "cnt": 8  # Next 24 hours (3-hour intervals)
                }
                
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Sum up rainfall from next few hours
                total_rainfall = 0.0
                if "list" in data:
                    for forecast in data["list"][:4]:  # Next 12 hours
                        if "rain" in forecast:
                            total_rainfall += forecast["rain"].get("3h", 0.0)
                
                return total_rainfall / 4 if total_rainfall > 0 else 0.0  # Average per 3 hours
        
        except Exception as e:
            print(f"Error fetching forecast data: {e}")
            return 0.0
    
    async def get_elevation_data(self, latitude: float, longitude: float) -> float:
        """
        Fetch elevation data from Google Elevation API or use mock data.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            Elevation in meters above sea level
        """
        # If Google API key is not configured, use mock elevation
        if not self.google_elevation_api_key or self.google_elevation_api_key == "your_google_elevation_api_key_here":
            return self._mock_elevation(latitude, longitude)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "locations": f"{latitude},{longitude}",
                    "key": self.google_elevation_api_key
                }
                
                response = await client.get(
                    self.google_elevation_base_url,
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") == "OK" and data.get("results"):
                    elevation = data["results"][0]["elevation"]
                    return elevation
                else:
                    return self._mock_elevation(latitude, longitude)
        
        except Exception as e:
            print(f"Error fetching elevation data: {e}")
            return self._mock_elevation(latitude, longitude)
    
    def _mock_elevation(self, latitude: float, longitude: float) -> float:
        """
        Generate mock elevation data based on coordinates.
        For MVP/development use when Google API is not configured.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
        
        Returns:
            Mock elevation in meters
        """
        # Simple heuristic: use latitude to vary elevation
        # Coastal areas (near equator) tend to be lower
        base_elevation = abs(latitude) * 10  # 0-900m range
        variation = (hash(f"{latitude},{longitude}") % 100) - 50  # -50 to +50m
        return max(0, base_elevation + variation)
    
    def calculate_risk_score(
        self,
        rainfall_mm: float,
        elevation_m: float
    ) -> Tuple[float, str]:
        """
        Calculate flood risk score based on rainfall and elevation.
        
        Risk Score Formula (MVP):
        - Rainfall Score (0-60): Higher rainfall increases risk
          - 0-5mm: 10 points
          - 5-15mm: 20 points
          - 15-30mm: 35 points
          - 30-50mm: 50 points
          - 50+ mm: 60 points
        
        - Elevation Score (0-40): Lower elevation increases risk
          - 0-10m: 40 points (very high risk - near sea level)
          - 10-50m: 30 points
          - 50-100m: 20 points
          - 100-200m: 10 points
          - 200+m: 5 points (low risk - elevated areas)
        
        Args:
            rainfall_mm: Rainfall amount in millimeters
            elevation_m: Elevation in meters
        
        Returns:
            Tuple of (risk_score, severity_level)
        """
        # Calculate rainfall contribution (0-60 points)
        if rainfall_mm < 5:
            rainfall_score = 10
        elif rainfall_mm < 15:
            rainfall_score = 20
        elif rainfall_mm < 30:
            rainfall_score = 35
        elif rainfall_mm < 50:
            rainfall_score = 50
        else:
            rainfall_score = 60
        
        # Calculate elevation contribution (0-40 points)
        # Lower elevation = higher risk
        if elevation_m < 10:
            elevation_score = 40
        elif elevation_m < 50:
            elevation_score = 30
        elif elevation_m < 100:
            elevation_score = 20
        elif elevation_m < 200:
            elevation_score = 10
        else:
            elevation_score = 5
        
        # Total risk score (0-100)
        total_score = rainfall_score + elevation_score
        
        # Determine severity level
        if total_score <= 25:
            severity = SeverityLevel.LOW
        elif total_score <= 50:
            severity = SeverityLevel.MEDIUM
        elif total_score <= 75:
            severity = SeverityLevel.HIGH
        else:
            severity = SeverityLevel.CRITICAL
        
        return total_score, severity.value
    
    async def calculate_flood_risk(
        self,
        latitude: float,
        longitude: float,
        rainfall_override: Optional[float] = None,
        elevation_override: Optional[float] = None
    ) -> Dict:
        """
        Complete flood risk calculation for a location.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            rainfall_override: Optional manual rainfall value (for testing)
            elevation_override: Optional manual elevation value (for testing)
        
        Returns:
            Dictionary with risk calculation results
        """
        # Fetch data from APIs or use overrides
        rainfall = rainfall_override if rainfall_override is not None else await self.get_rainfall_data(latitude, longitude)
        elevation = elevation_override if elevation_override is not None else await self.get_elevation_data(latitude, longitude)
        
        # Calculate risk score
        risk_score, severity = self.calculate_risk_score(rainfall, elevation)
        
        return {
            "rainfall_mm": rainfall,
            "elevation_m": elevation,
            "risk_score": risk_score,
            "severity": severity,
            "factors": {
                "rainfall_contribution": "High" if rainfall > 30 else "Medium" if rainfall > 15 else "Low",
                "elevation_contribution": "High risk" if elevation < 50 else "Medium risk" if elevation < 100 else "Low risk",
                "explanation": f"Risk is {'elevated' if risk_score > 50 else 'moderate' if risk_score > 25 else 'low'} due to "
                              f"{'heavy' if rainfall > 30 else 'moderate' if rainfall > 15 else 'light'} rainfall "
                              f"and {'low' if elevation < 50 else 'moderate' if elevation < 100 else 'high'} elevation."
            }
        }


# Global service instance
flood_risk_service = FloodRiskService()
