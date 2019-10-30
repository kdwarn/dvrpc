import pytest

from bicycles import create_app, models, db
from config import TestConfig


dummy_data = {
    "x": -75.172528,
    "y": 39.953553,
    "objectid": 51841,
    "recordnum": 140305,
    "setdate": "2018-03-14T20:00:00-04:00",
    "setyear": 2018,
    "comments": "",
    "mcd": 4210160103,
    "route": "3",
    "road": "market st north side",
    "cntdir": "east ",
    "fromlmt": "20th st",
    "tolmt": "19th st",
    "type": "Bicycle 2",
    "latitude": 39.953545,
    "longitude": -75.172526,
    "factor": 0,
    "axle": 1.02,
    "outdir": "W",
    "indir": "E",
    "aadb": 133,
    "updated": "2018-09-10T22:36:30-04:00",
    "co_name": "Philadelphia",
    "mun_name": "Central",
    "globalid": "3bd7ec0f-0d03-48d8-9323-04b21ed5f05d",
    "program": "Project",
    "bikepedgro": "Mixed",
    "bikepedfac": "Mixed Traffic",
    "geom": "0101000020E61000006CED7DAA0ACB52C0D52137C30DFA4340",
}


@pytest.fixture
def flask_client():
    test_app = create_app(config_class=TestConfig)
    flask_client = test_app.test_client()

    with test_app.app_context():
        db.create_all()

        count = models.BicycleCount(**dummy_data)
        db.session.add(count)
        db.session.commit()

        yield flask_client

        db.session.remove()
        db.drop_all()
