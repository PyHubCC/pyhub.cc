from __future__ import absolute_import

import json
from bson import ObjectId
from urllib.parse import urlencode
import requests as req
import re, html, datetime

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

def parse(url='', title='', abstract=''):
    try:
        header = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1)'
                                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                                 'Chrome/49.0.2623.110 Safari/537.36')}
        res = req.get(url, headers=header, timeout=5)
        rTitle = r'<title>(.*?)<\/title>'
        rAbs   = r'<meta.*?name=".*?description".*?content="([\s\S]*?)"'
        rPy    = r'python|Python|__init__'

        if res.encoding in ['GB2312']:
            text = res.text
        else:
            text = res.text.encode(res.encoding).decode()

        """
        try:
            content = ExtractFromText(text).getContext()
        except:
            content = text
        """

        if not title or len(title) == 0:
            title = re.findall(rTitle, text)
            if len(title) == 0:
                return "None title found!"
            title = html.unescape(title[0])
            title = title.split("|")[0]
        if not abstract:
            abstract = re.findall(rAbs, text)

            if len(abstract) == 0:
                abstract = title
            else:
                abstract = abstract[0]

        abstract = re.sub(r'\s', ' ', abstract)

        return dict(
            title = title,
            link  = url,
            abstract = abstract,
        )
    except:
        return "Catch other error!"