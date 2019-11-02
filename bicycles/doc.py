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
        '201': 'Item Created',
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
                            'status_code': '200',
                            'short_name': 'OK',
                            'description': "Success"
                        },
                        {
                            'status_code': '400',
                            'short_name': 'Bad Request',
                            'description': "Provided <recordnum> is not an Integer"
                        },
                        {
                            'status_code': '404',
                            'short_name': 'Not Found',
                            'description': "No count with provided <recordnum> found"
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
                            'name': '',
                            'type': 'query string',
                            'required': False,
                            'content': '',
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
                    ]
                },
                {
                    'name': 'POST',
                    'description': 'Create new count',
                }
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
                    ]
                },
            ],
        },
        {
            'url': '/counts/facilities',
            'methods': [
                {
                    'name': 'GET',
                    'description': 'Retrieve all facility types',
                },
            ],
        },
    ]

    return render_template("documentation.html", intro=intro, endpoints=endpoints)
