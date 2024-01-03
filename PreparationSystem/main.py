import sys
from src.preparation_system import PreparationSystem

if __name__ == '__main__':
    preparation_system = PreparationSystem()
    try:
        preparation_system.run()
    except KeyboardInterrupt:
        print("Ingestion App terminated")
        sys.exit(0)    