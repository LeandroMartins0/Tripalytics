from sqlalchemy import func, and_
from datetime import datetime
from app.database.models import Trip
from app.database.models import Trip
from sqlalchemy.orm import Session

def get_last_ingestion_status(session):
    """
    Returns the last ingestion date, records added, and if it was successful.
    """
    last_ingestion = session.query(Trip.datetime).order_by(Trip.datetime.desc()).first()
    if not last_ingestion:
        return None

    date_of_last_ingestion = last_ingestion[0]
    records_added_on_last_date = session.query(func.count(Trip.id)).filter(Trip.datetime == date_of_last_ingestion).scalar()
    
    return {
        "last_ingestion_date": date_of_last_ingestion.strftime('%Y-%m-%d'),
        "records_added": records_added_on_last_date,
        "success": True  # Assuming it's always successful for now.
    }

def weekly_average_for_bounding_box(session, x1, y1, x2, y2):
    results = session.query(
        func.date_trunc('week', Trip.datetime).label('week_start'),
        func.count(Trip.id)
    ).filter(
        and_(
            Trip.origin_coord.between(f"POINT ({x1} {y1})", f"POINT ({x2} {y2})"),
            Trip.destination_coord.between(f"POINT ({x1} {y1})", f"POINT ({x2} {y2})")
        )
    ).group_by(func.date_trunc('week', Trip.datetime)).all()
    
    return [{"week": r[0].strftime('%Y-%m-%d'), "count": r[1]} for r in results]

def weekly_average_by_region(session, region):
    results = session.query(
        func.date_trunc('week', Trip.datetime).label('week_start'),
        func.count(Trip.id)
    ).filter(Trip.region == region).group_by(func.date_trunc('week', Trip.datetime)).all()
    
    return [{"week": r[0].strftime('%Y-%m-%d'), "count": r[1]} for r in results]


def regions_for_datasource(session, datasource):
    results = session.query(Trip.region).filter(Trip.datasource == datasource).distinct().all()
    return [r[0] for r in results]

def total_records_in_database(session: Session):
    return session.query(Trip).count()

def select_all_records(session: Session):
    return session.query(Trip).all()

def most_recent_datasource_for_top_regions(session):
    # Identificar as duas regiões com mais viagens
    top_regions = session.query(Trip.region, func.count(Trip.id)).group_by(Trip.region).order_by(func.count(Trip.id).desc()).limit(2).all()
    regions = [r[0] for r in top_regions]

    # Identificar a fonte de dados mais recente para essas regiões
    most_recent_source = session.query(Trip.region, Trip.datasource, func.max(Trip.datetime).label('max_datetime')).filter(Trip.region.in_(regions)).group_by(Trip.region, Trip.datasource).all()
    
    result = {}
    for region, datasource, max_datetime in most_recent_source:
        if region not in result or max_datetime > result[region]['datetime']:
            result[region] = {'datasource': datasource, 'datetime': max_datetime}
    
    return result


