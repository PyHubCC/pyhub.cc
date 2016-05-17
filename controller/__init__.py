import tornado.web
from urllib.parse import urlparse
from datetime import datetime
from .helper import JSONEncoder
import time
import re
class BaseController(tornado.web.RequestHandler):
    FLASH_KEY = 'FL'

    @property
    def default_data(self):
        return dict(
            title="首页",
            login_url = self.application.github.login_url,
            uid = self.get_secure_cookie('uid'),
            nick = self.get_secure_cookie('nick'),
            avatar = self.get_secure_cookie('avatar'),
        )
    def json_encode(self, obj):
        return JSONEncoder().encode(obj)

    def is_admin(self):
        uid = self.get_secure_cookie('uid')
        return int(uid is not None and uid.decode() == self.application.settings.get('admin_user'))
    def auth(self, method):
        if self.get_secure_cookie('uid'):
            return method
        else:
            self.flash_msg('Login first please!')
            self.redirect('/')
    def flash_msg(self, msg=''):
        if bool(msg):
            self.set_secure_cookie(self.FLASH_KEY, msg)
        else:
            msg = self.get_secure_cookie(self.FLASH_KEY)
            self.clear_cookie(self.FLASH_KEY)
            return msg
    def make_link(self, data):
        """
        data format: {
            title:
            abstract:
            date:
            link:
            via:
            via_uid:
            public:
        }
        """
        data['abstract'] = re.sub(r'\'|"', '`', data.get('abstract') or '')
        data['title'] = re.sub(r'\'|"', '`', data.get('title') or '')
        link = dict(
            host = urlparse(data['link']).netloc,
            thumb = '',
            author = '雨神',
            via_uid = 'rainyear',
            via_avatar = self.application.settings.get('default_avatar'),
            rank   = 1,
            public = True,
            favs = 1,
            favlist = [],
            date = int(time.time())
        )
        link.update(data)
        return link
    def make_user(self, user):
        """
        user format: {
            uid:
            nick:
            avatar:
            email:
            admin: 0
            points: 0
        }
        """
        return dict(
            uid = user.get('login'),
            nick = user.get('name') or user.get('login'),
            avatar = user.get('avatar_url'),
            email = user.get('email'),
            admin= 0,
            points=20,
            date = datetime.today().strftime("%Y-%m-%d")
        )
