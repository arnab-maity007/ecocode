"""
Setup script to help initialize the Flood Forecaster backend.
Run this after installing dependencies and configuring .env
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def check_env_file():
    """Check if .env file exists."""
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        print("   Please copy .env.example to .env and configure it")
        print("   Command: copy .env.example .env")
        return False
    print("✅ .env file found")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2",
        "pydantic",
        "httpx",
        "python-jose",
        "passlib"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not installed")
    
    if missing:
        print("\n⚠️  Missing packages. Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def check_database_config():
    """Check if database configuration is set."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv("DATABASE_URL")
        if not db_url or db_url == "postgresql://username:password@localhost:5432/flood_forecaster":
            print("⚠️  DATABASE_URL not configured in .env")
            print("   Please update DATABASE_URL with your PostgreSQL credentials")
            return False
        
        print("✅ DATABASE_URL configured")
        
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not api_key or api_key == "your_openweathermap_api_key_here":
            print("⚠️  OPENWEATHERMAP_API_KEY not configured in .env")
            print("   Get free API key at: https://openweathermap.org/api")
            return False
        
        print("✅ OPENWEATHERMAP_API_KEY configured")
        
        secret = os.getenv("SECRET_KEY")
        if not secret or secret == "your_secret_key_here_generate_with_openssl_rand_hex_32":
            print("⚠️  SECRET_KEY not configured in .env")
            print("   Generate with: python -c \"import secrets; print(secrets.token_hex(32))\"")
            return False
        
        print("✅ SECRET_KEY configured")
        
        return True
        
    except ImportError:
        print("⚠️  python-dotenv not installed")
        return False


def check_database_connection():
    """Test database connection."""
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure PostgreSQL is running and DATABASE_URL is correct")
        return False


def initialize_database():
    """Initialize database tables."""
    try:
        from app.database import init_db
        init_db()
        print("✅ Database tables initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("🌊 Hyperlocal Urban Flood Forecaster - Setup Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        (".env File", check_env_file),
        ("Database Config", check_database_config),
        ("Database Connection", check_database_connection),
        ("Database Initialization", initialize_database),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        results.append(check_func())
        print()
    
    print("=" * 60)
    if all(results):
        print("✅ All checks passed! Your backend is ready to run.")
        print()
        print("🚀 Start the server with:")
        print("   python main.py")
        print("   or")
        print("   uvicorn main:app --reload")
        print()
        print("📚 API Documentation will be available at:")
        print("   http://localhost:8000/docs")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("📖 See README.md or QUICKSTART.md for detailed instructions")
    print("=" * 60)


if __name__ == "__main__":
    main()
