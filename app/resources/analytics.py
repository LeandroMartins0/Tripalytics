"""
analytics.py

Provides RESTful resource endpoints for fetching analytics from the trip database.

Modules:
- flask: Used to create the API and handle request/response.
- flask_restful: Extension for Flask to easily build REST APIs.
- app.database.session: Provides database session functionalities.
- app.utils.query_helpers: Houses helper functions for querying the database.
"""

# -------------------------
# Imports
# -------------------------
from flask import jsonify
from flask_restful import Resource
from app.database.session import SessionLocal as Session
from app.utils.query_helpers import (
    weekly_average_for_bounding_box,
    weekly_average_by_region,
    regions_for_datasource,
    most_recent_datasource_for_top_regions,
    total_records_in_database,
    select_all_records
)

# -------------------------
# Resource Definitions
# -------------------------
class WeeklyAverage(Resource):
    """
    Resource for fetching the weekly average of trips within a bounding box.
    """
    def get(self, x1, y1, x2, y2):
        with Session() as session:
            result = weekly_average_for_bounding_box(session, x1, y1, x2, y2)
        return jsonify(result)


class WeeklyAverageByRegion(Resource):
    """
    Resource for fetching the weekly average of trips by region.
    """
    def get(self, region):
        with Session() as session:
            result = weekly_average_by_region(session, region)
        return jsonify(result)


class DataSourceRegions(Resource):
    """
    Resource for retrieving the regions associated with a specific data source.
    """
    def get(self, datasource):
        with Session() as session:
            regions = regions_for_datasource(session, datasource)
        return jsonify(regions)


class MostRecentDataSourceForTopRegions(Resource):
    """
    Resource to fetch the most recent data source for the top regions.
    """
    def get(self):
        with Session() as session:
            source = most_recent_datasource_for_top_regions(session)
        return jsonify(source)


class TotalRecords(Resource):
    """
    Resource for fetching the total number of records in the database.
    """
    def get(self):
        with Session() as session:
            total_records = total_records_in_database(session)
        return jsonify({"total_records": total_records})


class SelectAllRecords(Resource):
    """
    Resource to fetch all records from the database.
    """
    def get(self):
        with Session() as session:
            all_records = select_all_records(session)
        return jsonify([record.serialize() for record in all_records])
