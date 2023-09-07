from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Replace DATABASE_URL with your actual database connection URL
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/tripalytics"

# Create a SQLAlchemy engine for the database connection
engine = create_engine(DATABASE_URL)

# Create a session factory using SQLAlchemy's sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database schema by creating tables defined in the Base class.

    This function creates the necessary database tables based on the models defined in the Base class.
    It should be called when setting up the application or initializing the database.
    """
    Base.metadata.create_all(bind=engine)
