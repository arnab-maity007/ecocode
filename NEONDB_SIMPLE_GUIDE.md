# ✅ What You Need for NeonDB Setup - SIMPLE GUIDE

## 🎯 You're Almost Ready! Just 3 Things:

### ✅ **ALREADY DONE:**
1. ✅ Python packages installed
2. ✅ Virtual environment created
3. ✅ SECRET_KEY configured in `.env`
4. ✅ NeonDB connection string in `.env`
5. ✅ OpenWeatherMap API key in `.env`

### 🚀 **WHAT TO DO NOW:**

## Just Run This Command:

```powershell
python main.py
```

**That's it!** Your application will:
1. ✅ Connect to your NeonDB
2. ✅ Automatically create these 2 tables:
   - `flood_events` - stores all flood predictions
   - `users` - stores user accounts (optional)
3. ✅ Start the API server at http://localhost:8000

---

## 📊 What Tables Get Created Automatically

### Table 1: `flood_events`
Stores all flood risk predictions and events:
- Location details (name, latitude, longitude)
- Risk assessment (score 0-100, severity level)
- Weather data (rainfall, elevation)
- Timestamps

### Table 2: `users` (Optional)
Stores user accounts for authentication:
- Email, username, password (hashed)
- Active/inactive status
- Admin privileges

---

## 🔍 Verify Everything Works

### Step 1: Run the server
```powershell
python main.py
```

You should see:
```
🚀 Starting Hyperlocal Urban Flood Forecaster API...
📊 Initializing database...
✅ Database initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open your browser
Go to: **http://localhost:8000/docs**

You'll see the interactive API documentation with all endpoints!

### Step 3: Test an endpoint
Click on **POST /api/v1/floods/** → **Try it out**

Use this sample data:
```json
{
  "location_name": "Test Street",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "description": "Test location"
}
```

Click **Execute** - it will:
1. Fetch real rainfall data from OpenWeatherMap
2. Calculate elevation
3. Compute risk score (0-100)
4. Determine severity (Low/Medium/High/Critical)
5. Save to your NeonDB database
6. Return the complete flood event with all data

---

## 🎓 What Happens Behind the Scenes

```
When you run: python main.py

1. App connects to NeonDB ✅
2. Checks if tables exist
3. If not, creates them automatically:
   - flood_events table
   - users table
4. Starts FastAPI server
5. Ready to accept requests!
```

---

## ❌ What You DON'T Need

- ❌ Don't need to install PostgreSQL locally
- ❌ Don't need to run SQL commands manually
- ❌ Don't need to create tables yourself
- ❌ Don't need database migrations (for MVP)
- ❌ Don't need to configure PostGIS
- ❌ Don't need pgAdmin or any database tools

**Everything is automated!** ✨

---

## 📱 Your Backend Provides These APIs

Once running, your React frontend can call:

### Create Flood Event
```javascript
POST http://localhost:8000/api/v1/floods/
{
  "location_name": "Main Street",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### Get All Flood Events
```javascript
GET http://localhost:8000/api/v1/floods/
```

### Calculate Risk (without saving)
```javascript
POST http://localhost:8000/api/v1/floods/calculate-risk
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### Find Nearby Events
```javascript
GET http://localhost:8000/api/v1/floods/nearby/?latitude=40.7128&longitude=-74.0060&radius_km=5
```

---

## 🎊 Summary

**Your backend is 100% ready!**

Your `.env` file has:
- ✅ NeonDB connection string
- ✅ OpenWeatherMap API key
- ✅ SECRET_KEY

**Just run:**
```powershell
python main.py
```

**Then visit:**
- API Docs: http://localhost:8000/docs
- API Root: http://localhost:8000
- Health Check: http://localhost:8000/health

**Start building your React frontend - your backend is live!** 🚀

---

## 🆘 If Something Goes Wrong

### NeonDB Connection Error?
1. Check your `.env` file has the correct NeonDB URL
2. Make sure it ends with `?sslmode=require`
3. Visit https://console.neon.tech and wake up your project if it's paused

### OpenWeatherMap Error?
1. Verify your API key in `.env`
2. Check you've activated the key (sometimes takes 10 minutes)
3. Ensure you're using the "Current Weather Data" API

### Run This to Diagnose:
```powershell
python setup_check.py
```

It will check everything and tell you what's wrong!

---

**You don't need to do anything in NeonDB manually. Just run `python main.py` and you're done!** 🎉
