import tornado.web
from urllib.parse import urlparse
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
