# /tripalytics/utils/data_ingestion.py

import csv
from datetime import datetime
from app.database.models import Trip
from app.database.session import SessionLocal as Session
from sqlalchemy import func, extract

def parse_csv_line(line):
    """
    Parse a line from the CSV into a Trip object.
    """
    region, origin_coord, destination_coord, date_time, datasource = line
    trip = Trip(
        region=region,
        origin_coord=origin_coord,
        destination_coord=destination_coord,
        datetime=datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S"),
        datasource=datasource
    )
    return trip

def ingest_csv_data(filename):
    """
    Ingest data from the CSV into the database.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        session = Session()
        try:
            for line in reader:
                trip = parse_csv_line(line)
                session.add(trip)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            session.close()


def group_trips_by_hour():
    """
    Group trips with similar origin, destination, and time of day.
    """
    session = Session()
    try:
        grouped_trips = session.query(
            Trip.origin_coord,
            Trip.destination_coord,
            extract('hour', Trip.datetime).label('hour'),
            func.count(Trip.id).label('trip_count')
        ).group_by(
            Trip.origin_coord,
            Trip.destination_coord,
            extract('hour', Trip.datetime)
        ).all()

        # The above query will give you results grouped by origin, destination, and hour
        return grouped_trips

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        session.close()
