# 🌊 Hyperlocal Urban Flood Forecaster - Backend API

A production-ready FastAPI backend for predicting street-level flood risks using real-time weather data, elevation information, and AI-powered risk calculations.

## 🎯 Features

- **Real-time Flood Risk Prediction**: Uses OpenWeatherMap for rainfall data and Google Elevation API for terrain analysis
- **AI-Powered Risk Scoring**: Calculates 0-100 risk scores based on multiple factors
- **RESTful API**: Complete CRUD operations for flood events
- **Geospatial Queries**: Find flood events by location with radius search
- **JWT Authentication**: Optional user management system
- **CORS Enabled**: Ready for React/Vue/Angular frontend integration
- **PostgreSQL Database**: Robust data storage with SQLAlchemy ORM
- **Auto-generated API Documentation**: Interactive Swagger UI and ReDoc

## 📋 Prerequisites

- Python 3.9 or higher
- NeonDB account (free serverless PostgreSQL - https://neon.tech)
- OpenWeatherMap API key (free tier available)
- Google Elevation API key (optional, falls back to mock data)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to project directory
cd floodAurra

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup (NeonDB)

✅ **No local PostgreSQL installation needed!**

1. Go to https://neon.tech and sign up (free tier)
2. Create a new project
3. Copy your connection string (it looks like):
   ```
   postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require
   ```
4. Paste it into your `.env` file as `DATABASE_URL`

Tables will be **created automatically** when you run the application!

### 3. Environment Configuration

```bash
# Copy example environment file
copy .env.example .env

# Edit .env with your configuration
# Required:
# - DATABASE_URL
# - OPENWEATHERMAP_API_KEY
# - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_hex(32))")
```

**Example `.env` file:**

```env
# NeonDB Connection (from your NeonDB dashboard)
DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require

OPENWEATHERMAP_API_KEY=your_api_key_here
GOOGLE_ELEVATION_API_KEY=optional_key_here
SECRET_KEY=generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Hyperlocal Urban Flood Forecaster
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Run Application (Tables Auto-Created)

```bash
# Simply run the application - it will create tables automatically in NeonDB
python main.py

# Tables are created on first run - no manual setup needed!
```

### 5. Run the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🗂️ Project Structure

```
floodAurra/
├── app/
│   ├── __init__.py           # App package initialization
│   ├── config.py             # Configuration and settings
│   ├── database.py           # Database connection and session
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── crud.py               # Database CRUD operations
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── floods.py         # Flood events endpoints
│   │   └── auth.py           # Authentication endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── flood_risk.py     # Risk calculation logic
│   └── utils/
│       ├── __init__.py
│       └── auth.py           # JWT and password utilities
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🧮 Risk Calculation Logic

### MVP Risk Score Formula (0-100 scale)

**Rainfall Component (0-60 points):**
- 0-5mm: 10 points
- 5-15mm: 20 points
- 15-30mm: 35 points
- 30-50mm: 50 points
- 50+mm: 60 points

**Elevation Component (0-40 points):**
- 0-10m: 40 points (very high risk)
- 10-50m: 30 points (high risk)
- 50-100m: 20 points (moderate risk)
- 100-200m: 10 points (low risk)
- 200+m: 5 points (very low risk)

**Severity Levels:**
- **Low**: 0-25 points
- **Medium**: 26-50 points
- **High**: 51-75 points
- **Critical**: 76-100 points


## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | ✅ Yes | - |
| OPENWEATHERMAP_API_KEY | OpenWeatherMap API key | ✅ Yes | - |
| GOOGLE_ELEVATION_API_KEY | Google Elevation API key | ❌ No | Mock data |
| SECRET_KEY | JWT secret key | ✅ Yes | - |
| ALGORITHM | JWT algorithm | ❌ No | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry time | ❌ No | 30 |
| DEBUG | Debug mode | ❌ No | False |
| ALLOWED_ORIGINS | CORS allowed origins | ❌ No | localhost:3000 |

## 🚀 Deployment

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t flood-forecaster-api .
docker run -p 8000:8000 --env-file .env flood-forecaster-api
```

### Production Considerations

1. **Database**: Use connection pooling and prepared statements
2. **Security**: Enable HTTPS, implement rate limiting, use secure secrets
3. **Monitoring**: Add logging, error tracking (Sentry), and metrics
4. **Scaling**: Use gunicorn/uvicorn workers, load balancer, caching (Redis)
5. **Backups**: Automated database backups

## 📊 Database Schema

### flood_events Table
```sql
CREATE TABLE flood_events (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    severity VARCHAR NOT NULL,
    risk_score FLOAT NOT NULL,
    rainfall_mm FLOAT,
    elevation_m FLOAT,
    description TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### users Table (Optional)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🛠️ Future Enhancements

- [ ] CNN-LSTM hybrid model for advanced predictions
- [ ] Real-time notifications via Twilio/Firebase
- [ ] Historical flood data analysis
- [ ] Weather radar integration
- [ ] Drainage system data integration
- [ ] Mobile app support
- [ ] WebSocket for real-time updates
- [ ] PostGIS for advanced geospatial queries
- [ ] Multi-language support
- [ ] Admin dashboard

## 🤝 Contributing

### Arnab maity
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/arnab-maity007)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arnab-maity-860050229/)

### shraddhanjali Barik
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Shraddhanjali04)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shraddhanjali-barik-00bb9634b/)

### Nishchay Garg
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Nishchay71177)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nishchay-garg-a04994351/)

### Sahil mishra
[![GitHub](https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mishraji55)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mishraji721/)




Contributions are welcome! Please follow these steps:



## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

