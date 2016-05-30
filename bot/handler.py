from threading import Thread
from sdk import *
from .queries.processor import process_text
import logging
from utils.text_formatter import restrict_len


class Handler:
    def __init__(self, facebook):
        self.facebook = facebook

    def process(self, event):
        logging.info('Processing ' + str(event))
        data = ''
        if 'text' in event['message']:
            data = event['message']['text']
            data = process_text(data)
        elif 'attachments':
            if len(event['message']['attachments']) > 1:
                data = 'Only 1 attachment!'
            else:
                data = Attachment(
                    type=event['message']['attachments'][0]['type'],
                    payload=ImagePayload(url=event['message']['attachments'][0]['payload']['url'])
                )
        self.send(data, event['sender']['id'])

    def send(self, data, to):
        def start_thread(inp):
            args = []
            if inp['type'] is 'image':
                args.append(Message(Recipient(to),
                                    Attachment(type='image', payload=ImagePayload(url=inp['content']))))
            elif inp['type'] is 'text':
                text = restrict_len(inp['content'])
                args.append(Message(Recipient(to), text))
            if 'url' in inp:
                url = restrict_len(inp['url'])
                args.append(Message(Recipient(to), url))
            Thread(target=self.facebook.message, args=(args,)).start()

        if type(data) is str or type(data) is Attachment:
            Thread(target=self.facebook.message,
                   args=(Message(Recipient(to), restrict_len(data[:data.rfind('\n')])),)).start()
        elif type(data) is list:
            map(start_thread, data)
        elif type(data) is dict:
            start_thread(data)
