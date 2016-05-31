from bottle import ServerAdapter


class SSLWebServer(ServerAdapter):
    def __init__(self, fullchain, privkey, quiet, **options):
        super().__init__(**options)
        self.quiet = quiet
        self.certfile = fullchain
        self.keyfile = privkey

    def run(self, handler):
        import ssl
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass

            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket(
            srv.socket, server_side=True,
            certfile=self.certfile,
            keyfile=self.keyfile)
        srv.serve_forever()
