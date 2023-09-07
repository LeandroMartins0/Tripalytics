# Standard library imports
from flask import Flask
from flask_restful import Api

# Local application imports
from app.database.session import engine
from app.database.models import Base
from app.utils.data_ingestion import ingest_csv_data, group_trips_by_hour
from app.resources.ingestion import IngestionStatus
from app.resources.analytics import (
    WeeklyAverage,
    WeeklyAverageByRegion,
    DataSourceRegions,
    MostRecentDataSourceForTopRegions,
    TotalRecords,
    SelectAllRecords
)


# ===============================
# App and API Initialization
# ===============================
app = Flask(__name__)
api = Api(app)


def setup_resources():
    """
    Associates API resources with their respective endpoints.
    """
    api.add_resource(IngestionStatus, "/ingestion_status")
    api.add_resource(WeeklyAverage, "/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>")
    api.add_resource(WeeklyAverageByRegion, "/weekly_average/<string:region>")
    api.add_resource(DataSourceRegions, "/datasource_regions/<string:datasource>")
    api.add_resource(MostRecentDataSourceForTopRegions, "/most_recent_datasource_for_top_regions")
    api.add_resource(TotalRecords, "/total_records")
    api.add_resource(SelectAllRecords, "/select_all_records")


def setup_database():
    """
    Initializes the database and creates necessary tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)


# ===============================
# Main Execution
# ===============================
def main():
    """
    The main execution function:
    - Sets up the database.
    - Ingests data.
    - Performs data aggregation.
    - Starts the Flask app.
    """
    setup_database()  # Initialize the database tables.
    setup_resources()  # Register API resources and routes.

    # Define the path to the CSV file containing the trip data.
    csv_file_path = "data/trips.csv"

    # Ingest and process the trip data from the CSV file.
    ingest_csv_data(csv_file_path)

    # Aggregate trip data by hour.
    group_trips_by_hour()

    # Run the Flask application.
    app.run(debug=True)


# If this script is executed directly, invoke the main function.
if __name__ == "__main__":
    main()
