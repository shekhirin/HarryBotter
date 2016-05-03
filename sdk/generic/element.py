class GenericElement:
    def __init__(self, title, item_url=None, image_url=None, subtitle=None, buttons=None):
        buttons = [button.json for button in buttons]
        self.json = {k: v for k, v in locals().items() if v is not None}
        del self.json['self']
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
