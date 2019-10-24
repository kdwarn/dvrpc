import json
import datetime
import decimal

from flask import request, Blueprint, Response, jsonify
from sqlalchemy import text

from bicycles import db
from .models import BicycleCount

api_bp = Blueprint("api", __name__)  # url prefix of /api set in init


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


@api_bp.route("counts/<record_num>", methods=['GET', 'PUT', 'DELETE'])
def count(record_num):
    '''Get, edit, or delete one bicycle count record.'''
    if request.method == 'GET':
        return record_num

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

    return


@api_bp.route("counts", methods=['GET', 'POST'])
def counts(facility_type="", precipitation="", lat="", lon=""):
    '''Return all bicycle counts according to various criteria or add new bicycle count record.'''
    if request.method == 'GET':

        t = text("select b.*, w.prcp, w.tavg, w.tmax, w.tmin from bicycle_count b left join "
                 "weather w on date(b.setdate) = w.date")
        result = db.session.execute(t)

        serialized = json.dumps([dict(r) for r in result], default=alchemyencoder)

        return Response(serialized, mimetype='application/json')

    if request.method == 'POST':
        pass

    return


@api_bp.route("facilities", methods=['GET'])
def facilities():
    '''Return list of all facilities.'''
    result = db.session.query(BicycleCount.BikePedFac).distinct().all()
    result = [row[0] for row in result if row[0]]
    return jsonify(result)
