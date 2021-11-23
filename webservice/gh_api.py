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

def call_gh_api(url, page=1):
    prefix = "https://api.github.com"
    ret = requests.get(
        prefix + url + f"?per_page=100&page={page}", 
        auth=HTTPBasicAuth(gh_user, gh_pat), 
        headers=app_headers()).json()
    if (len(ret) == 100):
        return ret + call_gh_api(url, page=page+1)
    else:
        return ret
    
def get_members_and_invites(org, skip_failed=True):
    resp = call_gh_api(f'/orgs/{org}/members')
    members = [i['login'] for i in resp]

    resp = call_gh_api(f'/orgs/{org}/invitations')
    invitations = [i['login'] for i in resp]

    resp = call_gh_api(f'/orgs/{org}/failed_invitations')
    failed_invitations = [i['login'] for i in resp]

    print('Members: ', len(members))
    print('Pending Invitations: ', len(invitations))
    print('Failed Invitations: ', len(failed_invitations))
    if skip_failed:
        return members + invitations
    else:
        return members + invitations + failed_invitations

def invite_user(user,org):
    resp = requests.put(
      f'https://api.github.com/orgs/{org}/memberships/{user}',
      auth=HTTPBasicAuth(user, os.environ.get("GH_PAT")),
      headers=app_headers())
    print(f'Invited {user} to {org} - response {resp.status_code}')