import sys
from controller.evaluation_system import EvaluationSystem
from dotenv import load_dotenv

load_dotenv()
if __name__ == '__main__':

    evaluation_system = EvaluationSystem()
    try:
        evaluation_system.run()
    except KeyboardInterrupt:
        print("Evaluation App terminated")
        sys.exit(0)
