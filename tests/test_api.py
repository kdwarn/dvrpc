import pytest

from bicycles import api

####################
# helper functions #
####################

# check_required_fields()


def test_required_fields_result_empty_if_all_submitted():
    params = {'x': "dummy",
              'y': "dummy",
              'objectid': "dummy",
              'setdate': "dummy",
              'mcd': "dummy",
              'road': "dummy",
              'cntdir': "dummy",
              'fromlmt': "dummy",
              'tolmt': "dummy",
              'type': "dummy",
              'latitude': "dummy",
              'longitude': "dummy",
              'factor': "dummy",
              'axle': "dummy",
              'outdir': "dummy",
              'indir': "dummy",
              'aadb': "dummy",
              'co_name': "dummy",
              'mun_name': "dummy",
              'bikepedgro': "dummy",
    }
    missing_params = api.check_required_fields(params)
    assert len(missing_params) == 0


def test_required_fields_no_required_fields_submitted():
    params = {'not_required': 'dummy'}
    missing_params = api.check_required_fields(params)
    assert len(missing_params) == 20


def test_required_fields_one_required_field_submitted():
    params = {'x': 123}
    missing_params = api.check_required_fields(params)
    assert len(missing_params) == 19


def test_required_fields_case():
    params = {'X': 123}
    missing_params = api.check_required_fields(params)
    assert len(missing_params) == 20


# check_params()

def test_check_params_one_unknown_param():
    params = {'not_a_param': 'some text'}
    unknown_params, bad_params = api.check_params(params)
    assert len(unknown_params) == 1 and unknown_params[0] == "not_a_param"


def test_check_params_multiple_unknown_params():
    params = {'not_a_param': 'some text',
              'not_a_param1': 'some text',
              'not_a_param2': 'some text',
    }
    unknown_params, bad_params = api.check_params(params)
    assert (len(unknown_params) == 3 and 
            unknown_params[0] == "not_a_param" and
            unknown_params[1] == "not_a_param1" and
            unknown_params[2] == "not_a_param2")


@pytest.mark.parametrize("params",
                         [{'objectid': 'not int'},
                          {'mcd': 'not int'},
                          {'route': 'not int'},
                          {'factor': 'not int'},
                          {'aadb': 'not int'},
                         ])
def test_check_params_int_types_bad(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 1


@pytest.mark.parametrize("params",
                         [{'x': 1},
                          {'y': 1},
                          {'latitude': 1},
                          {'longitude': 1},
                         ])
def test_check_params_float_types_bad(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 1


@pytest.mark.parametrize("params",
                         [{'road': 1},
                          {'fromlmt': 1},
                          {'tolmt': 1},
                          {'type': 1},
                          {'mun_name': 1},
                          {'program': 1},
                          {'bikepedgro': 1},
                          {'bikepedfac': 1},
                         ])
def test_check_params_string_types_bad(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 1


@pytest.mark.parametrize("params",
                         [{'cntdir': 1},
                          {'axle': 'not 0, 1, or 1.02'},
                          {'indir': 1},
                          {'outdir': 1},
                          {'co_name': 1},
                         ])
def test_check_params_values_bad(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 1


@pytest.mark.parametrize("params",
                         [{'setdate': '2019-09-31'},
                          {'setdate': '19-01-31'},
                          {'setdate': '2019-02-29'},
                         ])
def test_check_params_setdate_bad(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 1

@pytest.mark.parametrize("params",
                         [{'objectid': 123},
                          {'mcd': 123},
                          {'route': 123},
                          {'factor': 1},
                          {'aadb': 123},
                          {'x': -75.123456},
                          {'y': 39.08890},
                          {'latitude': 39.08890},
                          {'longitude': -75.123456},
                          {'road': 'some road'},
                          {'fromlmt': 'something'},
                          {'tolmt': 'something'},
                          {'type': 'something'},
                          {'mun_name': 'municipality'},
                          {'program': 'a program'},
                          {'bikepedgro': 'something'},
                          {'bikepedfac': 'Mixed Traffic'},
                          {'cntdir': "both"},
                          {'cntdir': "north"},
                          {'cntdir': "east"},
                          {'cntdir': "south"},
                          {'cntdir': "west"},
                          {'axle': 0},
                          {'axle': 1},
                          {'axle': 1.02},
                          {'indir': 'N'},
                          {'indir': 'E'},
                          {'indir': 'S'},
                          {'indir': 'W'},
                          {'outdir': 'N'},
                          {'outdir': 'E'},
                          {'outdir': 'S'},
                          {'outdir': 'W'},
                          {'co_name': 'Bucks'},
                          {'co_name': 'Chester'},
                          {'co_name': 'Delaware'},
                          {'co_name': 'Montgomery'},
                          {'co_name': 'Philadelphia'},
                          {'co_name': 'Burlington'},
                          {'co_name': 'Camden'},
                          {'co_name': 'Gloucester'},
                          {'co_name': 'Mercer'},
                          {'setdate': '2019-09-30'},
                          {'setdate': "2020-02-29"},
                         ])
def test_check_params_all_good(params):
    unknown_params, bad_params = api.check_params(params)
    assert len(bad_params) == 0

###########
# count() #
###########

# all request methods


def test_count_get_returns_error_if_bad_recordnum(flask_client):
    response = flask_client.get("/api/counts/notvalid")
    json_data = response.get_json()
    assert response.status_code == 400 and "not a valid recordnum" in json_data["error"]


def test_count_put_returns_error_if_bad_recordnum(flask_client):
    response = flask_client.put("/api/counts/notvalid")
    json_data = response.get_json()
    assert response.status_code == 400 and "not a valid recordnum" in json_data["error"]


def test_count_delete_returns_error_if_bad_recordnum(flask_client):
    response = flask_client.delete("/api/counts/notvalid")
    json_data = response.get_json()
    assert response.status_code == 400 and "not a valid recordnum" in json_data["error"]


# get


def test_count_get_returns_one_value(flask_client):
    response = flask_client.get("/api/counts/140313")
    json_data = response.get_json()
    assert len(json_data) == 1 and response.status_code == 200


def test_count_get_returns_404_if_no_matching_recordnum(flask_client):
    response = flask_client.get("/api/counts/1")
    json_data = response.get_json()
    assert response.status_code == 404 and json_data["error"] == "No matching record found."


# put






    

############
# counts() #
############


#############
# closest() #
#############


################
# facilities() #
################

def test_facilities1(flask_client):

    response = flask_client.get("/api/facilities")
    json_data = response.get_json()
    assert len(json_data) == 4

