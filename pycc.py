import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import os.path
import subprocess

_ROOT = os.path.dirname(__file__)
_ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

define("port", default=8080, type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
        ]
        settings = dict(
            template_path=_ROOT_JOIN('templates'),
            static_path=_ROOT_JOIN('static'),
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
            subprocess.call("git pull", shell=True)
        if self.request.headers.get('X-GitHub-Event') == 'push':
            print("Execute git pull github master")
            subprocess.call("git pull github master", shell=True)
        else:
            print(self.request.headers.get('X-Coding-Event'))
            self.write("Bye")
    def get(self, *args, **kwargs):
        self.write("What're u looking 4?")
class OAuthGitHubHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write("Under development!")

def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()