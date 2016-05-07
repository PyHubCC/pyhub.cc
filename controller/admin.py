from __future__ import absolute_import
import re

from . import BaseController
import json

class AdminController(BaseController):
    def get(self, *args, **kwargs):
        nick = self.get_secure_cookie('nick')
        uid  = self.get_secure_cookie('uid')
        github_url = self.application.github.login_url
        render_data = dict(
            title = 'PyHub Admin',
            uid   = uid,
            nick = nick,
            login_url= github_url
        )
        self.render("admin.html", **render_data)