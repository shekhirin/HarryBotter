class LocationPayload:
    def __init__(self, coordinates):
        self.json = locals()
        del self.json['self']