from __future__ import absolute_import
import re

from . import BaseController
import json
import subprocess

# '/web_hook/github_push'
# '/web_hook/coding_git' => Webhooks
class WebHookHandler(BaseController):
    async def post(self, *args, **kwargs):
        if self.request.headers.get('X-Coding-Event') == 'push':
            print("Execute git pull")
            subprocess.call("git pull", shell=True)
        if self.request.headers.get('X-GitHub-Event') == 'push':
            payload = json.loads(self.request.body.decode())
            if payload.get('head_commit'):
                if payload.get('head_commit').get('message').startswith('Event:'):
                    msg = payload.get('head_commit').get('message').split('Event:')[-1]
                    await self.application.db.save_event(msg)

            print("Execute git pull github master")
            subprocess.call("git pull github master", shell=True)
        else:
            print(self.request.headers.get('X-Coding-Event'))
            self.write("Bye")
    async def put(self, *args, **kwargs):
            payload = json.loads(self.request.body.decode())
            print(payload)
            if payload.get('head_commit'):
                if payload.get('head_commit').get('message').startswith('Event:'):
                    msg = payload.get('head_commit').get('message').split('Event:')[-1]
                    await self.application.db.save_event(msg)
    def get(self, *args, **kwargs):
        self.write("What're u looking 4?")

# '/api/v1/post_data' => Post data in
class APIPost(BaseController):
    async def post(self, *args, **kwargs):
        """
        data format: {
            title:
            abstract:
            date:
            link:
            via:
        }
        """
        if self.request.headers.get('X-Spider-Key') == self.settings['X-Spider-Key']:
            body = self.request.body.decode()

            data = json.loads(body)
            data = self.make_link(data)
            res = await self.application.db.save_link(data)
            if bool(res):
                self.write(dict(status=0))
            else:
                self.write(dict(status=-1))
        else:
            self.write("Bye~")
# '/api/v1/msg'
class MsgPost(BaseController):
    async def get(self, *args, **kwargs):
        msgs = await self.application.db.get_new_msgs(20)
        self.write(self.json_encode({'msgs': msgs}))

    async def post(self, *args, **kwargs):
        uid = self.get_secure_cookie('uid')
        if isinstance(uid, bytes):
            uid = uid.decode()
        if not uid:
            self.write({'status': 403})

        msg = re.sub(r'\s', ' ', self.get_body_argument('msg'))
        result = await self.application.db.save_msg(content=msg, user=self.get_secure_cookie('nick').decode(), uid = uid)
        self.write(self.json_encode(dict(status=200, msg=result)))

# '/api/v1/comment'
class CommentAPI(BaseController):
    async def get(self, link_id):
        if not link_id:
            self.write({"status": 404})
        comments = await self.application.db.get_comments_by_link_id(link_id)
        self.write(self.json_encode(comments))
    async def post(self, *args, **kwargs):
        uid = self.get_secure_cookie('uid')
        if isinstance(uid, bytes):
            uid = uid.decode()
        if not uid:
            self.write({'status': 403})
        nick = self.get_secure_cookie('nick').decode()

        link_id = self.get_body_argument('link_id')
        comment = self.get_body_argument('comment')
        await self.application.db.save_comment(link_id, uid, nick, comment)
        self.write({'link_id': link_id, 'comment': comment})

# '/fav/link_id' => Fav action
# '/act/link_id' => Action
class FavHandler(BaseController):

    async def post(self, link_id):
        uid = self.get_secure_cookie('uid')
        if isinstance(uid, bytes):
            uid = uid.decode()
        if not uid:
            self.write({'status': 403})

        action = self.get_body_argument('action')
        if action == 'FAV':
            await self.application.db.fav_link(link_id, uid)
        elif action == 'PRO':
            await self.application.db.pro_link(link_id, uid)
        elif action == 'DEL':
            if not self.is_admin():
                self.write({'status': 403})
            await self.application.db.del_link(link_id)
        self.write(self.json_encode({'status': 200}))

# '/api/v1/points' => Points api
class APIPoints(BaseController):
    async def post(self, *args, **kwargs):
        uid = self.get_secure_cookie('uid')
        if not uid:
            self.write({'status': 403})
        points = await self.application.db.get_points_of_uid(uid.decode())
        self.write(dict(points=points))
