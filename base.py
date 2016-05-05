import os
import tornado.web
from _config import Env
import motor.motor_tornado
from controller.helper import GitHub

__all__ = ['BaseApplication']
_ROOT = os.path.dirname(__file__)
ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

class DB:
    def __init__(self):
        self._client = motor.motor_tornado.MotorClient('localhost', 27017)
        self.db = self._client[Env.DB_NAME]
        self.link_collection = self.db[Env.COL_LINK]
        self.user_collection = self.db[Env.COL_USER]

    async def get_user(self, uid):
        return await self.user_collection.find_one({'uid': uid})
    async def save_user(self, user):
        exist = await self.get_user(user['uid'])
        if not bool(exist):
            self.user_collection.insert(user)
    async def get_links(self, page_no=1, page_size=30):
        query = dict(
            public = True,
        )
        # res = {'count': 0, 'links': []}
        # res['count'] = await self.link_collection.find(query).count()
        links = []
        async for link in self.link_collection.find(query).sort('date').limit(page_size).skip((page_no-1)*page_size):
            links.append(link)
        return links

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
            cookie_secret=Env.COOKIE_SEC,
        )
        settings.update({'X-Spider-Key': Env.POST_KEY})
        super(BaseApplication, self).__init__(handlers=handlers, **settings)
        self.db = DB()
        self.github = GitHub(Env.GITHUB_ID, Env.GITHUB_SEC, Env.GITHUB_REDIRECT)

