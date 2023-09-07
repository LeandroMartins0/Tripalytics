"""
session.py

Manages the database session configuration and provides utility functions
related to database initialization.

Modules:
- SQLAlchemy: ORM for database interactions.
- .models: Imports the Base class which contains the defined database models.
"""

# -------------------------
# Imports
# -------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# -------------------------
# Constants
# -------------------------

# The database connection URL. Replace with your actual database connection URL.
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/tripalytics"

# -------------------------
# Database Engine Configuration
# -------------------------
engine = create_engine(DATABASE_URL)

# Create a session factory using SQLAlchemy's sessionmaker. 
# This session factory will be used to create individual database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------
# Utility Functions
# -------------------------
def init_db():
    """
    Initialize the database schema by creating tables defined in the Base class.

    This function creates the necessary database tables based on the models defined in the Base class.
    It should be called when setting up the application or initializing the database.
    """
    Base.metadata.create_all(bind=engine)
