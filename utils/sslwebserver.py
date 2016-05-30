from bottle import ServerAdapter


class SSLWebServer(ServerAdapter):
    def __init__(self, fullchain, privkey, **options):
        super().__init__(**options)
        self.certfile = fullchain
        self.keyfile = privkey

    def run(self, handler):
        from wsgiref.simple_server import make_server
        import ssl
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket(
            srv.socket, server_side=True,
            certfile=self.certfile,
            keyfile=self.keyfile)
        srv.serve_forever()
