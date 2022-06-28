import os

import dotenv
dotenv.load_dotenv()


os.environ["RICARDOBOT_ROOT_PATH"] = os.path.dirname(os.path.abspath(__file__))