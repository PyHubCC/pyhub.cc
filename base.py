import os
import tornado.web
from _config import Env
from controller.helper import GitHub
import tornado.web
from model import DB
__all__ = ['BaseApplication']
_ROOT = os.path.dirname(__file__)
ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

class PyHub404(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('404.html')

class BaseApplication(tornado.web.Application):
    def __init__(self, handlers):
        settings = dict(
            template_path=ROOT_JOIN('templates'),
            static_path=ROOT_JOIN('static'),
            debug=True,
            cookie_secret=Env.COOKIE_SEC,
            admin_user=Env.ADMIN_USER,
            default_handler_class=PyHub404,
            default_avatar = Env.AVATAR,
        )
        settings.update({'X-Spider-Key': Env.POST_KEY})
        super(BaseApplication, self).__init__(handlers=handlers, **settings)
        self.db = DB(Env)
        self.github = GitHub(Env.GITHUB_ID, Env.GITHUB_SEC, Env.GITHUB_REDIRECT)

