import os
import urllib.parse as URL
from redis import Redis
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from .derekscode import predict_technical
from .preprocess import Magic
from .sentiment import TS

listen = ['default']
redis_url = os.getenv('REDISTOGO_URL')
if not redis_url:
    raise RuntimeError('Set up Redis To Go first.')
URL.uses_netloc.append('redis')
url = URL.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)
Q = Queue(connection=conn)

Q.enqueue

# try this
def connect_worker():
    with Connection(conn):
        worker = Worker(map(Q, listen))
        worker.work()