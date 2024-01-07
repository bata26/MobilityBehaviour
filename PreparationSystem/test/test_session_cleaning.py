import sys
import pytest
import numpy as np
sys.path.insert(0, r'..')
from src.session_cleaning import SessionCleaning

@pytest.fixture
def test_raw_session():
    return {
            "uuid" : "wrwewr-ewrewr-werwrew-werrwe",
            "time_series" : [-1] + list(range(2, 100)) + [None] + list(range(102, 1237)),
            "calendar" : "shopping",
            "environment" : "slippery",
            "pressure_dected" : "Regular"}

def test_session_cleaning(test_raw_session):
    cleaner = SessionCleaning()
    assert cleaner.correct_missing_samples(time_series = test_raw_session["time_series"]) is True
    cleaner.correct_outliers(time_series = test_raw_session["time_series"])
    assert np.max(test_raw_session["time_series"]) == 3
    assert np.min(test_raw_session["time_series"]) == 0
