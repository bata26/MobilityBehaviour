import os
import sys
import pytest
sys.path.insert(0, r'../../segregation_system')
from src.coverage_report_generator import CoverageReportGenerator

@pytest.fixture
def test_dataset():
    return [
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        },
    ]

def test_report(test_dataset):
    generator = CoverageReportGenerator()
    info = generator.generate_chart(test_dataset)

    assert os.path.isfile("./data/balancing/balancing_chart.png") == True

    assert info['maximum_pressure_ts'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    assert info['minimum_pressure_ts'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    assert info['median_pressure_ts'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    assert info['mean_absolute_deviation_pressure_ts'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    assert info['activity_and_small_scatter'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    assert info['environment_and_small_scatter'] == [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

    result = generator.generate_report(info)
    assert result is True
    assert os.path.isfile("./data/coverage/coverage_report.json")
