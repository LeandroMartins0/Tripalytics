# Standard library imports
from flask import Flask
from flask_restful import Api

# Local imports
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

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# ===============================
# Database Initialization
# ===============================
def setup_database():
    """
    Sets up the database and creates necessary tables.
    """
    Base.metadata.create_all(bind=engine)

# Add resources to the API
api.add_resource(IngestionStatus, "/ingestion_status")
api.add_resource(WeeklyAverage, "/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>")
api.add_resource(WeeklyAverageByRegion, "/weekly_average/<string:region>")
api.add_resource(DataSourceRegions, "/datasource_regions/<string:datasource>")
api.add_resource(MostRecentDataSourceForTopRegions, "/most_recent_datasource_for_top_regions")
api.add_resource(TotalRecords, "/total_records")
api.add_resource(SelectAllRecords, "/select_all_records")


# ===============================
# Main Execution
# ===============================
def main():
    """
    Main function to set up the database, perform data ingestion, aggregation, and run the Flask app.
    """
    setup_database()

    # Path to the CSV file
    csv_file_path = "data/trips.csv"

    # Perform data ingestion from the CSV file
    ingest_csv_data(csv_file_path)

    # Perform data aggregation
    group_trips_by_hour()

    # Run the Flask app
    app.run(debug=True)

if __name__ == "__main__":
    main()
