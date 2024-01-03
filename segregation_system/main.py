import sys
from src.segregation_system import SegregationSystem

if __name__ == '__main__':

    segregation_system = SegregationSystem()
    try:
        segregation_system.run()
    except KeyboardInterrupt:
        print("Segregation App terminated")
        sys.exit(0)
