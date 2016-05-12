from bottle import post, request, run, get
from bot import Handler
from utils import Config, Facebook, SSLWebServer
import os
import logging

config = Config()
for var, value in config.items():
    os.environ[var] = str(value)
facebook = Facebook(os.environ['messenger_access_token'])
handler = Handler(facebook)
logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='output.log')


@post('/5bb893ef4003aa48b7d27965bcb32ab9faf03453f920fdb19c')
def post():
    entries = request.json
    for entry in entries['entry']:
        for event in entry['messaging']:
            if 'message' not in event:
                continue
            handler.process(event)


@get('/5bb893ef4003aa48b7d27965bcb32ab9faf03453f920fdb19c')
def get():
    if request.GET['hub.verify_token'] == '18731293187':
        return request.GET['hub.challenge']
    else:
        return 'Error, invalid token'


srv = SSLWebServer(host='0.0.0.0', port=8000)
run(server=srv, reloader=True)
