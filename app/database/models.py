from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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
