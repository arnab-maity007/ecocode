# 🗄️ NeonDB Setup Guide for Flood Forecaster

## ✅ Your NeonDB Connection is Already Configured!

Your `.env` file shows:
```
DATABASE_URL=postgresql://neondb_owner:npg_...@ep-nameless-mud-adtrjmjk-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
```

✅ This is perfect and ready to use!

---

## 📋 What Tables Your Program Needs

Your FastAPI backend will **automatically create** these tables when you run `python main.py`:

### 1. **flood_events** Table
Stores all flood event predictions and historical data.

```sql
CREATE TABLE flood_events (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    severity VARCHAR(50) NOT NULL,  -- 'Low', 'Medium', 'High', 'Critical'
    risk_score FLOAT NOT NULL,      -- 0-100 scale
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    rainfall_mm FLOAT,              -- Rainfall in millimeters
    elevation_m FLOAT,              -- Elevation in meters
    description TEXT
);

CREATE INDEX idx_location_name ON flood_events(location_name);
```

**What it stores:**
- Location details (name, lat, lng)
- Risk assessment (score, severity)
- Weather data (rainfall, elevation)
- Timestamps for tracking

### 2. **users** Table (Optional - for authentication)
Stores user accounts for JWT authentication.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active INTEGER DEFAULT 1,    -- 1 = active, 0 = inactive
    is_admin INTEGER DEFAULT 0,     -- 1 = admin, 0 = regular user
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_username ON users(username);
```

**What it stores:**
- User credentials (email, username, hashed password)
- User status (active/inactive, admin/regular)
- Account creation date

---

## 🚀 Two Options to Create Tables

### **Option 1: Automatic (Recommended for MVP)**

Just run your application - it will create tables automatically:

```powershell
python main.py
```

The code in `main.py` includes:
```python
from app.database import init_db
init_db()  # This creates all tables automatically
```

### **Option 2: Manual (Using NeonDB SQL Editor)**

If you want to create tables manually in NeonDB:

1. **Go to NeonDB Console**: https://console.neon.tech
2. **Select your project**: `ep-nameless-mud-adtrjmjk`
3. **Open SQL Editor**
4. **Run this SQL:**

```sql
-- Create flood_events table
CREATE TABLE IF NOT EXISTS flood_events (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    severity VARCHAR(50) NOT NULL,
    risk_score DOUBLE PRECISION NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    rainfall_mm DOUBLE PRECISION,
    elevation_m DOUBLE PRECISION,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_flood_location ON flood_events(location_name);
CREATE INDEX IF NOT EXISTS idx_flood_timestamp ON flood_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_flood_severity ON flood_events(severity);

-- Create users table (optional)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active INTEGER DEFAULT 1,
    is_admin INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_user_username ON users(username);

-- Create enum type for severity
CREATE TYPE severity_level AS ENUM ('Low', 'Medium', 'High', 'Critical');
```

---

## 🔍 Verify Tables Were Created

### Using NeonDB SQL Editor:

```sql
-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check flood_events structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'flood_events';

-- Check users structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users';
```

### Using Python:

```powershell
python -c "from app.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"
```

---

## 📊 Sample Data for Testing

Once tables are created, you can insert test data:

### Via NeonDB SQL Editor:

```sql
-- Insert test flood events
INSERT INTO flood_events (location_name, latitude, longitude, severity, risk_score, rainfall_mm, elevation_m, description)
VALUES 
    ('Main Street, Downtown', 40.7128, -74.0060, 'High', 68.5, 35.2, 12.3, 'Heavy rainfall expected'),
    ('Riverside Park', 40.7829, -73.9654, 'Medium', 45.0, 18.5, 25.7, 'Moderate risk area'),
    ('Harbor District', 40.7061, -74.0134, 'Critical', 85.0, 52.0, 3.5, 'Low elevation, high risk');

-- Verify data
SELECT * FROM flood_events;
```

### Via API (after server is running):

```bash
curl -X POST "http://localhost:8000/api/v1/floods/" \
  -H "Content-Type: application/json" \
  -d '{
    "location_name": "Test Street",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "description": "Test location"
  }'
```

---

## ✅ What You DON'T Need to Do

❌ **Don't need to:**
- Install PostgreSQL locally (NeonDB is cloud-hosted)
- Configure PostGIS extensions (not required for MVP)
- Set up database backups (NeonDB handles this)
- Configure connection pooling (NeonDB Pooler handles this)
- Worry about database migrations (auto-created on first run)

---

## 🎯 Quick Start Checklist

- [x] ✅ NeonDB connection string configured in `.env`
- [x] ✅ OpenWeatherMap API key configured
- [x] ✅ SECRET_KEY configured
- [ ] ⚠️ Run `python main.py` to auto-create tables
- [ ] ⚠️ Test API at http://localhost:8000/docs

---

## 🧪 Test Your Database Connection

Run this to verify your NeonDB connection works:

```powershell
python -c "from app.database import engine; print('✅ Database connection successful!' if engine.connect() else '❌ Connection failed')"
```

Or run the setup checker:

```powershell
python setup_check.py
```

---

## 📈 Database Schema Diagram

```
┌─────────────────────────────────────────┐
│           flood_events                  │
├─────────────────────────────────────────┤
│ id              SERIAL PRIMARY KEY      │
│ location_name   VARCHAR NOT NULL        │
│ latitude        FLOAT NOT NULL          │
│ longitude       FLOAT NOT NULL          │
│ severity        VARCHAR(50) NOT NULL    │
│ risk_score      FLOAT NOT NULL          │
│ timestamp       TIMESTAMP WITH TZ       │
│ rainfall_mm     FLOAT                   │
│ elevation_m     FLOAT                   │
│ description     TEXT                    │
└─────────────────────────────────────────┘
                    ↑
                    │
                    │ (Optional Future)
                    │
┌─────────────────────────────────────────┐
│              users                      │
├─────────────────────────────────────────┤
│ id              SERIAL PRIMARY KEY      │
│ email           VARCHAR UNIQUE          │
│ username        VARCHAR UNIQUE          │
│ hashed_password VARCHAR                 │
│ is_active       INTEGER DEFAULT 1       │
│ is_admin        INTEGER DEFAULT 0       │
│ created_at      TIMESTAMP WITH TZ       │
└─────────────────────────────────────────┘
```

---

## 🎊 You're Ready!

Your NeonDB is configured and ready. Just run:

```powershell
python main.py
```

The application will:
1. ✅ Connect to your NeonDB
2. ✅ Create all required tables automatically
3. ✅ Start the API server at http://localhost:8000
4. ✅ Make API docs available at http://localhost:8000/docs

**No manual database setup needed!** 🚀

---

## 🆘 Troubleshooting

### "Connection Failed" Error?
- Check your NeonDB connection string in `.env`
- Verify `sslmode=require` is in the URL
- Ensure your NeonDB project is not paused (it auto-pauses after inactivity)
- Wake it up by visiting: https://console.neon.tech

### Tables Not Created?
- Make sure `init_db()` is called in `main.py`
- Check server logs for errors
- Verify NeonDB user has CREATE TABLE permissions

### Can't Connect from Python?
```powershell
pip install psycopg2-binary sqlalchemy --upgrade
```

---

**Your NeonDB setup is complete and ready to use!** 🎉
