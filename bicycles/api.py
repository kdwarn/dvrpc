import json
import datetime
import decimal
import uuid

from flask import request, Blueprint, Response, jsonify, make_response, url_for
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.inspection import inspect
from werkzeug.exceptions import BadRequest

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
    required_fields = ['x',
                       'y',
                       'objectid',
                       'setdate',
                       'mcd',
                       'road',
                       'cntdir',
                       'fromlmt',
                       'tolmt',
                       'type',
                       'latitude',
                       'longitude',
                       'factor',
                       'axle',
                       'outdir',
                       'indir',
                       'aadb',
                       'co_name',
                       'mun_name',
                       'bikepedgro',
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

    type_int = ['objectid', 'mcd', 'route', 'factor', 'aadb']
    type_float = ['x', 'y', 'latitude', 'longitude']
    type_string = ['road',
                   'fromlmt',
                   'tolmt',
                   'type',
                   'mun_name',
                   'program',
                   'bikepedgro',
                   'bikepedfac',
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
        if k == 'cntdir' and v not in cnt_dir:
            bad_params.append(k + " must be one of " + ", ".join(cnt_dir))
        if k == 'axle' and v not in axle:
            bad_params.append(k + " must be one of " + ", ".join(str(n) for n in axle))
        if k in ['indir', 'outdir'] and v not in in_out_dir:
            bad_params.append(k + " must be one of " + ", ".join(in_out_dir))
        if k == 'co_name' and v not in counties:
            bad_params.append(k + " must be one of " + ", ".join(counties))

        # check SETDate
        # since all values in sample had no time values, just require date in format YYYY-MM-DD,
        # and then convert to datetime when inserting/updating
        if k == 'setdate':
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
    # ensure record_num is an int
    try:
        record_num = int(record_num)
    except ValueError:
        return jsonify({"error": f"{record_num} is not a valid recordnum"}), 400

    if request.method == 'GET':
        sql_query += " WHERE recordnum = :record_num"
        
        result = db.session.execute(text(sql_query), {"record_num": record_num}).fetchall()
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
        try:
            params = request.get_json()
        except BadRequest:
            return jsonify({"error": "Unable to process submitted JSON content."})
        
        if not params:
            return jsonify({"error": "No parameters submitted."}), 400

        unknown_params, bad_params = check_params(params)

        if unknown_params:
            return jsonify({"error": "Unknown parameter(s) submitted: "
                            + ", ".join(unknown_params)}), 400

        if bad_params:
            return jsonify({"error": "Error(s) in submitted parameters: "
                            + "; ".join(bad_params)}), 400

        # remove params that should not be updated by client
        try:
            del params["setyear"]
        except KeyError:
            pass
        try:
            del params["globalid"]
        except KeyError:
            pass

        count = BicycleCount.query.filter_by(recordnum=record_num)
        
        try:
            count.one()
        except NoResultFound:
            return jsonify({"error": "No matching record found."}), 404
        except MultipleResultsFound:
            return jsonify({"error": "More than one record found. There are mutliple records with "
                            "the same PRIMARY KEY"}), 500
        
        # set Updated
        params["updated"] = datetime.datetime.now(datetime.timezone.utc)

        # update fields
        count.update(params)
        db.session.commit()

        # update geom, if either lat or lon submitted
        if params.get("latitude") or params.get("longitude"):
            count = BicycleCount.query.filter_by(recordnum=record_num).one()
            sql_query = f'''
                UPDATE bicycle_count
                SET geom = ST_SetSRID(ST_MakePoint({count.longitude}, {count.latitude}), 4326)
                WHERE recordnum = {count.recordnum}
                '''
            db.session.execute(text(sql_query))
            db.session.commit()

        # get location of updated resource (url_root[:-1] removes duplicate "/")
        location = request.url_root[:-1] + url_for('api.count', record_num=record_num)
        
        response = make_response({"Success": "true"}, 200)
        response.headers['Location'] = location
        return response

    if request.method == 'DELETE':
        try:
            result = BicycleCount.query.filter_by(recordnum=record_num).one()
        except NoResultFound:
            return jsonify({"error": "No matching record found."}), 404
        except MultipleResultsFound:
            return jsonify({"error": "More than one record found. There are mutliple records with "
                            "the same PRIMARY KEY"}), 500

        BicycleCount.query.filter_by(recordnum=record_num).delete()
        db.session.commit()

        return jsonify({"Success": "Count with recordnum " + str(record_num) + " deleted."})

    return


@api_bp.route("counts", methods=['GET', 'POST'])
def counts(sql_query=sql_query):
    '''Return all bicycle counts according to various criteria or add new bicycle count record.'''
    if request.method == 'GET':
        bikepedfac = request.args.get("bikepedfac")
        precipitation = request.args.get("precipitation")
        
        where_clauses = []

        if precipitation:
            try:
                precipitation = float(precipitation)
            except ValueError:
                return jsonify({'error': 'Precipitation value must be an number, with optional '
                                'decimal points.'}), 400
            
            where_clauses.append(f"w.prcp >= {precipitation}")
        
        if bikepedfac:
            facility_types = ['Multiuse Trail',
                              'Sidepath',
                              'Striped Shoulder',
                              'Bike Lane',
                              'Mixed Traffic',
                              'Buffered Bike Lane',
                              'Sharrow']
            if bikepedfac not in facility_types:
                return jsonify({'error': 'Facility must be one of '
                                          + ', '.join(facility_types)}), 400
            where_clauses.append(f"b.bikepedfac = '{bikepedfac}'")

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
        try:
            params = request.get_json()
        except BadRequest:
            return jsonify({"error": "Unable to process submitted JSON content."})

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
        params["setdate"] = datetime.datetime.strptime(params["setdate"], "%Y-%m-%d")
        params["setyear"] = params["setdate"].year
        params["updated"] = datetime.datetime.now(datetime.timezone.utc)
        params["globalid"] = str(uuid.uuid4())  # ideally, this would check against existing GlobalIDs
        
        count = BicycleCount(**params)

        db.session.add(count)
        db.session.commit()

        # add the geom field
        sql_query = f'''
            UPDATE bicycle_count
            SET geom = ST_SetSRID(ST_MakePoint({params["longitude"]}, {params["latitude"]}), 4326)
            WHERE recordnum = {count.recordnum}
            '''
        db.session.execute(text(sql_query))
        db.session.commit()
        
        # get location of created resource (url_root[:-1] removes duplicate "/")
        location = request.url_root[:-1] + url_for('api.count', record_num=count.recordnum)
        
        response = make_response({"Success": "true"}, 201)
        response.headers['Location'] = location
        return response
        

@api_bp.route("counts/closest", methods=['GET'])
def closest(sql_query=sql_query):
    '''Return 5 closest counts to given lat/lon location.'''
    if request.method == 'GET':
        lon = request.args.get("lon")
        lat = request.args.get("lat")

        if not lat or not lon:
            return jsonify({"error": "You must supply a longitude and a latitude."}), 400

        # ensure they are floats
        try:
            lon = float(lon)
        except ValueError:
            return jsonify({"error": f"{lon} is not a valid longitude"})
        
        try:
            lat = float(lat)
        except ValueError:
            return jsonify({"error": f"{lat} is not a valid longitude"})

        sql_query += f'''
            ORDER BY
            b.geom <->'SRID=4326;POINT({lon} {lat})'::geometry
            LIMIT 5;
            '''
        
        result = db.session.execute(text(sql_query)).fetchall()

        if len(result):
            serialized = json.dumps([dict(r) for r in result], default=alchemyencoder)
            return Response(serialized, mimetype='application/json')
        else:
            return jsonify({"error": "No matching records found."}), 404


@api_bp.route("facilities", methods=['GET'])
def facilities():
    '''Return list of all facilities.'''
    try:
        result = db.session.query(BicycleCount.bikepedfac).distinct().all()
    except NoResultFound:
        return jsonify({"error": "No facilities found."}), 404

    result = [row[0] for row in result if row[0]]
    return jsonify(result)
