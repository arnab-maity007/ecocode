# 🎯 Getting Started Checklist

Follow this checklist to get your Flood Forecaster backend up and running!

## ✅ Pre-Setup Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] NeonDB account created at https://neon.tech
- [ ] Git installed (for version control)
- [ ] Code editor installed (VS Code recommended)
- [ ] OpenWeatherMap account created (free tier is fine)

## ✅ Initial Setup (First Time)

### 1. Environment Setup
- [ ] Open terminal/command prompt in project directory
- [ ] Run setup script:
  - Windows: `setup.bat`
  - Linux/Mac: `chmod +x setup.sh && ./setup.sh`
- [ ] Virtual environment created successfully
- [ ] All dependencies installed

### 2. Database Setup
- [ ] NeonDB account created at https://neon.tech
- [ ] New project created in NeonDB dashboard
- [ ] Connection string copied from NeonDB
- [ ] Connection string includes `?sslmode=require`
- [ ] ✅ **No need to create tables manually** - they auto-create!

### 3. API Keys Setup
- [ ] Get OpenWeatherMap API key from https://openweathermap.org/api
- [ ] (Optional) Get Google Elevation API key
- [ ] Generate SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`

### 4. Configuration
- [ ] Copy `.env.example` to `.env`: `copy .env.example .env` (Windows) or `cp .env.example .env` (Linux/Mac)
- [ ] Edit `.env` file with:
  - [ ] Your NeonDB connection string (DATABASE_URL)
  - [ ] Your OPENWEATHERMAP_API_KEY
  - [ ] Your generated SECRET_KEY
  - [ ] Your ALLOWED_ORIGINS (your frontend URL)

### 5. Validation
- [ ] Run setup check: `python setup_check.py`
- [ ] All checks pass ✅

## ✅ Running the Server

### Development Mode
- [ ] Activate virtual environment:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- [ ] Start server: `python main.py` or `uvicorn main:app --reload`
- [ ] Server starts without errors
- [ ] Visit http://localhost:8000 - see welcome message
- [ ] Visit http://localhost:8000/docs - see API documentation

## ✅ Testing the API

### Basic Health Check
- [ ] Open browser to http://localhost:8000/health
- [ ] Response shows: `{"status": "healthy"}`

### Test Endpoints
- [ ] Test POST /api/v1/floods/ (create event)
- [ ] Test GET /api/v1/floods/ (list events)
- [ ] Test POST /api/v1/floods/calculate-risk (calculate risk)
- [ ] Test GET /api/v1/floods/nearby/ (find nearby events)

### Using API Documentation
- [ ] Open http://localhost:8000/docs
- [ ] Try "POST /api/v1/floods/" endpoint
- [ ] Click "Try it out"
- [ ] Enter sample data:
  ```json
  {
    "location_name": "Test Street",
    "latitude": 40.7128,
    "longitude": -74.0060
  }
  ```
- [ ] Click "Execute"
- [ ] See 201 response with flood event data

## ✅ Frontend Integration

### CORS Setup
- [ ] Update ALLOWED_ORIGINS in `.env` with your frontend URL
- [ ] Restart server
- [ ] Test API from frontend (no CORS errors)

### Test API Call from Frontend
```javascript
// Test this code in browser console
fetch('http://localhost:8000/api/v1/floods/')
  .then(res => res.json())
  .then(data => console.log(data));
```
- [ ] API call succeeds
- [ ] No CORS errors in browser console
- [ ] Data returned successfully

## ✅ Optional Features

### User Authentication
- [ ] Test POST /api/v1/auth/register (create user)
- [ ] Test POST /api/v1/auth/login (get JWT token)
- [ ] Test GET /api/v1/auth/me (with Bearer token)

### Database Migrations (Optional)
- [ ] Install Alembic: `pip install alembic`
- [ ] Initialize: `alembic init alembic`
- [ ] Configure alembic/env.py
- [ ] Create migration: `alembic revision --autogenerate -m "Initial"`
- [ ] Apply migration: `alembic upgrade head`

## ✅ Production Readiness

### Security
- [ ] Set DEBUG=False in `.env`
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Add input sanitization

### Performance
- [ ] Configure database connection pool
- [ ] Add Redis for caching (optional)
- [ ] Use multiple workers: `uvicorn main:app --workers 4`
- [ ] Set up CDN for static assets

### Monitoring
- [ ] Add logging configuration
- [ ] Set up error tracking (Sentry)
- [ ] Configure health check endpoint monitoring
- [ ] Set up database backup schedule

### Deployment
- [ ] Choose hosting platform (AWS, Heroku, DigitalOcean, etc.)
- [ ] Set up CI/CD pipeline
- [ ] Configure environment variables on hosting
- [ ] Deploy and test
- [ ] Set up domain and SSL certificate

## 🎉 Success Criteria

You're ready to go when:
- ✅ Server starts without errors
- ✅ API documentation loads at /docs
- ✅ Can create flood events via API
- ✅ Can retrieve flood events
- ✅ Risk calculation works correctly
- ✅ Frontend can communicate with backend
- ✅ Database stores data correctly
- ✅ All endpoints return expected responses

## 📚 Quick Reference

### Common Commands
```bash
# Start server
python main.py
uvicorn main:app --reload

# Run tests
pytest tests/

# Check setup
python setup_check.py

# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Database shell
psql -U postgres -d flood_forecaster
```

### Important URLs
- API Root: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### File Locations
- Main app: `main.py`
- Configuration: `app/config.py`
- Models: `app/models.py`
- API routes: `app/routers/`
- Risk logic: `app/services/flood_risk.py`
- Environment: `.env`

## 🆘 Troubleshooting

### Server won't start
- Check Python version: `python --version`
- Check all dependencies installed: `pip list`
- Check .env file exists and configured
- Check database connection

### Database errors
- Verify NeonDB connection string in .env
- Check `?sslmode=require` is in the URL
- Ensure NeonDB project is active (not paused)
- Wake paused projects at https://console.neon.tech

### API errors
- Check API key is valid
- Verify endpoint URL is correct
- Check request payload format
- Review server logs for errors

### CORS errors
- Update ALLOWED_ORIGINS in .env
- Restart server after changes
- Check frontend uses correct API URL

## 📞 Need Help?

1. ✅ Read README.md for detailed documentation
2. ✅ Check QUICKSTART.md for quick setup
3. ✅ Review API_EXAMPLES.md for usage examples
4. ✅ Run `python setup_check.py` for diagnostics
5. ✅ Check FastAPI docs: https://fastapi.tiangolo.com/

---

**Happy Coding! 🚀 Build amazing flood prediction features!**
