import tornado.web
from urllib.parse import urlparse
from datetime import datetime
class BaseController(tornado.web.RequestHandler):

    def make_link(self, data):
        """
        data format: {
            title:
            abstract:
            date:
            link:
            via:
            public:
        }
        """
        link = dict(
            host = urlparse(data['link']).netloc,
            thumb = '',
            author = '',
            rank   = 1,
            public = True,
        )
        link.update(data)
        return link
    def make_user(self, user):
        """
        user format: {
            uid:
            nick:
            avatar:
            email:
            admin: 0
            points: 0
        }
        """
        return dict(
            uid = user.get('login'),
            nick = user.get('name'),
            avatar = user.get('avatar_url'),
            email = user.get('email'),
            admin= 0,
            points=0,
            date = datetime.today().strftime("%Y-%m-%d")
        )
