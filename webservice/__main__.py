import asyncio
import os
import sys
import traceback

from aiohttp import web
import cachetools
from gidgethub import routing
from cryptography.hazmat.backends import default_backend
import jwt
import requests
import time

router = routing.Router()
cache = cachetools.LRUCache(maxsize=500)

routes = web.RouteTableDef()

fname = os.environ.get("GH_PRIVATE_KEY")
cert_str = open(fname, 'r').read()
cert_bytes = cert_str.encode()
private_key = default_backend().load_pem_private_key(cert_bytes, None)
gh_app_id = os.environ.get("GH_APP_ID")

def app_headers():
    time_since_epoch_in_seconds = int(time.time())
    
    payload = {
      # issued at time
      'iat': time_since_epoch_in_seconds,
      # JWT expiration time (10 minute maximum)
      'exp': time_since_epoch_in_seconds + (10 * 60),
      # GitHub App's identifier
      'iss': gh_app_id
    }

    actual_jwt = jwt.encode(payload, private_key, algorithm='RS256')
    headers = {"Authorization": f"Bearer {actual_jwt}",
               "Accept": "application/vnd.github.machine-man-preview+json"}
    return headers

@routes.get("/", name="home")
async def handle_get(request):
    return web.Response(text="FINOS GitHub App - Org members sync")

@routes.post("/webhook")
async def webhook(request):
    try:
        body = await request.read()
        print("---------")
        print(body)

        resp = requests.get('https://api.github.com/app', headers=app_headers())

        print('Code: ', resp.status_code)
        print('Content: ', resp.content.decode())

        return web.Response(status=resp.status_code)
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

# @router.register("installation", action="created")
# async def repo_installation_added(event, gh, *args, **kwargs):
#     installation_id = event.data["installation"]["id"]

#     installation_access_token = await apps.get_installation_access_token(
#         gh,
#         installation_id=installation_id,
#         app_id=os.environ.get("GH_APP_ID"),
#         private_key=os.environ.get("GH_PRIVATE_KEY"))
#     repo_name = event.data["repositories"][0]["full_name"]
#     url = f"/repos/{repo_name}/issues"
#     response = await gh.post(
#         url,
#         data={
#             'title': 'Thanks for installing the FINOS GitHub App - Org members sync',
#             'body': 'Thanks!',
#         },
#         oauth_token=installation_access_token["token"])
#     print(response)