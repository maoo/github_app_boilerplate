import asyncio
import os
import sys
import traceback

from aiohttp import web
import cachetools
from gidgethub import routing

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)
routes = web.RouteTableDef()

@routes.get("/", name="home")
async def handle_get(request):
    return web.Response(text="FINOS GitHub App - Org members sync")

@routes.post("/webhook")
async def webhook(request):
    try:
        body = await request.read()
        print("---------")
        print(body)
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