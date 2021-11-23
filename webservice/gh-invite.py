from cryptography.hazmat.backends import default_backend
from requests.models import HTTPBasicAuth
import jwt
import requests
import time
import os

gh_pat = os.environ.get("GH_PAT")
gh_user = "maoo"
gh_app_id = os.environ.get("GH_APP_ID")
fname = os.environ.get("GH_PRIVATE_KEY")
cert_str = open(fname, 'r').read()
cert_bytes = cert_str.encode()
private_key = default_backend().load_pem_private_key(cert_bytes, None)

def app_headers():
    time_since_epoch_in_seconds = int(time.time())    
    payload = {
      'iat': time_since_epoch_in_seconds,
      'exp': time_since_epoch_in_seconds + (10 * 60),
      'iss': gh_app_id
    }

    actual_jwt = jwt.encode(payload, private_key, algorithm='RS256')
    headers = {"Authorization": f"Bearer {actual_jwt}",
               "Accept": "application/vnd.github.machine-man-preview+json"}
    return headers

def get_members_and_invites():
    resp = requests.get(f'https://api.github.com/orgs/{org}/members', auth=HTTPBasicAuth(gh_user, gh_pat), headers=app_headers())
    members = [i['login'] for i in resp.json()]

    resp = requests.get(f'https://api.github.com/orgs/{org}/invitations', auth=HTTPBasicAuth(gh_user, gh_pat), headers=app_headers())
    invitations = [i['login'] for i in resp.json()]

    resp = requests.get(f'https://api.github.com/orgs/{org}/failed_invitations', auth=HTTPBasicAuth(gh_user, gh_pat), headers=app_headers())
    failed_invitations = [i['login'] for i in resp.json()]

    print('Members: ', members)
    print('Invitations: ', invitations)
    print('Failed Invitations: ', failed_invitations)
    return members + invitations + failed_invitations

def invite_user(user,org):
    resp = requests.put(
      f'https://api.github.com/orgs/{org}/memberships/{user}',
      auth=HTTPBasicAuth(user, os.environ.get("GH_PAT")),
      headers=app_headers())
    print(f'Invited {user} to {org} - response {resp.status_code}')

user="TheJuanAndOnly99"
org="sessiontechnologies"

if not user in get_members_and_invites():
    invite_user(user,org)
else:
    print(f"skipped {user}")