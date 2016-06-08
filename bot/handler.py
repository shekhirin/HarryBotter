from threading import Thread
from sdk import *
from .queries.processor import process_text
import logging
from utils.text import restrict_len
from utils.mongo import Mongo
from utils.config import Config
import time


class Handler:
    def __init__(self, config, facebook):
        self.facebook = facebook
        self.mongo = Mongo('users')
        self.callback = None
        self.languages = Config('languages.yml')
        self.config = config

    def set_lang(self, user_id, event):
        lang = event['message']['text'].lower().strip()
        if lang not in self.languages.keys():
            try:
                self.check(user_id)
            except BaseException:
                return
        else:
            logging.getLogger('app').log(logging.INFO, 'SET language {} to user {}'.format(lang, user_id))
            self.mongo.user_made_first_contact(user_id, True)
            self.mongo.set_lang(user_id, lang)
            self.send(user_id, self.get_phrase(user_id, 'lang_install_success'))
            time.sleep(1)
            self.callback = None
            self.mongo.insert_user_ready(user_id, True)
            self.mongo.set_awaiting(user_id, False)
            self.send(user_id, self.get_phrase(user_id, 'send_location'))

    def check(self, user_id):
        if self.mongo.is_user_first_contact(user_id):
            self.send_waiting_response(user_id, 'What is your language? ({})'.format('/'.join(self.languages.keys())))
            self.callback = self.set_lang
            raise BaseException

    def get_phrase(self, user_id, name):
        return self.languages[self.mongo.get_user_lang(user_id)][name]

    def process(self, event):
        logging.getLogger('app').log(logging.INFO, 'Processing ' + str(event))
        user_id = event['sender']['id']
        if self.mongo.is_awaiting(user_id):
            if 'message' in event and self.callback is not None:
                self.callback(user_id, event)
                return
        try:
            self.check(user_id)
        except BaseException:
            return
        if not self.mongo.is_user_location_exists(user_id) and self.mongo.is_user_wants(
                user_id) and not self.mongo.is_user_ready(user_id):
            if not self.mongo.is_user_ready(user_id):
                self.mongo.insert_user_ready(user_id, True)
                self.send_waiting_response(user_id, self.get_phrase(user_id, 'send_location'))
                return
        if 'text' in event['message']:
            data = event['message']['text']
            data = process_text(data, self.config, {'user_id': user_id})
            if type(data) is dict:
                data['content'] = data['content'].split('\n\n')
        elif 'attachments' in event['message']:
            if len(event['message']['attachments']) > 1:
                data = 'Only 1 attachment!'
            else:
                user_attachment = event['message']['attachments'][0]
                if user_attachment['type'] == 'location':
                    if not self.mongo.is_user_location_exists(user_id) or self.mongo.is_user_ready(user_id):
                        self.mongo.insert_user_location(user_id, user_attachment['payload']['coordinates'])
                        logging.getLogger('app').log(logging.INFO,
                                                     'SET location {} to user {}'.format(
                                                         self.mongo.get_user_location(user_id), user_id)
                                                     )
                        data = self.get_phrase(user_id, 'location_updated')
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
                    data = process_text('sendsorryplease', self.config)
        else:
            data = process_text('sendsorryplease', self.config)
        self.send(user_id, data)

    def send_waiting_response(self, user_id, data):
        self.send(user_id, data)
        self.mongo.set_awaiting(user_id, True)

    def send(self, user_id, data):
        to = user_id

        def start_thread(inp):
            args = []
            if inp['type'] == 'image':
                args.append(Message(Recipient(to),
                                    Attachment(type='image', payload=ImagePayload(url=inp['content']))))
            elif inp['type'] == 'text':
                text = restrict_len(inp['content'])
                args.append(Message(Recipient(to), text))
            if 'url' in inp and inp['url'] is not None:
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
            for item_data in data:
                if type(item_data) is str:
                    self.send(user_id, item_data)
                elif type(item_data) is dict:
                    item_data['content'] = item_data['content'].split('\n\n')
                    self.send(user_id, item_data)
                time.sleep(0.2)
        elif type(data) is dict:
            if type(data['content']) is list:
                for content_data in data['content']:
                    dic = data
                    dic['content'] = content_data
                    start_thread(dic)
                    time.sleep(0.2)
