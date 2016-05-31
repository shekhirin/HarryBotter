from bottle import Bottle, request, response
from bot import Handler
from utils import Config, Facebook, SSLWebServer
from datetime import datetime
from functools import wraps
import logging

config = Config()
facebook = Facebook(config['messenger_access_token'])
handler = Handler(config, facebook)

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='output.log')
logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('access.log')
formatter = logging.Formatter('%(msg)s')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def log_to_logger(fn):
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        logger.info('%s %s %s %s %s' % (request.remote_addr,
                                        request_time,
                                        request.method,
                                        request.url,
                                        response.status))
        return actual_response
    return _log_to_logger

app = Bottle()
app.install(log_to_logger)


@app.post('/' + config['webhook_url'])
def post():
    entries = request.json
    for entry in entries['entry']:
        for event in entry['messaging']:
            if 'message' not in event:
                continue
            handler.process(event)


@app.get('/' + config['webhook_url'])
def get():
    if request.GET['hub.verify_token'] == config['hub.verify_token']:
        return request.GET['hub.challenge']
    else:
        return 'Error, invalid token'

srv = SSLWebServer(fullchain=config['fullchain'], privkey=config['privkey'], quiet=True, host='0.0.0.0', port=8000)
app.run(server=srv, reloader=True)
