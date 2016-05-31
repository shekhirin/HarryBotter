from threading import Thread
from sdk import *
from .queries.processor import process_text
import logging
from utils.text_formatter import restrict_len
from utils.mongo import Mongo


class Handler:
    def __init__(self, facebook):
        self.facebook = facebook
        self.mongo = Mongo('userLocations')

    def process(self, event):
        logging.info('Processing ' + str(event))
        user_id = event['sender']['id']
        if not self.mongo.check_user_location_exists(user_id) and self.mongo.check_user_ready(
                user_id):
            if 'text' in event['message'] and event['message']['text'] == 'NO':
                self.mongo.insert_user_wants(user_id, False)
                self.send('Если вы все же решите получить доступ, отправьте свое местоположение', user_id)
                return
        elif not self.mongo.check_user_location_exists(user_id) and self.mongo.check_user_wants(user_id):
            self.mongo.insert_user_ready(user_id, True)
            self.send(
                'Отправьте свое местоположение или "NO", если не желаете получить доступ к погоде в своем регионе',
                user_id)
            return
        if 'text' in event['message']:
            data = event['message']['text']
            data = process_text(data, {'user_id': user_id})
        elif 'attachments' in event['message']:
            if len(event['message']['attachments']) > 1:
                data = 'Only 1 attachment!'
            else:
                user_attachment = event['message']['attachments'][0]
                if user_attachment['type'] == 'location':
                    if not self.mongo.check_user_location_exists(
                            user_id) or self.mongo.check_user_ready(user_id):
                        self.mongo.insert_user_location(user_id,
                                                        user_attachment['payload']['coordinates'])
                        self.mongo.insert_user_wants(user_id, True)
                        data = 'Ваше местоположение успешно установлено!'
                    else:
                        data = Attachment(
                            type='location',
                            payload=LocationPayload(user_attachment['payload']['coordinates'])
                        )
                elif user_attachment['type'] == 'image':
                    data = Attachment(
                        type='image',
                        payload=ImagePayload(url=user_attachment['payload']['url'])
                    )
                else:
                    data = process_text('sendsorryplease')
        else:
            data = process_text('sendsorryplease')
        self.send(data, user_id)

    def send(self, data, to):
        def start_thread(inp):
            args = []
            if inp['type'] == 'image':
                args.append(Message(Recipient(to),
                                    Attachment(type='image', payload=ImagePayload(url=inp['content']))))
            elif inp['type'] == 'text':
                text = restrict_len(inp['content'])
                args.append(Message(Recipient(to), text))
            if 'url' in inp:
                url = restrict_len(inp['url'])
                args.append(Message(Recipient(to), url))
            Thread(target=self.facebook.message, args=(args,)).start()

        if type(data) is str:
            Thread(target=self.facebook.message,
                   args=(
                       Message(Recipient(to), restrict_len((data[:data.rfind('\n')] if '\n' in data else data))),)
                   ).start()
        elif type(data) is Attachment:
            Thread(target=self.facebook.message,
                   args=(Message(Recipient(to), data),)).start()
        elif type(data) is list:
            map(start_thread, data)
        elif type(data) is dict:
            start_thread(data)
