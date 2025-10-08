"""
Alembic configuration for database migrations.
Run this script to set up Alembic for your project.
"""

# To initialize Alembic:
# 1. Run: alembic init alembic
# 2. Update alembic/env.py to import your models
# 3. Update alembic.ini with your database URL (or use environment variable)
# 4. Generate migration: alembic revision --autogenerate -m "Initial migration"
# 5. Apply migration: alembic upgrade head

# Example alembic/env.py modification:
"""
from app.database import Base
from app import models  # Import all models

target_metadata = Base.metadata
"""

print("Alembic setup instructions:")
print("1. Run: alembic init alembic")
print("2. Update alembic/env.py with your models")
print("3. Generate migration: alembic revision --autogenerate -m 'Initial migration'")
print("4. Apply migration: alembic upgrade head")
