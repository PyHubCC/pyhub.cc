import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import os.path

_ROOT = os.path.dirname(__file__)
_ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

define("port", default=8080, type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/eb_hook/coding_git', WebHookHandler)
                    ]
        settings = dict(
            template_path=_ROOT_JOIN('templates'),
            debug=True
        )
        super(Application, self).__init__(handlers=handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass

class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html", title='PyHub.cc')
    def post(self, *args, **kwargs):
        self.redirect("/")
class WebHookHandler(BaseHandler):
    def post(self, *args, **kwargs):
        if self.request.headers.get('X-Coding-Event') == 'push':
            print("Execute git pull")


def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()