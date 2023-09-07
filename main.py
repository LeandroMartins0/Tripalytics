# main.py

from app.database.session import SessionLocal as Session, engine
from app.database.models import Base, Trip
from app.utils.data_ingestion import ingest_csv_data, group_trips_by_hour

def setup_database():
    # Create tables in the database
    Base.metadata.create_all(bind=engine)

def main():
    setup_database()

    # Ingest data from the CSV to the database
    ingest_csv_data('./data/trips.csv')

    # Call the function to group trips (optional, only if you want to see the results now)
    grouped_data = group_trips_by_hour()
    print(grouped_data)  # Again, you can format or limit the output if it's too much

if __name__ == "__main__":
    main()
