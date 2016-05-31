from threading import Thread
from sdk import *
from .queries.processor import process_text
import logging
from utils.text_formatter import restrict_len
from utils.mongo import Mongo


class Handler:
    def __init__(self, facebook, config):
        self.facebook = facebook
        self.mongo = Mongo('userLocations')
        self.callback = None
        self.config = config

    def set_lang(self, event):
        if event['message']['text'] not in self.config['languages']:
            try:
                self.check()
            except BaseException:
                return
        else:
            self.mongo.user_made_first_contact(True)
            self.mongo.set_lang(event['message']['text'])
            self.send(self.config['languages'][self.mongo.get_user_lang()]['lang_install_success'])
            self.callback = None
            self.mongo.insert_user_ready(True)
            self.mongo.set_awaiting(False)
            self.send(self.config['languages'][self.mongo.get_user_lang()]['send_location'])

    def check(self):
        if self.mongo.is_user_first_contact():
            self.send_and_wait_response('What is your language? (russian/english)')
            self.callback = self.set_lang
            raise BaseException

    def process(self, event):
        logging.info('Processing ' + str(event))
        self.mongo.user_id = event['sender']['id']
        if self.mongo.is_awaiting():
            if 'message' in event and self.callback is not None:
                self.callback(event)
                return
        try:
            self.check()
        except BaseException:
            return
        if not self.mongo.is_user_location_exists() and self.mongo.is_user_wants():
            if self.mongo.is_user_ready() and 'text' in event['message'] and event['message']['text'] == 'NO':
                self.mongo.insert_user_wants(False)
                self.send(self.config['languages'][self.mongo.get_user_lang()]['if_send_location'])
                return
            else:
                self.mongo.insert_user_ready(True)
                self.send_and_wait_response(self.config['languages'][self.mongo.get_user_lang()]['send_location'])
                return
        if 'text' in event['message']:
            data = event['message']['text']
            data = process_text(data, {'user_id': self.mongo.user_id})
        elif 'attachments' in event['message']:
            if len(event['message']['attachments']) > 1:
                data = 'Only 1 attachment!'
            else:
                user_attachment = event['message']['attachments'][0]
                if user_attachment['type'] == 'location':
                    if not self.mongo.is_user_location_exists() or self.mongo.is_user_ready():
                        self.mongo.insert_user_location(user_attachment['payload']['coordinates'])
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
        self.send(data)

    def send_and_wait_response(self, data):
        self.send(data)
        self.mongo.set_awaiting(True)

    def send(self, data):
        to = self.mongo.user_id

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
