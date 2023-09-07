from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app.database.session import SessionLocal as Session, engine
from app.database.models import Base, Trip
from app.utils.data_ingestion import ingest_csv_data, group_trips_by_hour
from app.utils.query_helpers import weekly_average_for_bounding_box, regions_for_datasource, most_recent_datasource_for_top_regions, get_last_ingestion_status, total_records_in_database, select_all_records, weekly_average_by_region
from app.database.models import Base, Trip, IngestionLog

app = Flask(__name__)
api = Api(app)

def setup_database():
    # Create tables in the database
    Base.metadata.create_all(bind=engine)

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
    
class WeeklyAverageByRegion(Resource):
    def get(self, region):
        with Session() as session:
            result = weekly_average_by_region(session, region)
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
    
class TotalRecords(Resource):
    def get(self):
        with Session() as session:
            total_records = total_records_in_database(session)
        return jsonify({"total_records": total_records})
    
class SelectAllRecords(Resource):
    def get(self):
        with Session() as session:
            all_records = select_all_records(session)
        return jsonify([record.serialize() for record in all_records])


# Adicionando os recursos à API
api.add_resource(IngestionStatus, "/ingestion_status")
api.add_resource(WeeklyAverage, "/weekly_average/<float:x1>/<float:y1>/<float:x2>/<float:y2>")
api.add_resource(WeeklyAverageByRegion, "/weekly_average/<string:region>")

api.add_resource(DataSourceRegions, "/datasource_regions/<string:datasource>")
api.add_resource(MostRecentDataSourceForTopRegions, "/most_recent_datasource_for_top_regions")
api.add_resource(TotalRecords, "/total_records")
api.add_resource(SelectAllRecords, "/select_all_records")

def main():
    setup_database()

    # Run the Flask app
    app.run(debug=True)

if __name__ == "__main__":
    main()
