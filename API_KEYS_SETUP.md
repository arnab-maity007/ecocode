# API Keys Setup Guide

This application requires several API keys to function fully. Follow these instructions to obtain and configure them.

## Required API Keys

### 1. Google Maps API Key
**Required for:** Interactive map showing India with weather risk overlay

**How to get it:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Geocoding API
   - Places API (optional, for better location search)
4. Go to "Credentials" and create an API key
5. Restrict the API key (recommended):
   - Application restrictions: HTTP referrers
   - Add: `http://localhost:3000/*`
   - API restrictions: Select the Maps APIs you enabled

**Where to add it:**
- Frontend: `.env.local` → `REACT_APP_GOOGLE_MAPS_API_KEY=your_key_here`

**Free tier:** $200 credit per month (enough for development)

---

### 2. Gemini AI API Key
**Required for:** AI-powered route verdict system

**How to get it:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Select your Google Cloud project
5. Copy the generated API key

**Where to add it:**
- Backend: `.env` → `GEMINI_API_KEY=your_key_here`
- Frontend (optional): `.env.local` → `REACT_APP_GEMINI_API_KEY=your_key_here`

**Free tier:** 60 requests per minute, generous daily quota

---

### 3. OpenWeatherMap API Key (Already Configured)
**Required for:** Weather data and flood risk calculations

**Current key:** `0d155cf64ebcf8ba3a1efca8f23732e1` (already in `.env`)

**If you need your own:**
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to "API keys" section
4. Copy your API key

**Where to add it:**
- Backend: `.env` → `OPENWEATHERMAP_API_KEY=your_key_here`

**Free tier:** 1,000 calls/day

---

### 4. NeonDB Connection String (Optional)
**Required for:** Database persistence (currently using mock data fallback)

**Current status:** The database credentials in `.env` are outdated.

**If you want to set up a new database:**
1. Go to [Neon](https://neon.tech/)
2. Create a free account
3. Create a new project
4. Copy the connection string
5. Update `.env` → `DATABASE_URL=your_connection_string`

**Where to add it:**
- Backend: `.env` → `DATABASE_URL=postgresql://...`

**Free tier:** 512MB storage, 3 compute hours/day

---

## Configuration Files

### Backend Configuration (`.env`)
```env
# Database Configuration
DATABASE_URL=postgresql://your_neondb_connection_string

# API Keys
OPENWEATHERMAP_API_KEY= yous_api_key
GOOGLE_ELEVATION_API_KEY=your_google_elevation_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# JWT Configuration
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
APP_NAME=Hyperlocal Urban Flood Forecaster
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Configuration (`.env.local`)
```env
# Google Maps API Key
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Gemini AI API Key (optional - backend handles this)
REACT_APP_GEMINI_API_KEY=your_gemini_api_key_here

# Backend API URL
REACT_APP_API_URL=http://localhost:8000
```

---

## Quick Start Order

1. **Get Google Maps API Key** (highest priority)
   - Without this, the map won't load at all
   - Add to `.env.local`

2. **Get Gemini AI API Key** (high priority)
   - Without this, route verdict will use mock data
   - Add to `.env`

3. **OpenWeatherMap** (already configured)
   - Current key works but has rate limits
   - Consider getting your own for production

4. **NeonDB** (optional)
   - App works with mock data fallback
   - Only needed for data persistence

---

## Testing Without API Keys

The application has fallback mechanisms:

- **Google Maps:** Shows placeholder, app won't crash
- **Gemini AI:** Returns realistic mock data
- **Weather API:** Uses existing key (limited)
- **Database:** Mock data mode (no persistence)

You can test the basic functionality without any API keys, but for full features:
- **Minimum required:** Google Maps API Key
- **Recommended:** Google Maps + Gemini AI

---

## Security Notes

⚠️ **Important:**
- Never commit API keys to Git
- `.env` and `.env.local` are in `.gitignore`
- For production, use environment variables
- Restrict API keys to specific domains/IPs
- Monitor usage in respective consoles

---

## Cost Estimates

All services have generous free tiers:

| Service | Free Tier | Est. Monthly Cost (Dev) |
|---------|-----------|-------------------------|
| Google Maps | $200 credit | $0 (within free tier) |
| Gemini AI | 60 req/min | $0 (within free tier) |
| OpenWeatherMap | 1000 calls/day | $0 (within free tier) |
| NeonDB | 512MB storage | $0 (within free tier) |

**Total:** $0/month for development

---

## Troubleshooting

### Google Maps not showing
- Check browser console for API key errors
- Verify API is enabled in Google Cloud Console
- Check HTTP referrer restrictions

### Route Verdict not working
- Check backend logs for Gemini API errors
- Verify API key in `.env`
- Fallback to mock data should work automatically

### Weather data not updating
- Check OpenWeatherMap API key validity
- Free tier has rate limits (1000/day)
- Consider caching responses

---

## Support Links

- [Google Maps API Docs](https://developers.google.com/maps/documentation)
- [Gemini AI Docs](https://ai.google.dev/docs)
- [OpenWeatherMap Docs](https://openweathermap.org/api)
- [Neon Docs](https://neon.tech/docs/introduction)
