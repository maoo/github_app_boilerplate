import requests
import os

easycla_prod_prefix = os.environ.get("EASY_CLA_API_PREFIX")
cla_group_id = os.environ.get("EASY_CLA_GROUP_ID") 
token = os.environ.get("EASY_CLA_TOKEN")

def app_headers():
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def get_entries(url):
    resp = requests.get(easycla_prod_prefix + url + "pageSize=100", headers=app_headers())
    if resp.status_code != 200:
        print("Error fetching EasyCLA entries...")
        print(resp.text)
        return []
    resp = resp.json()
    ret = []
    if 'list' in resp:
        ret = resp['list']
    elif 'signatures' in resp:
        ret = resp['signatures']
    # TODO - test
    if 'lastKeyScanned' in resp and len(ret) == 100:
        return ret + get_entries(url + f"nextKey={resp['lastKeyScanned']}&")
    return ret

def get_easycla_gh_usernames():
    icla_signatures_url = f"/cla-group/{cla_group_id}/icla/signatures?"
    icla_signatures_raw = get_entries(icla_signatures_url)
    iclas = [i['github_username'] for i in icla_signatures_raw]
    easycla_gh_users = iclas
    print(f"Found {len(iclas)} ICLAs!")

    cclas_url = f"/signatures/project/{cla_group_id}?signatureType=ccla&signed=true&approved=true&"
    cclas_raw = get_entries(cclas_url)
    cclas = [i['signatureReferenceID'] for i in cclas_raw]
    print(f"Found {len(cclas)} CCLAs!")
    for ccla in cclas:
        company_contributors_url = f"/cla-group/{cla_group_id}/contributors?companyID={ccla}&"
        company_contributors_raw = get_entries(company_contributors_url)
        if company_contributors_raw and len(company_contributors_raw) > 0:
            company_contributors = [i['github_id'] for i in company_contributors_raw]
            easycla_gh_users = easycla_gh_users + company_contributors
            
    ret = set(easycla_gh_users)
    if '' in ret: ret.remove('')
    return ret
