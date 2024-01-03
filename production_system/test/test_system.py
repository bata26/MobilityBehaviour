import os
import sys
import pytest
from dotenv import load_dotenv
sys.path.insert(0, r'../../production_system')
from controller.production_system import ProductionSystem
from model.msg_manager import MessageManager
from model.prepared_session import PreparedSession
from controller.classify_controller import ClassifyController
load_dotenv()

@pytest.fixture
def message_manager():
    return MessageManager.get_instance()

@pytest.fixture
def prepared_session():
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
@pytest.fixture
def test_file():
    return  {'file': open("NN0.joblib",'rb')}

def test_system_flow(message_manager, prepared_session, test_file):
    res = message_manager.get_app().test_client().post("/deploy" , files = test_file)
    assert res.status_code == 200
    assert os.path.isfile("./classifier/NN0.joblib") is True
    res = message_manager.get_app().test_client().post("/prepared_session" , json = prepared_session)
    assert res.status_code == 200
