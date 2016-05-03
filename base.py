import os
import tornado.web
from _config import Env
import motor.motor_tornado

__all__ = ['BaseApplication']
_ROOT = os.path.dirname(__file__)
ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

class DB:
    def __init__(self):
        self._client = motor.motor_tornado.MotorClient('localhost', 27017)
        self.db = self._client[Env.DB_NAME]
        self.link_collection = self.db[Env.COL_LINK]

    async def get_links(self, page_no=1, page_size=30):
        query = dict(
            public = True,
        )
        res = {'count': 0, 'links': []}
        res['count'] = await self.link_collection.find(query).count()
        async for link in self.link_collection.find(query).sort('date').limit(page_size).skip((page_no-1)*page_size):
            res['links'].append(link)
        return res

    async def find_link_by_title(self, title):
        return await self.link_collection.find_one({'title': title})
    async def save_link(self, data):
        """
        API use
        """
        if len(data['title']) == 0:
            return False
        exist = await self.find_link_by_title(data['title'])
        if not bool(exist):
            return await self.link_collection.insert(data)
        else:
            return False

class BaseApplication(tornado.web.Application):
    def __init__(self, handlers):
        settings = dict(
            template_path=ROOT_JOIN('templates'),
            static_path=ROOT_JOIN('static'),
            debug=True,
        )
        settings.update({'X-Spider-Key': Env.POST_KEY})
        super(BaseApplication, self).__init__(handlers=handlers, **settings)
        self.db = DB()

