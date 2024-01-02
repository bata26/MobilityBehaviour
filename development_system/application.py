from dotenv import load_dotenv
from .controller.development_system import DevelopmentSystem

load_dotenv()
if __name__ == '__main__':
    DevelopmentSystem().run()
