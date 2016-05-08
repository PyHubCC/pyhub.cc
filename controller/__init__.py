import tornado.web
from urllib.parse import urlparse
from datetime import datetime
import time
class BaseController(tornado.web.RequestHandler):
    FLASH_KEY = 'FL'


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
            public:
        }
        """
        link = dict(
            host = urlparse(data['link']).netloc,
            thumb = '',
            author = '雨神',
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
            points=0,
            date = datetime.today().strftime("%Y-%m-%d")
        )
