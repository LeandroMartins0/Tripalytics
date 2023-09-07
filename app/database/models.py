# System imports
from datetime import datetime

# Third-party imports
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

# Define the declarative base
Base = declarative_base()


# ORM Model for Trip
class Trip(Base):
    """
    Represents a trip record in the database.

    Attributes:
        id (int): Primary key for the trip.
        region (str): Name of the region.
        origin_coord (str): Coordinate of the origin point.
        destination_coord (str): Coordinate of the destination point.
        datetime (datetime): Date and time of the trip.
        datasource (str): Source of the trip data.
    """
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    origin_coord = Column(String, index=True)
    destination_coord = Column(String, index=True)
    datetime = Column(DateTime, index=True)
    datasource = Column(String, index=True)

    def serialize(self):
        """
        Serialize the Trip object to a dictionary.

        Returns:
            dict: A dictionary containing serialized trip data.
        """
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
        """
        Create a new Trip record.

        Args:
            session (Session): SQLAlchemy session.
            trip_data (dict): Data for creating a new trip.

        Returns:
            int: The ID of the newly created trip, or None if there was an error.
        """
        try:
            new_trip = Trip(**trip_data)
            session.add(new_trip)
            session.commit()
            return new_trip.id
        except SQLAlchemyError as e:
            session.rollback()
            return None


# ORM Model for IngestionLog
class IngestionLog(Base):
    """
    Represents a log entry for data ingestion.

    Attributes:
        id (int): Primary key for the log entry.
        records_added (int): Number of records added during ingestion.
        status (str): Status of the ingestion (e.g., success, error).
        timestamp (datetime): Timestamp of the log entry.
    """
    __tablename__ = "ingestion_log"
    
    id = Column(Integer, primary_key=True, index=True)
    records_added = Column(Integer, index=True)
    status = Column(Text, index=True)
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create_log_entry(session, log_data):
        """
        Create a new IngestionLog entry.

        Args:
            session (Session): SQLAlchemy session.
            log_data (dict): Data for creating a new log entry.

        Returns:
            int: The ID of the newly created log entry, or None if there was an error.
        """
        try:
            new_log_entry = IngestionLog(**log_data)
            session.add(new_log_entry)
            session.commit()
            return new_log_entry.id
        except SQLAlchemyError as e:
            session.rollback()
            return None
