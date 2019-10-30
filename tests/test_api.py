import pytest


def test_facilities1(flask_client):
    response = flask_client.get("/api/facilities")
    json_data = response.get_json() 
    assert json_data[0] == "Mixed Traffic"


def test_counts1(flask_client):
    response = flask_client.get("/api/counts")
    json_data = response.get_json()
    assert len(json_data) == 1
