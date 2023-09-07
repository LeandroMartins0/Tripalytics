from flask import jsonify
from flask_restful import Resource

# Import your session and helper functions
from app.database.session import SessionLocal as Session
from app.utils.query_helpers import (
    weekly_average_for_bounding_box,
    weekly_average_by_region,
    regions_for_datasource,
    most_recent_datasource_for_top_regions,
    total_records_in_database,
    select_all_records
)

# ===============================
# Resource Definitions
# ===============================
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

