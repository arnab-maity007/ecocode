# API Examples and Sample Responses

## Sample API Requests and Responses

### 1. Create Flood Event

**Request:**
```bash
POST http://localhost:8000/api/v1/floods/
Content-Type: application/json

{
  "location_name": "Downtown Main Street",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "description": "Major intersection near waterfront"
}
```

**Response:**
```json
{
  "id": 1,
  "location_name": "Downtown Main Street",
  "latitude": 40.7128,
  "longitude": -74.006,
  "severity": "Medium",
  "risk_score": 45.0,
  "timestamp": "2025-10-08T14:30:00.123456+00:00",
  "rainfall_mm": 12.5,
  "elevation_m": 23.4,
  "description": "Major intersection near waterfront"
}
```

### 2. Get All Flood Events

**Request:**
```bash
GET http://localhost:8000/api/v1/floods/?limit=10&skip=0
```

**Response:**
```json
[
  {
    "id": 1,
    "location_name": "Downtown Main Street",
    "latitude": 40.7128,
    "longitude": -74.006,
    "severity": "Medium",
    "risk_score": 45.0,
    "timestamp": "2025-10-08T14:30:00.123456+00:00",
    "rainfall_mm": 12.5,
    "elevation_m": 23.4,
    "description": "Major intersection near waterfront"
  },
  {
    "id": 2,
    "location_name": "Riverside Park",
    "latitude": 40.7829,
    "longitude": -73.9654,
    "severity": "High",
    "risk_score": 68.0,
    "timestamp": "2025-10-08T15:00:00.789012+00:00",
    "rainfall_mm": 38.2,
    "elevation_m": 8.5,
    "description": "Low-lying area near river"
  }
]
```

### 3. Calculate Risk Score

**Request:**
```bash
POST http://localhost:8000/api/v1/floods/calculate-risk
Content-Type: application/json

{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "location_name": "Test Location"
}
```

**Response:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.006,
  "location_name": "Test Location",
  "risk_score": 55.0,
  "severity": "High",
  "rainfall_mm": 22.3,
  "elevation_m": 18.7,
  "factors": {
    "rainfall_contribution": "Medium",
    "elevation_contribution": "High risk",
    "explanation": "Risk is elevated due to moderate rainfall and low elevation."
  }
}
```

### 4. Get Nearby Flood Events

**Request:**
```bash
GET http://localhost:8000/api/v1/floods/nearby/?latitude=40.7128&longitude=-74.0060&radius_km=5
```

**Response:**
```json
[
  {
    "id": 1,
    "location_name": "Downtown Main Street",
    "latitude": 40.7128,
    "longitude": -74.006,
    "severity": "Medium",
    "risk_score": 45.0,
    "timestamp": "2025-10-08T14:30:00.123456+00:00",
    "rainfall_mm": 12.5,
    "elevation_m": 23.4,
    "description": "Major intersection near waterfront"
  }
]
```

### 5. Get Single Flood Event

**Request:**
```bash
GET http://localhost:8000/api/v1/floods/1
```

**Response:**
```json
{
  "id": 1,
  "location_name": "Downtown Main Street",
  "latitude": 40.7128,
  "longitude": -74.006,
  "severity": "Medium",
  "risk_score": 45.0,
  "timestamp": "2025-10-08T14:30:00.123456+00:00",
  "rainfall_mm": 12.5,
  "elevation_m": 23.4,
  "description": "Major intersection near waterfront"
}
```

### 6. Filter by Severity

**Request:**
```bash
GET http://localhost:8000/api/v1/floods/?severity=High&limit=50
```

**Response:**
```json
[
  {
    "id": 2,
    "location_name": "Riverside Park",
    "latitude": 40.7829,
    "longitude": -73.9654,
    "severity": "High",
    "risk_score": 68.0,
    "timestamp": "2025-10-08T15:00:00.789012+00:00",
    "rainfall_mm": 38.2,
    "elevation_m": 8.5,
    "description": "Low-lying area near river"
  }
]
```

### 7. User Registration

**Request:**
```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-10-08T16:00:00.123456+00:00"
}
```

### 8. User Login

**Request:**
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=SecurePassword123!
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjk2Nzg5MjAwfQ.abc123...",
  "token_type": "bearer"
}
```

### 9. Get Current User Info

**Request:**
```bash
GET http://localhost:8000/api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-10-08T16:00:00.123456+00:00"
}
```

### 10. Delete Flood Event

**Request:**
```bash
DELETE http://localhost:8000/api/v1/floods/1
```

**Response:**
```json
{
  "message": "Flood event deleted successfully",
  "detail": "Deleted flood event with ID 1"
}
```

## Error Responses

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "latitude"],
      "msg": "ensure this value is less than or equal to 90",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 90}
    }
  ]
}
```

### Not Found Error
```json
{
  "detail": "Flood event not found"
}
```

### Authentication Error
```json
{
  "detail": "Could not validate credentials"
}
```

## Frontend Integration Examples

### JavaScript/Fetch
```javascript
// Get flood events
const getFloodEvents = async () => {
  const response = await fetch('http://localhost:8000/api/v1/floods/');
  const data = await response.json();
  return data;
};

// Create flood event
const createFloodEvent = async (eventData) => {
  const response = await fetch('http://localhost:8000/api/v1/floods/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(eventData),
  });
  const data = await response.json();
  return data;
};
```

### Axios (React)
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Get flood events
const getFloodEvents = async () => {
  const response = await axios.get(`${API_URL}/floods/`);
  return response.data;
};

// Create with authentication
const createWithAuth = async (eventData, token) => {
  const response = await axios.post(
    `${API_URL}/floods/`,
    eventData,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  return response.data;
};
```

### Python Requests
```python
import requests

API_URL = 'http://localhost:8000/api/v1'

# Get flood events
response = requests.get(f'{API_URL}/floods/')
flood_events = response.json()

# Create flood event
data = {
    'location_name': 'Main Street',
    'latitude': 40.7128,
    'longitude': -74.0060
}
response = requests.post(f'{API_URL}/floods/', json=data)
created_event = response.json()
```
