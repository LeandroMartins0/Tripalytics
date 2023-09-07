from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app.database.session import SessionLocal as Session, engine
from app.database.models import Base, Trip
from app.utils.data_ingestion import ingest_csv_data, group_trips_by_hour
from app.utils.query_helpers import weekly_average_for_bounding_box, regions_for_datasource, most_recent_datasource_for_top_regions, get_last_ingestion_status
from app.database.models import Base, Trip, IngestionLog

app = Flask(__name__)
api = Api(app)

def setup_database():
    # Create tables in the database
    Base.metadata.create_all(bind=engine)

# class IngestionStatus(Resource):
#     def get(self):
#         with Session() as session:
#             last_ingestion = session.query(IngestionLog).order_by(IngestionLog.timestamp.desc()).first()

#             # Se não encontrarmos nenhum registro, retornamos um erro
#             if not last_ingestion:
#                 return {"error": "No ingestion logs found."}, 404

#             # Se tudo correu bem, retornamos o status da última ingestão
#             status = {
#                 "last_ingestion_date": str(last_ingestion.timestamp),
#                 "records_added": last_ingestion.records_added,
#                 "success": "success" in last_ingestion.status
#             }
#         return jsonify(status)

class IngestionStatus(Resource):
    def get(self):
        with Session() as session:
            status = get_last_ingestion_status(session)
        if not status:
            return {"error": "No ingestion logs found."}, 404
        return jsonify(status)



class WeeklyAverage(Resource):
    def get(self, x1, y1, x2, y2):
        with Session() as session:
            result = weekly_average_for_bounding_box(session, x1, y1, x2, y2)
        return jsonify(result)

class DataSourceRegions(Resource):
    def get(self, datasource):
        with Session() as session:
            regions = regions_for_datasource(session, datasource)
        return jsonify(regions)

class MostRecentDataSourceForTopRegions(Resource):
    def get(self):
        with Session() as session:
            source = most_recent_datasource_for_top_regions(session)
        return jsonify(source)

# Adicionando os recursos à API
api.add_resource(IngestionStatus, "/ingestion_status")
api.add_resource(WeeklyAverage, "/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>")
api.add_resource(DataSourceRegions, "/datasource_regions/<string:datasource>")
api.add_resource(MostRecentDataSourceForTopRegions, "/most_recent_datasource_for_top_regions")

def main():
    setup_database()

    # Run the Flask app
    app.run(debug=True)

if __name__ == "__main__":
    main()
