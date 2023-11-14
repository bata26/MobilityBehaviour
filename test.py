import pytest
from testScore import getAccuration

scoreThreshold = {0.5 , 0.75 , 0.95}

@pytest.mark.parametrize('th' , scoreThreshold)
def testAccuration(th):
    