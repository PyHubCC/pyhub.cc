from __future__ import absolute_import
import re

from . import BaseController
import json

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