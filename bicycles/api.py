import json
import datetime
import decimal

from flask import request, Blueprint, Response, jsonify
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect

from bicycles import db
from .models import BicycleCount

api_bp = Blueprint("api", __name__)  # url prefix of /api set in init


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def check_params(params):
    # list of fields in database
    table = inspect(BicycleCount)
    field_names = [field.name for field in table.c]

    # check for unknown parameters, parameter type, parameter content
    unknown_params = []
    bad_params = []
    type_int = ['ObjectID', 'SETYear', 'MCD', 'Route', 'Factor', 'AADB']
    type_float = ['X', 'Y', 'Latitude', 'Longitude']
    type_datetime = ['SETDate', 'Updated']
    type_string = ['Road',
                   'FromLmt',
                   'ToLmt',
                   'Type',
                   'Mun_name',
                   'Program',
                   'BikePedGro',
                   'BikePedFac']
    cnt_dir = ['both', 'east', 'west', 'north', 'south']
    axle = [0, 1, 1.02]
    in_out_dir = ['E', 'W', 'N', 'S']
    counties = ['Bucks',
                'Chester',
                'Delaware',
                'Montgomery',
                'Philadelphia',
                'Burlington',
                'Camden',
                'Gloucester',
                'Mercer']
    
    for k, v in params.items():
        if k not in field_names:
            unknown_params.append(k)

        if k in type_int and type(v) is not int:
            bad_params.append(k + " must be an integer")
        if k in type_float and type(v) is not float:
            bad_params.append(k + " must be a float")
        if k in type_datetime and type(v) is not datetime:
            bad_params.append(k + " must be in datetime ISO format")
        if k in type_string and type(v) is not str:
            bad_params.append(k + " must be text")
        if k == 'CntDir' and v not in cnt_dir:
            bad_params.append(k + " must be one of " + ", ".join(cnt_dir))
        if k == 'Axle' and v not in axle:
            bad_params.append(k + " must be one of " + ", ".join(str(n) for n in axle))
        if k in ['InDir', 'OutDir'] and v not in in_out_dir:
            bad_params.append(k + " must be one of " + ", ".join(in_out_dir))
        if k == 'Co_name' and v not in counties:
            bad_params.append(k + " must be one of " + ", ".join(counties))

        # Other checks would go here (Mun_name, etc.)

    return bad_params, unknown_params


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
        if not request.data:
            return jsonify({"error": "No Request body submitted"})

        if not request.is_json:
            return jsonify({"error": "Request body must be submitted in json format"})

        # get user-submitted parameters (body)
        params = request.get_json()

        if not params:
            return jsonify({"error": "No parameters submitted."})

        unknown_params, bad_params = check_params(params)

        if unknown_params:
            return jsonify({"error": "Unknown parameter(s) submitted: "
                            + ", ".join(unknown_params)})

        if bad_params:
            return jsonify({"error": "Error(s) in submitted parameters: "
                            + "; ".join(bad_params)})

        return "No errors"

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
