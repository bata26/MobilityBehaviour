import sys
import pytest
sys.path.insert(0, r'..')
from src.json_io import JsonIO

@pytest.fixture
def json_io():
    return JsonIO.get_instance()

@pytest.fixture
def test_label_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "pressure_detected" : "Regular",
            }

@pytest.fixture
def test_env_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "environment" : "slippery",
            }

@pytest.fixture
def test_act_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "calendar" : "shopping",
            }

@pytest.fixture
def test_time_series_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "time_series" : list(range(1, 1237))
          }

def test_get_instance(json_io):
    assert json_io == JsonIO.get_instance()

def test_get_app(json_io):
    assert json_io.get_app() == JsonIO.get_instance().get_app()

def test_label_record(json_io ,test_label_session):
    res = json_io.get_app().test_client().post("/record" , json = test_label_session)
    assert res.status_code == 200

def test_env_record(json_io ,test_env_session):
    res = json_io.get_app().test_client().post("/record" , json = test_env_session)
    assert res.status_code == 200

def test_activity_record(json_io ,test_act_session):
    res = json_io.get_app().test_client().post("/record" , json = test_act_session)
    assert res.status_code == 200

def test_time_series_record(json_io ,test_time_series_session):
    res = json_io.get_app().test_client().post("/record" , json = test_time_series_session)
    assert res.status_code == 200
    