from __future__ import absolute_import

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from _config import Env
from base import BaseApplication

from controller import BaseController
from controller.helper import WebHookHandler, JSONEncoder
from controller.api import APIPost


define("port", default=8080, type=int)

class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/share/([0-9]*)', ShareHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
            (r'/api/v1/post_data', APIPost),
        ]
        super(Application, self).__init__(handlers)
# '/' => Home page
class HomeHandler(BaseController):
    async def get(self):
        res = await self.application.db.get_links()
        self.render("home.html", title='PyHub.cc', links=res, json=JSONEncoder().encode(res))
    def post(self, *args, **kwargs):
        self.redirect("/")

# '/share/page_no' => Share page
class ShareHandler(BaseController):
    async def post(self, page_no):
        page_no = int(page_no)
        res = await self.application.db.get_links(page_no=page_no)
        self.write(JSONEncoder().encode(res))

# '/oauth/github' => login with GitHub
class OAuthGitHubHandler(BaseController):
    def get(self, *args, **kwargs):
        self.write("Under development!")

def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=(Env.env == 'pub'))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()