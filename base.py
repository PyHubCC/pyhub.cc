import os
import tornado.web
from _config import Env
import motor.motor_tornado

__all__ = ['BaseApplication']
_ROOT = os.path.dirname(__file__)
ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

class BaseApplication(tornado.web.Application):
    def __init__(self, handlers):
        settings = dict(
            template_path=ROOT_JOIN('templates'),
            static_path=ROOT_JOIN('static'),
            debug=True
        )
        super(BaseApplication, self).__init__(handlers=handlers, **settings)
        self._client = motor.motor_tornado.MotorClient()
        self.db = self._client[Env.DB_NAME]

