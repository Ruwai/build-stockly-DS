from .app import create_app
# from .tables import *
# from .sentiment import *
# from .derekscode import *
# from .preprocess import *
# from .tweetsDB import *
# from .models import *
# from .run_worker import *
from .run_worker import connect_worker

WORKER = connect_worker()

APP = create_app()