import json
import datetime
import decimal

from flask import request, Blueprint, Response, jsonify
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from bicycles import db
from .models import BicycleCount

api_bp = Blueprint("api", __name__)  # url prefix of /api set in init


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


sql_query = ("SELECT b.*, w.prcp, w.tavg, w.tmax, w.tmin FROM bicycle_count b LEFT JOIN weather "
             "w ON DATE(b.setdate) = w.date")


@api_bp.route("counts/<record_num>", methods=['GET', 'PUT', 'DELETE'])
def count(record_num, sql_query=sql_query):
    '''Get, edit, or delete one bicycle count record.'''
    if request.method == 'GET':
        sql_query += " WHERE recordnum = " + record_num
        result = db.session.execute(text(sql_query)).fetchall()
        if len(result):
            serialized = json.dumps([dict(r) for r in result], default=alchemyencoder)
            return Response(serialized, mimetype='application/json')
        else:
            return jsonify({"error": "No matching record found."})

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

    return


@api_bp.route("counts", methods=['GET', 'POST'])
def counts(sql_query=sql_query):
    '''Return all bicycle counts according to various criteria or add new bicycle count record.'''
    if request.method == 'GET':
        facility = request.args.get("facility")
        precipitation = request.args.get("precipitation")
        
        where_clauses = []

        if precipitation:
            try:
                precipitation = float(precipitation)
            except ValueError:
                return jsonify({'error': 'Precipitation value must be an number, with optional '
                                'decimal points.'})
            
            where_clauses.append(f"w.prcp >= {precipitation}")
        
        if facility:
            facility_types = ['Multiuse Trail',
                              'Sidepath',
                              'Striped Shoulder',
                              'Bike Lane',
                              'Mixed Traffic',
                              'Buffered Bike Lane',
                              'Sharrow']
            if facility not in facility_types:
                return jsonify({'error': 'Facility must be one of ' + 
                                         ', '.join(facility_types[:-1]) + 
                                         ', or ' + facility_types[-1] + '.'})
            where_clauses.append(f"b.bikepedfac = '{facility}'")

        if where_clauses:
            sql_query += " where " + " and ".join(where_clauses)

        sql_query += " ORDER BY b.setdate ASC"

        result = db.session.execute(text(sql_query)).fetchall()

        if len(result):
            serialized = json.dumps([dict(r) for r in result], default=alchemyencoder)
            return Response(serialized, mimetype='application/json')
        else:
            return jsonify({"error": "No matching records found."})

    if request.method == 'POST':
        pass

    return


@api_bp.route("facilities", methods=['GET'])
def facilities():
    '''Return list of all facilities.'''
    try:
        result = db.session.query(BicycleCount.BikePedFac).distinct().all()
    except NoResultFound:
        return jsonify({"error": "No facilities found."})

    result = [row[0] for row in result if row[0]]
    return jsonify(result)
