from threading import Thread
from sdk import *
from .queries.processor import process_text, process_attachment


class Handler:
    def __init__(self, facebook):
        self.facebook = facebook

    def process(self, event):
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
        Thread(target=self.facebook.message, args=(Message(Recipient(event['sender']['id']), data),)).start()
