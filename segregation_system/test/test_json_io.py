import sys
import pytest
sys.path.insert(0, r'../../segregation_system')
from src.json_io import JsonIO

@pytest.fixture
def json_io():
    return JsonIO.get_instance()

@pytest.fixture
def test_session():
    return {
            "_id" : "wrwewr-ewrewr-werwrew-werrwe",
            "calendar" : "shopping",
            "environment" : "slippery",
            "label" : "Regular",
            "features" : 
                        {
                        "maximum_pressure_ts" : 0.0,
                        "minimum_pressure_ts" : 0.0,
                        "median_pressure_ts" : 0.0,
                        "mean_absolute_deviation_pressure_ts" : 0.0,
                        "activity_and_small_scatter" : 0.0,
                        "environment_and_small_scatter" : 0.0
                        }
            }

def test_get_instance(json_io):
    assert json_io == JsonIO.get_instance()

def test_get_app(json_io):
    assert json_io.get_app() == JsonIO.get_instance().get_app()

def test_prepared_session(json_io ,test_session):
    res = json_io.get_app().test_client().post("/preparedsession" , json = test_session)
    assert res.status_code == 200