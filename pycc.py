from __future__ import absolute_import

import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
from base import BaseApplication

from controller import BaseController
from controller.helper import JSONEncoder
from controller.api import APIPost, MsgPost, WebHookHandler, CommentAPI, FavHandler, APIPoints
from controller.admin import AdminController
import re


define("port", default=8080, type=int)
define("env", default='dev', type=str)


class Application(BaseApplication):
    def __init__(self):
        handlers = [
            (r'/(|pin|topics)', HomeHandler),
            (r'/u/(\S+)', UserPage),
            (r'/topusers', TopUserHandler),
            (r'/py/(\w+)', DetailHandler),
            (r'/topic/(\S+)', TopicHandler),
            (r'/logout', LogoutHandler),
            (r'/share/([0-9]*)', ShareHandler),
            (r'/more_pin/(\S+)', MorePinHandler),
            (r'/web_hook/coding_git', WebHookHandler),
            (r'/web_hook/github_push', WebHookHandler),
            (r'/oauth/github', OAuthGitHubHandler),
            (r'/act/(\w+)', FavHandler),
            (r'/admin', AdminController),
            (r'/new', NewHandler),
            (r'/write/?(\w*)', WriteHandler),
            (r'/api/v1/post_data', APIPost),
            (r'/api/v1/msg', MsgPost),
            (r'/api/v1/comment/(\w*)', CommentAPI),
            (r'/api/v1/points', APIPoints)
        ]
        super(Application, self).__init__(handlers)
# '/' => Home page
class HomeHandler(BaseController):
    def fake_login(self):
        self.set_secure_cookie('nick', 'Yushneng')
        self.set_secure_cookie('uid', 'rainyear')

    async def get(self, tab):
        if options.env == 'dev':
            self.fake_login()

        tabs = {
            'share': '',
            'pin': ' : 每日推荐',
            'topics': ' : 专题分类',
        }
        tab = tab or 'share'
        if tab not in ['share', 'pin', 'topics']:
            self.redirect('/404')

        nick = self.get_secure_cookie('nick')
        uid  = self.get_secure_cookie('uid')
        github_url = self.application.github.login_url


        events = await self.application.db.get_events()
        users = await self.application.db.get_new_users()
        topic_metas = await self.application.db.get_topic_metas()

        render_data = dict(
            title='首页' + tabs[tab],
            login_url=github_url,
            nick=nick,
            uid = uid,
            admin = self.is_admin(),
            events=self.json_encode(events),
            users=self.json_encode(users),
            topic_metas = self.json_encode(topic_metas),
            page = tab,
        )

        links = []
        if tab == 'share':
            links = await self.application.db.get_links()
        elif tab == 'pin':
            links = await self.application.db.get_pro_links_by_date()
        render_data['json'] = self.json_encode(links)

        self.render("{}.html".format(tab), **render_data)

    async def post(self, tab):
        if tab == 'pin':
            date = self.get_body_argument('date')
            links = await self.application.db.get_pro_links_by_date(date)
            self.write({'links': links})
        else:
            self.write({'status': 404})

# '/u/uid' => User Page
class UserPage(BaseController):
    async def get(self, uid):
        cuid = self.get_secure_cookie('uid')
        if cuid is not None:
            cuid = cuid.decode()
        if not uid:
            self.redirect("/404")
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
            title='{}\'s Home'.format(user['nick']),
            login_url=self.application.github.login_url,
            uid=cuid,
            nick=self.get_secure_cookie('nick'),
            user=user,

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
        link['_id'] = str(link['_id'])
        if not link:
            self.redirect('/404')
        render_data = dict(
            title = link['title'],
            link  = link,
        )
        self.render('detail.html', **{**self.default_data, **render_data})


# '/share/page_no' => Load more shares
class ShareHandler(BaseController):
    async def post(self, page_no):
        page_no = int(page_no)
        res = await self.application.db.get_links(page_no=page_no)
        self.write(JSONEncoder().encode(res))
# '/more_pin/date' => Load more pins
class MorePinHandler(BaseController):
    async def post(self, date):
        print(date)
        links = await self.application.db.get_pro_links_by_date(date)
        self.write(dict(links = links))

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
                self.set_secure_cookie('avatar', user['avatar'])
                self.redirect("/")
            else:
                self.write("授权失败!".format(access_token))
# '/logout' => Logout action
class LogoutHandler(BaseController):
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        self.redirect("/")


# '/new' => share a link
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
                via = self.get_secure_cookie('nick').decode(),
                via_uid = self.get_secure_cookie('uid').decode(),
                via_avatar = self.get_secure_cookie('avatar').decode(),
            ))
            success = await self.application.db.save_link(data)
            if not success:
                self.write(JSONEncoder().encode({'status': 302, 'msg': 'existed!'}))
            else:
                self.write(JSONEncoder().encode({'status': 200, 'link': link}))

# '/topic/slug' => topic page
class TopicHandler(BaseController):
    def get(self, slug):
        self.write('topic {}'.format(slug))
# '/topusers' => 排行
class TopUserHandler(BaseController):
    async def get(self):
        topusers = await self.application.db.get_top_users()
        render_data = dict(
            title='用户排行榜',
            topusers = topusers,
        )
        self.render('topuser.html', **{**self.default_data, **render_data})
# '/write' => 创作
class WriteHandler(BaseController):
    async def get(self, page_id):

        topics = await self.application.db.get_topic_metas()
        render_data = dict(
            topics =  topics,
            title = '投稿'
        )
        self.render('write.html', **{**self.default_data, **render_data})
    async def post(self, *args, **kwargs):

        pass

def main():
    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    main()