import sys
from src.ingestion_system import IngestionSystem

if __name__ == '__main__':
    ingestion_system = IngestionSystem()
    try:
        while True:
            ingestion_system.run()
    except KeyboardInterrupt:
        print("Ingestion App terminated")
        sys.exit(0)    