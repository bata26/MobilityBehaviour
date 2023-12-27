import sys
from evaluation_system import EvaluationSystem

if __name__ == '__main__':

    evaluation_system = EvaluationSystem()
    try:
        evaluation_system.run()
    except KeyboardInterrupt:
        print("Evaluation App terminated")
        sys.exit(0)
