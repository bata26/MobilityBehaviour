import os
import sys
import pytest
sys.path.insert(0, r'../../segregation_system')
from src.balancing_report_generator import BalancingReportGenerator

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
    generator = BalancingReportGenerator()
    info = generator.generate_chart(test_dataset)

    assert os.path.isfile("./data/balancing/balancing_chart.png") == True

    assert info['shopping_items_number'] == 10
    assert info['sport_items_number']  == 0
    assert info['cooking_items_number'] == 0
    assert info['gaming_items_number'] == 0
    assert info['shopping_average'] == 1.0
    assert info['sport_average'] == 0
    assert info['cooking_average'] == 0
    assert info['gaming_average'] == 0
    assert info['threshold'] == 50

    result = generator.generate_report(info)
    assert result is True
    assert os.path.isfile("./data/balancing/balancing_report.json")
