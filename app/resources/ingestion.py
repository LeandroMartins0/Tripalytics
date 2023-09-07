"""
ingestion.py

Provides a RESTful resource endpoint for fetching the status of the last data ingestion 
from the trip database.

Modules:
- flask: Used for handling request/response.
- flask_restful: Extension for Flask to build REST APIs.
- app.database.session: Provides database session functionalities.
- app.utils.query_helpers: Houses helper functions for querying the database.
"""

# -------------------------
# Imports
# -------------------------
from flask_restful import Resource
from flask import jsonify
from app.database.session import SessionLocal as Session
from app.utils.query_helpers import get_last_ingestion_status

# -------------------------
# Resource Definition
# -------------------------
class IngestionStatus(Resource):
    """
    Resource for fetching the status of the last data ingestion.
    """
    
    def get(self):
        """
        Retrieve the status of the last data ingestion. If no ingestion logs are found, 
        an error is returned with a 404 status code.
        
        Returns:
            dict: A dictionary with the status of the last data ingestion.
        """
        with Session() as session:
            status = get_last_ingestion_status(session)
            
        if not status:
            return {"error": "No ingestion logs found."}, 404
            
        return jsonify(status)
