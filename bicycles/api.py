import json
import datetime
import decimal
import uuid

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


def check_required_fields(params):
    '''When creating a new count, check params submitted against required fields.'''
    # assumed required_params based on sample of counts without missing values, excluding
    # "RecordNum", "Updated", and "GlobalID"
    required_fields = ['X',
                       'Y',
                       'ObjectID',
                       'SETDate',
                       'SETYear',
                       'MCD',
                       'Road',
                       'CntDir',
                       'FromLmt',
                       'ToLmt',
                       'Type',
                       'Latitude',
                       'Longitude',
                       'Factor',
                       'Axle',
                       'OutDir',
                       'InDir',
                       'AADB',
                       'Co_name',
                       'Mun_name',
                       'BikePedGro',
    ]

    missing_params = []

    for field in required_fields:
        if field not in params.keys():
            missing_params.append(field)
    
    return missing_params

def check_params(params):
    '''
    Check user-submitted parameters, in PUT and POST requests, against allowed parameters,
    type of parameters, and allowed content of parameters.
    '''
    table = inspect(BicycleCount)
    field_names = [field.name for field in table.c]

    unknown_params = []
    bad_params = []

    type_int = ['ObjectID', 'SETYear', 'MCD', 'Route', 'Factor', 'AADB']
    type_float = ['X', 'Y', 'Latitude', 'Longitude']
    type_string = ['Road',
                   'FromLmt',
                   'ToLmt',
                   'Type',
                   'Mun_name',
                   'Program',
                   'BikePedGro',
                   'BikePedFac',
    ]
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
                'Mercer',
    ]

    # check for unknown parameters and parameter type/content
    for k, v in params.items():
        if k not in field_names:
            unknown_params.append(k)

        # check types
        if k in type_int and type(v) is not int:
            bad_params.append(k + " must be an integer")
        if k in type_float and type(v) is not float:
            bad_params.append(k + " must be a float")
        if k in type_string and type(v) is not str:
            bad_params.append(k + " must be text")
        
        # check values
        if k == 'CntDir' and v not in cnt_dir:
            bad_params.append(k + " must be one of " + ", ".join(cnt_dir))
        if k == 'Axle' and v not in axle:
            bad_params.append(k + " must be one of " + ", ".join(str(n) for n in axle))
        if k in ['InDir', 'OutDir'] and v not in in_out_dir:
            bad_params.append(k + " must be one of " + ", ".join(in_out_dir))
        if k == 'Co_name' and v not in counties:
            bad_params.append(k + " must be one of " + ", ".join(counties))

        # check SETDate
        # since all values in sample had no time values, just require date in format YYYY-MM-DD,
        # and then convert to datetime when inserting/updating
        if k == 'SETDate':
            try:
                datetime.datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                bad_params.append(k + " must be in the format 'YYYY-MM-DD")

        # Other checks would go here (Mun_name, against allowed value for facilities, etc.)

    return unknown_params, bad_params


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
            return jsonify({"error": "No matching record found."}), 404

    if request.method == 'PUT':
        if not request.data:
            return jsonify({"error": "No Request body submitted"}), 400

        if not request.is_json:
            return jsonify({"error": "Request body must be submitted in json format"}), 400

        # get user-submitted parameters (body)
        params = request.get_json()

        if not params:
            return jsonify({"error": "No parameters submitted."}), 400

        unknown_params, bad_params = check_params(params)

        if unknown_params:
            return jsonify({"error": "Unknown parameter(s) submitted: "
                            + ", ".join(unknown_params)}), 400

        if bad_params:
            return jsonify({"error": "Error(s) in submitted parameters: "
                            + "; ".join(bad_params)}), 400

        try:
            count = BicycleCount.query.filter_by(RecordNum=record_num).one()
        except NoResultFound:
            return jsonify({"error": "No matching record found."}), 404
        
        # update fields
        return "Update here"


    if request.method == 'DELETE':
        try:
            result = BicycleCount.query.filter_by(RecordNum=int(record_num)).one()
        except NoResultFound:
            return jsonify({"error": "No count found with RecordNum " + record_num}), 404

        BicycleCount.query.filter_by(RecordNum=int(record_num)).delete()
        db.session.commit()

        return jsonify({"Success": "Count with RecordNum " + record_num + " deleted."})

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
                                'decimal points.'}), 400
            
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
                return jsonify({'error': 'Facility must be one of '
                                          + ', '.join(facility_types)}), 400
            where_clauses.append(f"b.bikepedfac = '{facility}'")

        if where_clauses:
            sql_query += " where " + " and ".join(where_clauses)

        sql_query += " ORDER BY b.setdate ASC"

        result = db.session.execute(text(sql_query)).fetchall()

        if len(result):
            serialized = json.dumps([dict(r) for r in result], default=alchemyencoder)
            return Response(serialized, mimetype='application/json')
        else:
            return jsonify({"error": "No matching records found."}), 404

    if request.method == 'POST':
        if not request.data:
            return jsonify({"error": "No Request body submitted"}), 400

        if not request.is_json:
            return jsonify({"error": "Request body must be submitted in json format"}), 400

        # get user-submitted parameters (body)
        params = request.get_json()

        if not params:
            return jsonify({"error": "No parameters submitted."}), 400

        missing_params = check_required_fields(params)
        unknown_params, bad_params = check_params(params)

        if missing_params:
            return jsonify({"error": "Missing required parameters: "
                            + ", ".join(missing_params)}), 400
        if unknown_params:
            return jsonify({"error": "Unknown parameter(s) submitted: "
                            + ", ".join(unknown_params)}), 400

        if bad_params:
            return jsonify({"error": "Error(s) in submitted parameters: "
                            + "; ".join(bad_params)}), 400

        # insert into db
        # process a few special params
        params["SETDate"] = datetime.datetime.strptime(params["SETDate"], "%Y-%m-%d")
        params["Updated"] = datetime.datetime.now(datetime.timezone.utc)
        params["GlobalID"] = uuid.uuid4().hex  # ideally, this would check against existing GlobalIDs

        db.session.add(BicycleCount(**params))
        db.session.commit()

        return jsonify({"Success": "New count inserted."})
        


@api_bp.route("facilities", methods=['GET'])
def facilities():
    '''Return list of all facilities.'''
    try:
        result = db.session.query(BicycleCount.BikePedFac).distinct().all()
    except NoResultFound:
        return jsonify({"error": "No facilities found."}), 404

    result = [row[0] for row in result if row[0]]
    return jsonify(result)
