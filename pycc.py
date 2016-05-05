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
            (r'/u/(\w+)', UserPage),
            (r'/fav/(\w+)', FavHandler),
            (r'/logout', LogoutHandler),
            (r'/share/([0-9]*)', ShareHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
            (r'/api/v1/post_data', APIPost),
        ]
        super(Application, self).__init__(handlers)
# '/' => Home page
class HomeHandler(BaseController):
    def fake_login(self):
        self.set_secure_cookie('nick', 'Yushneng')
        self.set_secure_cookie('uid', 'rainyear')

    async def get(self):
        # self.fake_login()

        nick = self.get_secure_cookie('nick')
        uid  = self.get_secure_cookie('uid')
        github_url = self.application.github.login_url
        res = await self.application.db.get_links()

        render_data = dict(
            title='PyHub.cc',
            login_url=github_url,
            json=JSONEncoder().encode(res),
            nick=nick,
            uid = uid
        )

        self.render("home.html", **render_data)

    def post(self, *args, **kwargs):
        self.redirect("/")
# '/u/uid' => User Page
class UserPage(BaseController):
    def get(self, uid):
        self.write("Comming..."+uid)

# '/share/page_no' => Share page
class ShareHandler(BaseController):
    async def post(self, page_no):
        page_no = int(page_no)
        res = await self.application.db.get_links(page_no=page_no)
        self.write(JSONEncoder().encode(res))

# '/oauth/github' => login with GitHub
class OAuthGitHubHandler(BaseController):
    async def get(self, *args, **kwargs):
        code = self.get_argument('code')
        if not code:
            self.redirect("/")
        else:
            access_token = self.application.github.access_token(code)
            if access_token.get('access_token'):
                # get user info
                user = self.application.github.get_user(access_token.get('access_token'))
                user = self.make_user(user)
                await self.application.db.save_user(user)
                self.set_secure_cookie('nick', user['nick'])
                self.set_secure_cookie('uid', user['uid'])
                self.redirect("/")
            else:
                self.write("授权失败!".format(access_token))
# '/logout' => Logout action
class LogoutHandler(BaseController):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/")

# '/fav/link_id' => Fav action
class FavHandler(BaseController):

    def get(self, link_id):
        pass
    async def post(self, link_id):

        uid = self.get_secure_cookie('uid')
        if not uid:
            self.write(JSONEncoder().encode({'status': 403}))
        else:
            # update vote
            await self.application.db.fav_link(link_id, uid)
            self.write(JSONEncoder().encode({'status': 200}))



def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=(Env.env == 'pub'))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()