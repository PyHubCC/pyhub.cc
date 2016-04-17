from __future__ import absolute_import

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import subprocess
from _config import Env
from base import BaseApplication

define("port", default=8080, type=int)

class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
        ]
        super(Application, self).__init__(handlers)
class BaseHandler(tornado.web.RequestHandler):
    pass

# '/' => Home page
class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html", title='PyHub.cc')
    def post(self, *args, **kwargs):
        self.redirect("/")

# '/web_hook/github_push'
# '/web_hook/coding_git' => Webhooks
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

# '/oauth/github' => login with GitHub
class OAuthGitHubHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.write("Under development!")

def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=(Env.env == 'pub'))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()