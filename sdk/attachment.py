class Attachment:
    def __init__(self, type, payload):
        self.json = locals()
        del self.json['self']
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
