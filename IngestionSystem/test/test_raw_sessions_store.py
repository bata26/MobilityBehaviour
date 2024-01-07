import sys
import pytest
sys.path.insert(0, r'..')
from src.raw_sessions_store import RawSessionsStore

@pytest.fixture
def test_label_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "pressure_detected" : "Regular",
            }

@pytest.fixture
def test_uuid():
    return "wrwewr-ewrewr-werwrew-werrwe"

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

@pytest.fixture
def test_raw_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "time_series" : list(range(1, 1237)),
            "calendar" : "shopping",
            "environment" : "slippery",
            "pressure_dected" : "Regular"}

def test_init_storing():
    store = RawSessionsStore()
    assert True

def test_get_record_type(test_label_session, test_act_session, \
                         test_env_session, test_time_series_session):
    store = RawSessionsStore()
    record_type_act = store.get_record_type(test_act_session)
    record_type_env = store.get_record_type(test_env_session)
    record_type_label = store.get_record_type(test_label_session)
    record_type_ts = store.get_record_type(test_time_series_session)

    assert record_type_env == "environment"
    assert record_type_act == "calendar"
    assert record_type_label == "pressure_detected"
    assert record_type_ts == "time_series"


def test_validate_schema_record(test_label_session, test_act_session, \
                                test_env_session, test_time_series_session):
    store = RawSessionsStore()
    assert store.validate_schema_record \
        (record=test_label_session, record_type="pressure_detected") is True
    assert store.validate_schema_record \
        (record=test_act_session, record_type="calendar") is True
    assert store.validate_schema_record \
        (record=test_env_session, record_type="environment") is True
    assert store.validate_schema_record \
        (record=test_time_series_session, record_type="time_series") is True

def test_session_exists(test_uuid):
    store = RawSessionsStore()
    result = store.raw_session_exists(uuid=test_uuid)
    assert result is False

def test_store_record(test_label_session, test_act_session, \
                      test_env_session, test_time_series_session):
    store = RawSessionsStore()
    assert store.store_record(record=test_label_session) is True
    assert store.store_record(record=test_act_session) is True
    assert store.store_record(record=test_env_session) is True
    assert store.store_record(record=test_time_series_session) is True

def test_is_session_complete(test_label_session, test_act_session, \
                             test_env_session, test_time_series_session, test_uuid):
    store = RawSessionsStore()
    store.store_record(record=test_label_session)
    store.store_record(record=test_act_session)
    store.store_record(record=test_env_session)
    store.store_record(record=test_time_series_session)
    assert store.is_session_complete \
        (uuid=test_uuid, last_missing_sample=True, evaluation=False) is True
    assert store.is_session_complete \
        (uuid=test_uuid, last_missing_sample=False, evaluation=True) is True
