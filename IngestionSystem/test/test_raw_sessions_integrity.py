import sys
import pytest
sys.path.insert(0, r'..')
from src.raw_session_integrity import RawSessionIntegrity

@pytest.fixture
def test_time_series():
    return {
        "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
        "time_series" : list(range(1, 1237))
    }

@pytest.fixture
def test_time_series_missing():
    return {
        "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
        "time_series" : list(range(1, 1235)) + [None, None]
    }

def test_mark_missing_samples(test_time_series, test_time_series_missing):
    marker = RawSessionIntegrity()
    assert marker.mark_missing_samples(time_series = test_time_series["time_series"]) is True
    assert marker.mark_missing_samples \
        (time_series = test_time_series_missing["time_series"]) is False
