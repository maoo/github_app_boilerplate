import asyncio
import os
import sys
import traceback
import requests

from aiohttp import web
import cachetools
from gidgethub import routing

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)
routes = web.RouteTableDef()

@routes.get("/", name="home")
async def handle_get(request):
    return web.Response(text="FINOS GitHub App - Org members sync")

def build_csv(users, date, repo):
    # TODO
    return None

@routes.post("/webhook")
async def webhook(request):
    try:
        body = await request.json()
        print(body)
        print("---------")
        repo = body['url'].split('/')[5]
        action = body['action']
        if action == 'closed':
            comments = requests.get(body['issue']['comments_url'])
            print(comments.json())
            users = set([comment['user']['login'] for comment in comments])
            date = comments[0]['created_at']
            csv = build_csv(users, date, repo)
            print(csv)
        return web.Response(status=200)
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        return web.Response(status=500)

if __name__ == "__main__":  # pragma: no cover
    app = web.Application()
    app.router.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)