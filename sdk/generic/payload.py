class GenericPayload:
    def __init__(self, elements):
        elements = [element.json for element in elements]
        self.json = {**{'template_type': 'generic'}, **locals()}
        del self.json['self']
        for k, v in self.json.items():
            if hasattr(v, 'json'):
                self.json[k] = v.json
