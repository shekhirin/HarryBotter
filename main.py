from bottle import Bottle, request, response
from bot import Handler
from utils import Config, Facebook
from datetime import datetime
from functools import wraps
import logging.config
import yaml
from werkzeug.serving import run_simple, WSGIRequestHandler

config = Config()
facebook = Facebook(config['messenger_access_token'])
handler = Handler(config, facebook)

logging.config.dictConfig(yaml.load(open('loggers_config.yml')))

access_logger = logging.getLogger('access')


def log_to_logger(fn):
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
        request_time = datetime.now()
        actual_response = fn(*args, **kwargs)
        access_logger.info('%s - - %s "%s %s" %s -' % (request.remote_addr,
                                                       request_time.strftime('[%d/%b/%Y:%H:%M:%S +0300]'),
                                                       request.method,
                                                       request.url,
                                                       response.status_code))
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


class QuietHandler(WSGIRequestHandler):
    def log_request(self, code='-', size='-'): pass


run_simple('0.0.0.0', 8000, app, use_reloader=True, ssl_context=(config['fullchain'], config['privkey']),
           request_handler=QuietHandler)
