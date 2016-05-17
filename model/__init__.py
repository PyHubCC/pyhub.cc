from bson import objectid
from datetime import datetime
import time
import pytz
import motor.motor_tornado

class DB:
    def __init__(self, Env):
        self._client = motor.motor_tornado.MotorClient('localhost', 27017)
        self.db = self._client[Env.DB_NAME]
        self.link_collection = self.db[Env.COL_LINK]
        self.user_collection = self.db[Env.COL_USER]
        self.event_collection = self.db[Env.COL_EVENT]

        self.msg_collection = self.db[Env.COL_MSG]
        self.fav_collection = self.db[Env.COL_FAV]
        self.comment_collection = self.db[Env.COL_COMMENT]
        self.topic_meta_collection = self.db[Env.COL_TOPIC_META]
        self.topic_collection = self.db[Env.COL_TOPIC]

    @property
    def date(self):
        return datetime.today().strftime("%m/%d")
    @property
    def timestamp(self):
        return datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%m-%d:%H:%M:%S")

    async def get_comments_by_link_id(self, link_id, n = 50):
        comments = []
        async for c in self.comment_collection.find({'link_id': link_id}).sort('date', 1).limit(n):
            comments.append(c)
        return comments
    async def save_comment(self, link_id, uid, nick, content):
        await self.comment_collection.insert({
            'link_id': link_id,
            'uid': uid,
            'nick': nick,
            'comment': content,
            'timestamp': self.timestamp,
            'date': int(time.time())
        })
        await self.link_collection.update({'_id': objectid.ObjectId(link_id)},
                                          {'$inc': {'comments': 1}})

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

    async def get_user_by_uid(self, uid):
        return await self.user_collection.find_one({'uid': uid})
    async def get_favs_by_uid(self, uid, n = 20):
        favs = []
        async for f in self.fav_collection.find({'uid': uid}).sort('timestamp', -1).limit(n):
            favs.append(f['link'])
        return favs
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
        return await self.link_collection.find_one({'_id': objectid.ObjectId(link_id)}, {'public': 0})
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
            # await self.user_collection.update({'uid': uid},
            #                                   {'$push': {'favlist': link_id}})
            await self.fav_collection.insert({'uid': uid,
                                 'link_id': link_id,
                                 'timestamp': int(time.time()),
                                 'link': exist})
    async def remove_fav_link_from_uid(self, link_id, uid):
        await self.fav_collection.remove({'uid': uid, 'link_id': link_id})

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
            """
            # remove means never accept again
            if not exist['public']:
                await self.link_collection.remove({"_id": objectid.ObjectId(exist['_id'])})
                return await self.link_collection.insert(data)
            """
            return False

    async def get_topic_metas(self, all=False):
        query = {'public': True}
        if all:
            query = {}
        topic_metas = []
        async for m in self.topic_meta_collection.find(query).sort('rank', -1):
            topic_metas.append(m)
        return topic_metas