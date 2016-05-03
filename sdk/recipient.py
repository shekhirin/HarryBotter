class Recipient:
    def __init__(self, id=None, phone_number=None):
        self.json = {k: v for k, v in locals().items() if v is not None}
        del self.json['self']