from __future__ import absolute_import

from . import BaseController
import json

class AdminController(BaseController):
    async def get(self, *args, **kwargs):

        if not self.is_admin():
            self.redirect('/403')
        users = await self.application.db.get_new_users(n=50)
        topic_metas = await self.application.db.get_topic_metas(all=True)
        account_metas = self.application.db.get_account_metas()
        render_data = dict(
            title = 'PyHub Admin',
            topic_metas = self.json_encode(topic_metas),
            users = self.json_encode(users),
            account_metas = self.json_encode(account_metas)
        )
        self.render("admin.html", **{**self.default_data, **render_data})

    async def post(self, *args, **kwargs):
        if not self.is_admin():
            self.write({"status": 403})

        act = self.get_body_argument('act')
        if not act:
            self.write({"status": 404})
        if act == 'create_topic':
            topic = json.loads(self.get_body_argument('data'))
            self.application.db.topic_meta_collection.insert(topic)
            self.write({"status": 200})