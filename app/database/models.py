"""
models.py

Provides Object-Relational Mapping (ORM) models for the database.

Modules:
- datetime: Provides date and time functionalities.
- sqlalchemy: ORM for database interactions.
"""

# -------------------------
# System imports
# -------------------------
from datetime import datetime

# -------------------------
# Third-party imports
# -------------------------
from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    DateTime, 
    Text, 
    update,
    exc
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# -------------------------
# Define the declarative base
# -------------------------
Base = declarative_base()

# -------------------------
# ORM Models
# -------------------------
class Trip(Base):
    """ 
    ORM Model for Trip.
    
    Represents a trip record in the database. 
    """
    __tablename__ = "trips"

    # Attributes / Columns
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    origin_coord = Column(String, index=True)
    destination_coord = Column(String, index=True)
    datetime = Column(DateTime, index=True)
    datasource = Column(String, index=True)

    # Methods
    def serialize(self):
        """Converts object attributes into a dictionary."""
        return {
            "id": self.id,
            "region": self.region,
            "origin_coord": self.origin_coord,
            "destination_coord": self.destination_coord,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "datasource": self.datasource
        }

    @staticmethod
    def create_trip(session, trip_data):
        """Creates and saves a new trip to the database."""
        try:
            new_trip = Trip(**trip_data)
            session.add(new_trip)
            session.commit()
            return new_trip.id
        except exc.SQLAlchemyError:
            session.rollback()
            return None


class IngestionLog(Base):
    """ 
    ORM Model for IngestionLog.
    
    Represents a log entry for data ingestion in the database. 
    """
    __tablename__ = "ingestion_log"

    # Attributes / Columns
    id = Column(Integer, primary_key=True, index=True)
    records_added = Column(Integer, index=True)
    status = Column(Text, index=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    # Methods
    @staticmethod
    def create_log_entry(session, log_data):
        """Creates and saves a new log entry to the database."""
        try:
            new_log_entry = IngestionLog(**log_data)
            session.add(new_log_entry)
            session.commit()
            return new_log_entry.id
        except exc.SQLAlchemyError:
            session.rollback()
            return None
