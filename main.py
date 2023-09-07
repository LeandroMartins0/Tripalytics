# Standard library imports
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

# Local imports
from app.database.session import SessionLocal as Session, engine
from app.database.models import Base, Trip, IngestionLog
from app.utils.data_ingestion import ingest_csv_data, group_trips_by_hour
from app.utils.query_helpers import (
    weekly_average_for_bounding_box,
    regions_for_datasource,
    most_recent_datasource_for_top_regions,
    get_last_ingestion_status,
    total_records_in_database,
    select_all_records,
    weekly_average_by_region,
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

# ===============================
# Resource Definitions
# ===============================
# Note: For larger applications, consider moving these Resource classes into separate modules.

class IngestionStatus(Resource):
    """
    Provides information about the last data ingestion status.
    """
    def get(self):
        """
        Get the last data ingestion status.
        """
        with Session() as session:
            status = get_last_ingestion_status(session)
        if not status:
            return {"error": "No ingestion logs found."}, 404
        return jsonify(status)

class WeeklyAverage(Resource):
    """
    Calculates the weekly average of trips within a bounding box.
    """
    def get(self, x1, y1, x2, y2):
        """
        Calculate the weekly average of trips within a bounding box.

        Args:
            x1 (float): x-coordinate of the first point.
            y1 (float): y-coordinate of the first point.
            x2 (float): x-coordinate of the second point.
            y2 (float): y-coordinate of the second point.

        Returns:
            dict: Weekly average trip data.
        """
        with Session() as session:
            result = weekly_average_for_bounding_box(session, x1, y1, x2, y2)
            
        return jsonify(result)

class WeeklyAverageByRegion(Resource):
    """
    Calculates the weekly average of trips for a specific region.
    """
    def get(self, region):
        """
        Calculate the weekly average of trips for a specific region.

        Args:
            region (str): Name of the region.

        Returns:
            dict: Weekly average trip data for the region.
        """
        with Session() as session:
            result = weekly_average_by_region(session, region)
        return jsonify(result)

class DataSourceRegions(Resource):
    """
    Retrieves the regions associated with a specific data source.
    """
    def get(self, datasource):
        """
        Retrieve regions associated with a specific data source.

        Args:
            datasource (str): Name of the data source.

        Returns:
            dict: Regions associated with the data source.
        """
        with Session() as session:
            regions = regions_for_datasource(session, datasource)
        return jsonify(regions)

class MostRecentDataSourceForTopRegions(Resource):
    """
    Identifies the most recent data source for the top regions with the highest trip counts.
    """
    def get(self):
        """
        Identify the most recent data source for top regions.

        Returns:
            dict: The most recent data source for top regions.
        """
        with Session() as session:
            source = most_recent_datasource_for_top_regions(session)
        return jsonify(source)

class TotalRecords(Resource):
    """
    Retrieves the total number of records in the database.
    """
    def get(self):
        """
        Get the total number of records in the database.

        Returns:
            dict: Total number of records.
        """
        with Session() as session:
            total_records = total_records_in_database(session)
        return jsonify({"total_records": total_records})

class SelectAllRecords(Resource):
    """
    Retrieves all records from the database.
    """
    def get(self):
        """
        Get all records from the database.

        Returns:
            list: List of serialized records.
        """
        with Session() as session:
            all_records = select_all_records(session)
        return jsonify([record.serialize() for record in all_records])

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
