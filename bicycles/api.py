from flask import Flask, request, Blueprint

from bicycles import db
from .models import BicycleCount, Weather

api_bp = Blueprint("api", __name__)  # url prefix of /api set in init


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
        pass

    if request.method == 'POST':
        pass

    return

@api_bp.route("facilities", methods=['GET'])
def facilities():
    '''Return list of all facilities.'''
    
    return "List of facilities"
