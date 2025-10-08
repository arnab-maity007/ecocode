# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Get API Keys (Free)
- **OpenWeatherMap**: https://openweathermap.org/api (Free tier: 1000 calls/day)
- **NeonDB**: https://neon.tech (Free serverless PostgreSQL)
- **Google Elevation** (Optional): https://developers.google.com/maps/documentation/elevation

### 3. Setup NeonDB (2 minutes)
```bash
# Go to https://neon.tech
# Sign up (free)
# Create a project
# Copy your connection string
```

### 4. Configure Environment
```bash
# Copy and edit .env file
copy .env.example .env
```

Edit `.env`:
```env
# Get this from your NeonDB dashboard
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require
OPENWEATHERMAP_API_KEY=your_actual_api_key
SECRET_KEY=run_this_command_to_generate_python_-c_"import secrets; print(secrets.token_hex(32))"
```

### 5. Run Server (Auto-creates tables)
```bash
python main.py
# Or: uvicorn main:app --reload
```

✅ Tables are automatically created in NeonDB on first run!

Visit http://localhost:8000/docs for interactive API documentation!

## Test the API

### Using curl:
```bash
# Create a flood event
curl -X POST "http://localhost:8000/api/v1/floods/" \
  -H "Content-Type: application/json" \
  -d "{\"location_name\":\"Main St\",\"latitude\":40.7128,\"longitude\":-74.0060}"

# Get all events
curl "http://localhost:8000/api/v1/floods/"

# Calculate risk
curl -X POST "http://localhost:8000/api/v1/floods/calculate-risk" \
  -H "Content-Type: application/json" \
  -d "{\"latitude\":40.7128,\"longitude\":-74.0060,\"location_name\":\"Test\"}"
```

### Using Python:
```python
import requests

# Create flood event
response = requests.post(
    "http://localhost:8000/api/v1/floods/",
    json={
        "location_name": "Main Street",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
)
print(response.json())
```

## Frontend Integration

### React Example
```javascript
const API_URL = 'http://localhost:8000/api/v1';

// Get flood events
fetch(`${API_URL}/floods/`)
  .then(res => res.json())
  .then(data => console.log(data));

// Create flood event
fetch(`${API_URL}/floods/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    location_name: "Downtown",
    latitude: 40.7128,
    longitude: -74.0060
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Common Issues

### Port Already in Use
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

### Database Connection Error
- Check your NeonDB connection string in .env
- Verify `?sslmode=require` is at the end of the URL
- Ensure NeonDB project is not paused (auto-pauses after inactivity)
- Wake it up by visiting https://console.neon.tech

### API Key Issues
- Verify keys are correct in .env
- Check quotas on API provider dashboards
- Google Elevation is optional (uses mock data if not configured)

## Next Steps

1. ✅ Set up frontend to consume API
2. ✅ Add more locations to test
3. ✅ Monitor API at /docs
4. ✅ Customize risk calculation in `app/services/flood_risk.py`
5. ✅ Add your own machine learning model

Happy Coding! 🚀
