from bottle import post, request, run, get
from bot import Handler
from utils import Config, Facebook, SSLWebServer
import logging

config = Config()
facebook = Facebook(config['messenger_access_token'])
handler = Handler(facebook)

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='output.log')
logging.getLogger("requests").setLevel(logging.WARNING)


@post('/' + config['webhook_url'])
def post():
    entries = request.json
    for entry in entries['entry']:
        for event in entry['messaging']:
            if 'message' not in event:
                continue
            handler.process(event)


@get('/' + config['webhook_url'])
def get():
    if request.GET['hub.verify_token'] == '18731293187':
        return request.GET['hub.challenge']
    else:
        return 'Error, invalid token'


srv = SSLWebServer(fullchain=config['fullchain'], privkey=config['privkey'], host='0.0.0.0', port=8000)
run(server=srv, reloader=True, debug=False)
