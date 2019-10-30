import pytest

####################
# helper functions #
####################



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

