import motor.motor_asyncio
import asyncio
import time
from bson import objectid

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client['pyhub']

def score(votes, t):
    return votes/(((int(time.time()) - t)//60 + 2)**1.8)
async def ranky():
    c = db.links
    async for document in c.find({'public': True}):
        favs = document.get('favs') or 1
        comments = document.get('comments') or 0
        new_rank = score(favs + comments, document['date'])
        print(document['_id'], new_rank)
        await c.update({'_id': objectid.ObjectId(document['_id'])}, {'$set': {'rank': new_rank}}, False, True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ranky())