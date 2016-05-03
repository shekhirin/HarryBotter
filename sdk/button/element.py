class ButtonElement:
    def __init__(self, type, title, url=None, payload=None):
        # TODO: raise an exception if 'url' is provided with type='postback' and vice versa
        self.json = {k: v for k, v in locals().items() if v is not None}
        del self.json['self']
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
