from sdk import Attachment


class Message:
    def __init__(self, recipient, message, notification_type=None):
        if type(message) is str:
            message = {'text': message}
        elif type(message) is Attachment:
            message = {'attachment': message.json}
        self.json = {k: (v) for k, v in locals().items() if v is not None}
        del self.json['self']
        if len(self.json) == 0:
            raise ValueError('Both text and attachment are None')
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
