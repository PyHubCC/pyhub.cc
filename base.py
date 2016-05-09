import os
import time
import tornado.web
from _config import Env
import motor.motor_tornado
from controller.helper import GitHub
from bson import objectid
from datetime import datetime
import pytz
__all__ = ['BaseApplication']
_ROOT = os.path.dirname(__file__)
ROOT_JOIN = lambda sub: os.path.join(_ROOT, sub)

class DB:
    def __init__(self):
        self._client = motor.motor_tornado.MotorClient('localhost', 27017)
        self.db = self._client[Env.DB_NAME]
        self.link_collection = self.db[Env.COL_LINK]
        self.user_collection = self.db[Env.COL_USER]
        self.event_collection = self.db[Env.COL_EVENT]
        self.msg_collection = self.db['msg']

    @property
    def date(self):
        return datetime.today().strftime("%m/%d")
    @property
    def timestamp(self):
        return datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%m-%d:%H:%M:%S")

    async def get_new_msgs(self, n=5):
        msgs = []
        async for m in self.msg_collection.find({}).sort('date', -1).limit(n):
            msgs.append(m)
        return msgs
    async def save_msg(self, content = '', user = '', uid = ''):
        msg = dict(
            user= user,
            uid = uid,
            content= content,
            date= int(time.time()),
            timestamp = self.timestamp
        )
        await self.msg_collection.insert(msg)
        return msg
    async def get_new_users(self, n=5):
        users = []
        async for u in self.user_collection.find({}).sort('date', -1).limit(n):
            users.append(u)
        return users

    async def get_top_users(self, n=10):
        users=[]
        async for u in self.user_collection.find({}).sort('date', 1).limit(n):
            users.append(u)
        return users

    async def save_event(self, msg):
        await self.event_collection.insert({'msg': msg, 'timestamp': int(time.time()), 'date': self.date})
    async def get_events(self):
        events = []
        async for e in self.event_collection.find({}).sort('timestamp', -1).limit(3):
            events.append(e)
        return events
    async def get_link_by_id(self, link_id):
        return await self.link_collection.find_one({'_id': objectid.ObjectId(link_id)})
    async def del_link(self, link_id):
        await self.link_collection.update({'_id': objectid.ObjectId(link_id)},
                                          {'$set': {'public': False}})
    async def fav_link(self, link_id, uid):
        exist = await self.get_link_by_id(link_id)
        if bool(exist):
            # update fav list
            await self.link_collection.update({'_id': objectid.ObjectId(link_id)},
                                              {'$inc': {'favs': 1},
                                               '$push': {'favlist': uid}})
            await self.user_collection.update({'uid': uid},
                                              {'$push': {'favlist': link_id}})

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
        async for link in self.link_collection.find(query).sort('rank', -1).limit(page_size).skip((page_no-1)*page_size):
            links.append(link)
        return links

    async def find_link_by_title_or_link(self, title, link):
        return await self.link_collection.find_one({'$or': [{'title': title}, {'link': link}]})
    async def save_link(self, data):
        """
        API use
        """
        # print("Insert {}".format(data))
        if len(data['title']) == 0:
            return False
        exist = await self.find_link_by_title_or_link(data['title'], data['link'])
        if not bool(exist):
            return await self.link_collection.insert(data)
        else:
            if not exist['public']:
                await self.link_collection.remove({"_id": objectid.ObjectId(exist['_id'])})
                return await self.link_collection.insert(data)
            return False

class BaseApplication(tornado.web.Application):
    def __init__(self, handlers):
        settings = dict(
            template_path=ROOT_JOIN('templates'),
            static_path=ROOT_JOIN('static'),
            debug=True,
            cookie_secret=Env.COOKIE_SEC,
            admin_user=Env.ADMIN_USER,
        )
        settings.update({'X-Spider-Key': Env.POST_KEY})
        super(BaseApplication, self).__init__(handlers=handlers, **settings)
        self.db = DB()
        self.github = GitHub(Env.GITHUB_ID, Env.GITHUB_SEC, Env.GITHUB_REDIRECT)

