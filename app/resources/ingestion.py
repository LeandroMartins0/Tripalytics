from flask_restful import Resource
from app.database.session import SessionLocal as Session
from app.utils.query_helpers import get_last_ingestion_status
from flask import jsonify



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