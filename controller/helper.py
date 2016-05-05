from __future__ import absolute_import

from . import BaseController
import subprocess
import json
from bson import ObjectId

# '/web_hook/github_push'
# '/web_hook/coding_git' => Webhooks
class WebHookHandler(BaseController):
    def post(self, *args, **kwargs):
        if self.request.headers.get('X-Coding-Event') == 'push':
            print("Execute git pull")
            subprocess.call("git pull", shell=True)
        if self.request.headers.get('X-GitHub-Event') == 'push':
            print("Execute git pull github master")
            subprocess.call("git pull github master", shell=True)
        else:
            print(self.request.headers.get('X-Coding-Event'))
            self.write("Bye")
    def get(self, *args, **kwargs):
        self.write("What're u looking 4?")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, bool):
            return str(o)
        return json.JSONEncoder.default(self, o)
