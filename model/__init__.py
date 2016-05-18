from __future__ import absolute_import

from bson import objectid
from datetime import datetime
import time
import pytz
import motor.motor_tornado

from .Account import AccountMeta

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

        self.account_collection = self.db[Env.COL_ACCOUNT]

    @property
    def date(self):
        """
        MM/DD
        """
        return datetime.today().strftime("%m/%d")
    @property
    def timestamp(self):
        """
        MM-DD:HH:MM:SS
        """
        return datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%m-%d:%H:%M:%S")
    @property
    def full_timestamp(self):
        """
        YY-MM-DD:HH:MM:SS
        """
        return datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime("%y-%m-%d:%H:%M:%S")
    @property
    def time_int(self):
        """
        time int
        """
        return int(time.time())

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

        # ACCOUNT ACTION
        await self.update_account(uid, "评论")

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

        # ACCOUNT ACTION
        await self.update_account(uid, "留言")
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

        # ACCOUNT ACTION
        via = await self.link_collection.find_one({'_id': objectid.ObjectId(link_id)})
        await self.update_account(via.get('via_uid'), '分享链接被移除')


    async def fav_link(self, link_id, uid):
        exist = await self.get_link_by_id(link_id)
        if bool(exist):
            # update fav list
            await self.link_collection.update({'_id': objectid.ObjectId(link_id)},
                                              {'$inc': {'favs': 1},
                                               '$push': {'favlist': uid}})
            await self.fav_collection.insert({'uid': uid,
                                 'link_id': link_id,
                                 'timestamp': int(time.time()),
                                 'link': exist})
            # ACCOUNT ACTION
            await self.update_account(uid, '收藏链接')
            via = await self.link_collection.find_one({'_id': objectid.ObjectId(link_id)})
            await self.update_account(via.get('via_uid'), '分享被收藏')

    async def remove_fav_link_from_uid(self, link_id, uid):
        await self.fav_collection.remove({'uid': uid, 'link_id': link_id})
        # ACCOUNT ACTION
        await self.update_account(uid, '取消收藏')

    async def get_user(self, uid):
        return await self.user_collection.find_one({'uid': uid})
    async def save_user(self, user):
        exist = await self.get_user(user['uid'])
        if not bool(exist):
            self.user_collection.insert(user)

            # ACCOUNT ACTION
            await self.update_account(user['uid'], '新用户')

    async def get_links(self, page_no=1, page_size=30):
        query = dict(
            public = True,
        )
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
        if len(data['title']) == 0:
            return False
        exist = await self.find_link_by_title_or_link(data['title'], data['link'])
        if not bool(exist):
            res = await self.link_collection.insert(data)
            # ACCOUNT ACTION
            await self.update_account(data.get('via_uid'), '分享链接')
            return res
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
    def get_account_metas(self):
        return AccountMeta.META_LIST

    async def update_account(self, uid, action):
        points = AccountMeta.META.get(action)
        if not points or not uid:
            print("Wrong Action!")
            return

        update = {'$inc': {'points': points}}
        await self.user_collection.update({'uid': uid}, update)
        balance = await self.user_collection.find_one({'uid': uid})
        await self.account_collection.insert(dict(
            uid = uid,
            action = action,
            points = points,
            timestamp = self.full_timestamp,
            balance = balance['points']
        ))
    async def get_points_of_uid(self, uid, n = 50):
        points = []
        async for p in self.account_collection.find({'uid': uid}, {'_id': 0}).sort('timestamp', -1).limit(n):
            points.append(p)
        return points