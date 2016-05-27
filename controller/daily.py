from .api import BaseController
from .helper import parse
import json

class DailyBot(BaseController):
    def post(self):
        print(self.settings)
        if self.request.headers.get('X-Spider-Key') == self.settings['X-Spider-Key']:

            link = json.loads(self.request.body.decode())
            data = parse(link.get('link'))
            self.write(data)
        else:
            self.write("Bye")
