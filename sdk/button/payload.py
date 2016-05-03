class ButtonPayload:
    def __init__(self, text=None, buttons=None):
        buttons = [button.json for button in buttons]
        self.json = {**{'template_type': 'button'}, **{k: v for k, v in locals().items() if v is not None}}
        del self.json['self']
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
