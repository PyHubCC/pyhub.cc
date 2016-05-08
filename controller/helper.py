from __future__ import absolute_import

import json
from bson import ObjectId
from urllib.parse import urlencode
import requests as req

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

