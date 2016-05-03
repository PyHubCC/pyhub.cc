from __future__ import absolute_import

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import subprocess
from _config import Env
from base import BaseApplication
from controller import BaseController
import json

define("port", default=8080, type=int)

class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
            (r'/api/v1/post_data', APIPost),
        ]
        super(Application, self).__init__(handlers)
# '/' => Home page
class HomeHandler(BaseController):
    def get(self):
        self.render("home.html", title='PyHub.cc')
    def post(self, *args, **kwargs):
        self.redirect("/")

# '/web_hook/github_push'
# '/web_hook/coding_git' => Webhooks
class WebHookHandler(BaseController):
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
class OAuthGitHubHandler(BaseController):
    def get(self, *args, **kwargs):
        self.write("Under development!")

# '/api/v1/post_data' => Post data in
class APIPost(BaseController):
    async def post(self, *args, **kwargs):
        """
        data format: {
            title:
            abstract:
            date:
            link:
            via:
        }
        """
        print(self.request.headers.get('X-Spider-Key'))
        print(self.settings['X-Spider-Key'])
        if self.request.headers.get('X-Spider-Key') == self.settings['X-Spider-Key']:
            print(self.request.body.decode())
            data = json.loads(self.request.body.decode())
            data = self.make_link(data)
            res = await self.application.db.save_link(data)
            if bool(res):
                self.write(dict(status=0))
            else:
                self.write(dict(status=-1))
        else:
            self.write("Bye~")

def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=(Env.env == 'pub'))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()