"""
query_helpers.py

Provides helper functions to query various information from the database.

Modules:
- sqlalchemy: ORM and query functionalities.
- datetime: Provides functionalities to work with dates and times.
- app.database.models: Contains ORM models for the database.
"""

# -------------------------
# Imports
# -------------------------
from sqlalchemy import func, and_
from datetime import datetime
from app.database.models import Trip
from sqlalchemy.orm import Session

# -------------------------
# Helper Functions
# -------------------------
def get_last_ingestion_status(session: Session):
    """
    Returns the last ingestion date, records added, and if it was successful.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the last ingestion date, records added, and success status.
              Example: {"last_ingestion_date": "2023-09-05", "records_added": 100, "success": True}
    """
    last_ingestion = session.query(Trip.datetime).order_by(Trip.datetime.desc()).first()
    if not last_ingestion:
        return None

    date_of_last_ingestion = last_ingestion[0]
    records_added_on_last_date = session.query(func.count(Trip.id)).filter(Trip.datetime == date_of_last_ingestion).scalar()
    
    return {
        "last_ingestion_date": date_of_last_ingestion.strftime('%Y-%m-%d'),
        "records_added": records_added_on_last_date,
        "success": True  # Assuming it's always successful for now.
    }

def weekly_average_for_bounding_box(session: Session, x1, y1, x2, y2):
    """
    Calculate the weekly average for trips within a bounding box.

    Args:
        session (Session): The SQLAlchemy session.
        x1 (float): The x-coordinate of the bottom-left corner of the bounding box.
        y1 (float): The y-coordinate of the bottom-left corner of the bounding box.
        x2 (float): The x-coordinate of the top-right corner of the bounding box.
        y2 (float): The y-coordinate of the top-right corner of the bounding box.

    Returns:
        list: A list of dictionaries containing the week start date and the count of trips for each week.
              Example: [{"week": "2023-09-05", "count": 42}, {"week": "2023-09-12", "count": 56}, ...]
    """
    results = session.query(
        func.date_trunc('week', Trip.datetime).label('week_start'),
        func.count(Trip.id)
    ).filter(
        and_(
            Trip.origin_coord.between(f"POINT ({x1} {y1})", f"POINT ({x2} {y2})"),
            Trip.destination_coord.between(f"POINT ({x1} {y1})", f"POINT ({x2} {y2})")
        )
    ).group_by(func.date_trunc('week', Trip.datetime)).all()
    
    return [{"week": r[0].strftime('%Y-%m-%d'), "count": r[1]} for r in results]

def weekly_average_by_region(session: Session, region: str):
    """
    Calculate the weekly average for trips within a specific region.

    Args:
        session (Session): The SQLAlchemy session.
        region (str): The region for which to calculate the weekly average.

    Returns:
        list: A list of dictionaries containing the week start date and the count of trips for each week.
              Example: [{"week": "2023-09-05", "count": 42}, {"week": "2023-09-12", "count": 56}, ...]
    """
    results = session.query(
        func.date_trunc('week', Trip.datetime).label('week_start'),
        func.count(Trip.id)
    ).filter(Trip.region == region).group_by(func.date_trunc('week', Trip.datetime)).all()
    
    return [{"week": r[0].strftime('%Y-%m-%d'), "count": r[1]} for r in results]

def regions_for_datasource(session: Session, datasource: str):
    """
    Get a list of regions for a specific datasource.

    Args:
        session (Session): The SQLAlchemy session.
        datasource (str): The datasource for which to retrieve regions.

    Returns:
        list: A list of regions associated with the specified datasource.
              Example: ["Hamburg", "Prague", "Turin", ...]
    """
    results = session.query(Trip.region).filter(Trip.datasource == datasource).distinct().all()
    return [r[0] for r in results]

def total_records_in_database(session: Session):
    """
    Get the total number of records in the database.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        int: The total number of records in the database.
    """
    return session.query(Trip).count()

def select_all_records(session: Session):
    """
    Select all records from the database.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        list: A list of Trip objects representing all records in the database.
    """
    return session.query(Trip).all()

def most_recent_datasource_for_top_regions(session: Session):
    """
    Get the most recent datasource for the top two regions with the most trips.

    Args:
        session (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the most recent datasource for the top regions.
              Example: {"Hamburg": {"datasource": "cheap_mobile", "datetime": "2023-09-05 10:23:45"}}
    """
    # Identify the two regions with the most trips
    top_regions = session.query(Trip.region, func.count(Trip.id)).group_by(Trip.region).order_by(func.count(Trip.id).desc()).limit(2).all()
    regions = [r[0] for r in top_regions]

    # Identify the most recent datasource for these regions
    most_recent_source = session.query(Trip.region, Trip.datasource, func.max(Trip.datetime).label('max_datetime')).filter(Trip.region.in_(regions)).group_by(Trip.region, Trip.datasource).all()
    
    result = {}
    for region, datasource, max_datetime in most_recent_source:
        if region not in result or max_datetime > result[region]['datetime']:
            result[region] = {'datasource': datasource, 'datetime': max_datetime}
    
    return result

# For testing and debbuging
# if __name__ == '__main__':
    # Sample code for testing
    # (You can write some test or demo code here if you want)