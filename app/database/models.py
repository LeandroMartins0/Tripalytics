from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    origin_coord = Column(String, index=True)
    destination_coord = Column(String, index=True)
    datetime = Column(DateTime, index=True)
    datasource = Column(String, index=True)
