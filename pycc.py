from __future__ import absolute_import

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from _config import Env
from base import BaseApplication

from controller import BaseController
from controller.helper import JSONEncoder
from controller.api import APIPost, MsgPost, WebHookHandler, CommentAPI, FavHandler
from controller.admin import AdminController
import re


define("port", default=8080, type=int)
define("env", default='dev', type=str)


class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/u/(\w*)', UserPage),
            (r'/py/(\w+)', DetailHandler),
            (r'/logout', LogoutHandler),
            (r'/share/([0-9]*)', ShareHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
            (r'/act/(\w+)', FavHandler),
            (r'/admin', AdminController),
            (r'/new', NewHandler),
            (r'/api/v1/post_data', APIPost),
            (r'/api/v1/msg', MsgPost),
            (r'/api/v1/comment/(\w*)', CommentAPI)
        ]
        super(Application, self).__init__(handlers)
# '/' => Home page
class HomeHandler(BaseController):
    def fake_login(self):
        self.set_secure_cookie('nick', 'Yushneng')
        self.set_secure_cookie('uid', 'rainyear')

    async def get(self):
        if options.env == 'dev' :
            self.fake_login()

        nick = self.get_secure_cookie('nick')
        uid  = self.get_secure_cookie('uid')
        github_url = self.application.github.login_url
        res = await self.application.db.get_links()
        events = await self.application.db.get_events()
        users = await self.application.db.get_new_users()

        render_data = dict(
            title='首页',
            login_url=github_url,
            json=self.json_encode(res),
            nick=nick,
            uid = uid,
            admin = self.is_admin(),
            events=self.json_encode(events),
            users=self.json_encode(users)
        )

        self.render("home.html", **render_data)

    def post(self, *args, **kwargs):
        self.redirect("/")
# '/u/uid' => User Page
class UserPage(BaseController):
    async def get(self, uid):
        cuid = self.get_secure_cookie('uid').decode()
        if not uid:
            self.redirect("/u/{}".format(cuid))
        user = await self.application.db.get_user_by_uid(uid)
        is_self = 0
        if not user:
            user = {'nick': 'None'}
            favs = []
        else:
            favs = await self.application.db.get_favs_by_uid(uid)
            if cuid == uid:
                is_self = 1

        render_data = dict(
            title='{} \'s Home'.format(user['nick']),
            login_url=self.application.github.login_url,
            uid=cuid,
            nick=self.get_secure_cookie('nick'),

            favs = self.json_encode(favs),
            is_self=is_self,
        )
        self.render("user.html", **render_data)
    async def post(self, *args, **kwargs):
        uid = self.get_secure_cookie('uid').decode()
        if not uid:
            self.write({'status': 403})
        action = self.get_body_argument('action')
        if action == 'DEL':
            link_id = self.get_body_argument('_id')
            if not link_id:
                self.write({'status': -1})
            print('remove', link_id, uid)
            await self.application.db.remove_fav_link_from_uid(link_id, uid)
        elif action == 'LOAD':
            pass
        else:
            self.write({'status': 202})
# '/py/link_id' => detail page
class DetailHandler(BaseController):
    async def get(self, link_id):
        if not link_id:
            self.redirect('/404')
        link = await self.application.db.get_link_by_id(link_id)
        if not link:
            self.redirect('/404')
        render_data = dict(
            title = link['title'],
            link  = link,
            **self.default_data
        )
        self.render('detail.html', **render_data)


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



class NewHandler(BaseController):
    def get(self, *args, **kwargs):
        nick = self.get_secure_cookie('nick')
        uid  = self.get_secure_cookie('uid')
        github_url = self.application.github.login_url
        render_data = dict(
            title = '分享 Python 链接',
            uid   = uid,
            nick = nick,
            login_url= github_url
        )
        self.render("create.html", **render_data)
    async def post(self, *args, **kwargs):
        uid = self.get_secure_cookie('uid')
        if isinstance(uid, bytes):
            uid = uid.decode()
        if not uid:
            self.write(JSONEncoder().encode({'status': 403}))

        link = self.get_body_argument('link')
        title = re.sub(r'\s', ' ', self.get_body_argument('title'))
        abstract = re.sub(r'\s', ' ', self.get_body_argument('abstract'))

        if len(link)*len(title)*len(abstract) == 0:
            self.write(JSONEncoder().encode({'status': 0}))
        else:
            data = self.make_link(dict(
                link = link,
                title = title,
                abstract = abstract,
                via = self.get_secure_cookie('nick').decode()
            ))
            success = await self.application.db.save_link(data)
            if not success:
                self.write(JSONEncoder().encode({'status': 302, 'msg': 'existed!'}))
            else:
                self.write(JSONEncoder().encode({'status': 200, 'link': link}))

def main():
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()