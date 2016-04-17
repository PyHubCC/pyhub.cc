import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from _config import ENV
from base import BaseApplication

define('port', default=8081, type=int)

class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler)
        ]
        super(Application, self).__init__(handlers)

# 'admin.*/' => Admin Home Page
class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello admin")
def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=(ENV == 'pub'))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()

