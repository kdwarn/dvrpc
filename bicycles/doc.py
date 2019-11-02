from flask import Blueprint, render_template

doc_bp = Blueprint('doc_bp', __name__)  # url prefix of api/documentation set in init


@doc_bp.route('/')
def documentation():
    intro = {}

    intro['top'] = """
        The DVRPC Bicycle Count REST API allows users to interact with data from the DVRPC's Bicycle 
        Count program. The API provides access to the data via POST, GET, PUT, and DELETE HTTP Request 
        methods, which are returned in JSON format. The following status codes for Responses are 
        implemented:
        """

    intro['responses'] = {
        '200': 'OK',
        '201': 'Created',
        '400': 'Bad Request',
        '404': 'Not Found',
        '500': 'Internal Server Error',
    }

    intro['bottom'] = "Additional details for Requests and Responses are provided for each Endpoint below."

    base_url = '/api'

    endpoints = [
        {
            'url': '/counts/<recordnum>',
            'methods': [
                {
                    'name': 'GET',
                    'description': 'Retrieve one count',
                    'parameters': [
                        {
                            'name': 'recordnum',
                            'type': 'path',
                            'required': True,
                            'content': 'Integer',
                        }
                    ],
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Provided recordnum is not an Integer',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No count with provided recordnum found',
                        },

                    ]
                },
                {
                    'name': 'PUT',
                    'description': 'Edit one count',
                    'parameters': [
                        {
                            'name': 'recordnum',
                            'type': 'path',
                            'required': True,
                            'content': 'Integer',
                        },
                        {
                            'name': 'x',
                            'type': 'body',
                            'required': False,
                            'content': 'Float',
                        },
                        {
                            'name': 'y',
                            'type': 'body',
                            'required': False,
                            'content': 'Float',
                        },
                        {
                            'name': 'objectid',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'setdate',
                            'type': 'body',
                            'required': False,
                            'content': 'Date, in format YYYY-MM-DD',
                        },
                        {
                            'name': 'comments',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'mcd',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'route',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'road',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'cntdir',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                            'possible_values': [
                                'both',
                                'east',
                                'west',
                                'north',
                                'south',
                            ],
                        },
                        {
                            'name': 'fromlmt',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'tolmt',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'type',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'latitude',
                            'type': 'body',
                            'required': False,
                            'content': 'Float',
                        },
                        {
                            'name': 'longitude',
                            'type': 'body',
                            'required': False,
                            'content': 'Float',
                        },
                        {
                            'name': 'factor',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'axle',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer or Float',
                            'possible_values': [
                                0,
                                1,
                                1.02,
                            ],
                        },
                        {
                            'name': 'outdir',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                            'possible_values': [
                                'E',
                                'W',
                                'N',
                                'S',
                            ],
                        },
                        {
                            'name': 'indir',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                            'possible_values': [
                                'E',
                                'W',
                                'N',
                                'S',
                            ],
                        },
                        {
                            'name': 'aadb',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'co_name',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                            'possible_values': [
                                'Bucks',
                                'Chester',
                                'Delaware',
                                'Montgomery',
                                'Philadelphia',
                                'Burlington',
                                'Camden',
                                'Gloucester',
                                'Mercer',
                            ],
                        },
                        {
                            'name': 'mun_name',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'program',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'bikepedgro',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'bikepedfac',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                    ],
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Error in submitted parameters. A message detailing '
                                           'the problems will be provided',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No count with provided recordnum found',
                        },
                        {
                            'status_code': '500 Internal Server Error',
                            'description': 'An error ocurred on the server',
                        },
                    ],
                },
                {
                    'name': 'DELETE',
                    'description': 'Delete one count',
                    'parameters': [
                        {
                            'name': 'recordnum',
                            'type': 'path',
                            'required': True,
                            'content': 'Integer',
                        },
                    ],
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Provided recordnum is not an Integer',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No count with provided recordnum found',
                        },
                        {
                            'status_code': '500 Internal Server Error',
                            'description': 'An error ocurred on the server',
                        },
                    ],
                },
            ],
        },
        {
            'url': '/counts',
            'methods': [
                {
                    'name': 'GET',
                    'description': 'Retrieve all counts in chronological order, optionally '
                                   'filtered by facility type (bikepedfac) and precipitation '
                                   '(prcp) amount',
                    'parameters': [
                        {
                            'name': 'bikepedfac',
                            'type': 'query string',
                            'required': False,
                            'content': "String",
                        },
                        {
                            'name': 'prcp',
                            'type': 'query string',
                            'required': False,
                            'content': "Integer or Float"
                        }
                    ],
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Error in submitted parameters. A message detailing '
                                           'the problems will be provided',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No counts with provided criteria found',
                        },
                    ],
                },
                {
                    'name': 'POST',
                    'description': 'Create new count',
                    'parameters': [
                        {
                            'name': 'x',
                            'type': 'body',
                            'required': True,
                            'content': 'Float',
                        },
                        {
                            'name': 'y',
                            'type': 'body',
                            'required': True,
                            'content': 'Float',
                        },
                        {
                            'name': 'objectid',
                            'type': 'body',
                            'required': True,
                            'content': 'Integer',
                        },
                        {
                            'name': 'setdate',
                            'type': 'body',
                            'required': True,
                            'content': 'Date, in format YYYY-MM-DD',
                        },
                        {
                            'name': 'comments',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'mcd',
                            'type': 'body',
                            'required': True,
                            'content': 'Integer',
                        },
                        {
                            'name': 'route',
                            'type': 'body',
                            'required': False,
                            'content': 'Integer',
                        },
                        {
                            'name': 'road',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'cntdir',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                            'possible_values': [
                                'both',
                                'east',
                                'west',
                                'north',
                                'south',
                            ],
                        },
                        {
                            'name': 'fromlmt',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'tolmt',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'type',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'latitude',
                            'type': 'body',
                            'required': True,
                            'content': 'Float',
                        },
                        {
                            'name': 'longitude',
                            'type': 'body',
                            'required': True,
                            'content': 'Float',
                        },
                        {
                            'name': 'factor',
                            'type': 'body',
                            'required': True,
                            'content': 'Integer',
                        },
                        {
                            'name': 'axle',
                            'type': 'body',
                            'required': True,
                            'content': 'Integer or Float',
                            'possible_values': [
                                0,
                                1,
                                1.02
                            ],
                        },
                        {
                            'name': 'outdir',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                            'possible_values': [
                                'E',
                                'W',
                                'N',
                                'S',
                            ],
                        },
                        {
                            'name': 'indir',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                            'possible_values': [
                                'E',
                                'W',
                                'N',
                                'S',
                            ],
                        },
                        {
                            'name': 'aadb',
                            'type': 'body',
                            'required': True,
                            'content': 'Integer',
                        },
                        {
                            'name': 'co_name',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                            'possible_values': [
                                'Bucks',
                                'Chester',
                                'Delaware',
                                'Montgomery',
                                'Philadelphia',
                                'Burlington',
                                'Camden',
                                'Gloucester',
                                'Mercer',
                            ],
                        },
                        {
                            'name': 'mun_name',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'program',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                        {
                            'name': 'bikepedgro',
                            'type': 'body',
                            'required': True,
                            'content': 'String',
                        },
                        {
                            'name': 'bikepedfac',
                            'type': 'body',
                            'required': False,
                            'content': 'String',
                        },
                    ],
                    'responses': [
                        {
                            'status_code': '201 Created',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Error in submitted parameters. A message detailing '
                                           'the problems will be provided',
                        },
                    ],
                },
            ],
        },
        {
            'url': '/counts/closest',
            'methods': [
                {
                    'name': 'GET',
                    'description': 'Retrieve 5 counts closest to given latitude/longitude',
                    'parameters': [
                        {
                            'name': "latitude",
                            'type': "query string",
                            'required': True,
                            'content': "Float",
                        },
                        {
                            'name': "longitude",
                            'type': "query string",
                            'required': True,
                            'content': "Float",
                        }
                    ],
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '400 Bad Request',
                            'description': 'Values for latitude and/or longitude not provided or '
                                           'values provided are not Floats',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No counts found',
                        },
                    ],
                },
            ],
        },
        {
            'url': '/counts/facilities',
            'methods': [
                {
                    'name': 'GET',
                    'description': 'Retrieve all facility types',
                    'responses': [
                        {
                            'status_code': '200 OK',
                            'description': 'Success',
                        },
                        {
                            'status_code': '404 Not Found',
                            'description': 'No facilities found',
                        },
                    ],
                },
            ],
        },
    ]

    return render_template("documentation.html", intro=intro, endpoints=endpoints)
