from __future__ import absolute_import

from . import BaseController
import subprocess
import json
from bson import ObjectId
from urllib.parse import urlencode
import requests as req

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
                    print(msg)
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


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, bool):
            return str(o)
        if isinstance(o, bytes):
            return o.decode()
        return json.JSONEncoder.default(self, o)
class GitHub(object):
    AUTH_API = 'https://github.com/login/oauth/authorize?'
    TOKEN_API = 'https://github.com/login/oauth/access_token?'
    USER_API = 'https://api.github.com/user?'
    def __init__(self, client_id, client_sec, redirect):
        self.client_id = client_id
        self.client_sec = client_sec
        self.scope = "user:email"
        self.query = dict(
            client_id = self.client_id,
            redirect_uri = redirect,
            scope = self.scope
        )
    @property
    def login_url(self):
        return self.AUTH_API + urlencode(self.query)

    def access_token(self, code):
        token_api = self.TOKEN_API + urlencode(dict(
            client_id = self.client_id,
            client_secret = self.client_sec,
            code = code
        ))
        res = req.post(token_api, headers={'Accept': 'application/json'})
        return res.json()
    def get_user(self, atk):
        user_api = self.USER_API + urlencode({'access_token': atk})
        res = req.get(user_api, headers={'Accept': 'application/json'})
        return res.json()

