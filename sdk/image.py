class ImagePayload:
    def __init__(self, url):
        self.json = locals()
        del self.json['self']