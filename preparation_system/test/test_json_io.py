import sys
import pytest
sys.path.insert(0, r'..')
from src.json_io import JsonIO

@pytest.fixture
def json_io():
    return JsonIO.get_instance()

@pytest.fixture
def test_raw_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "time_series" : list(range(1, 1237)),
            "calendar" : "shopping",
            "environment" : "slippery",
            "pressure_dected" : "Regular"}

def test_get_instance(json_io):
    assert json_io == JsonIO.get_instance()

def test_get_app(json_io):
    assert json_io.get_app() == JsonIO.get_instance().get_app()

def test_recieve_raw_session(json_io ,test_raw_session):
    res = json_io.get_app().test_client().post("/json" , json = test_raw_session)
    assert res.status_code == 200
