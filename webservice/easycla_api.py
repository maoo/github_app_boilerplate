import requests

easycla_prod_prefix = "https://pcc-bff.platform.linuxfoundation.org/production/api/cla-services/"
cla_group_id = '5564f18f-3252-40fc-a65b-2eef1ad45fcd'

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rTXdPVGt4TkVaR1JqSkJPRFJFT1Rrek16ZzJRMFE0TlRFMlJFSTNRVUk0TUVGRU5FRTVNZyJ9.eyJodHRwOi8vbGZ4LmRldi9jbGFpbXMvZW1haWwiOiJtYXVyaXppb0BzZXNzaW9uLml0IiwiaHR0cDovL2xmeC5kZXYvY2xhaW1zL3VzZXJuYW1lIjoibWFvbyIsImlzcyI6Imh0dHBzOi8vc3NvLmxpbnV4Zm91bmRhdGlvbi5vcmcvIiwic3ViIjoiYXV0aDB8bWFvbyIsImF1ZCI6WyJodHRwczovL2FwaS1ndy5wbGF0Zm9ybS5saW51eGZvdW5kYXRpb24ub3JnLyIsImh0dHBzOi8vbGludXhmb3VuZGF0aW9uLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2Mzc3MDI3MzEsImV4cCI6MTYzNzcyNDMzMSwiYXpwIjoiNk44N0JMSGhKUGJEdDNkOTM2Z1RGazQ1UFF1TzFlRG8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIGFjY2VzczphcGkgb2ZmbGluZV9hY2Nlc3MifQ.r-uhXKYQa3vIBNMYCJ-Zkz-OM78Ei258jR--gP1sS5-4J1Nraf7d8epdTSfB1eJyBdTGUHv5pHO6k8f6kQz_Nsn2N5ytLT1wPFqf1NKwbX3sSKZtsZqjCnwLgWIHA9qPthSAKVGvbTfqust4ytaaLjKePazDhvUCGdnNTbBJlsTqsfFQoZRlw0skFOVX4_A16tkNvdVkgDfWGRFhI5D5WNhMXKMDmYpWTblryv7aNbtyRoTln8T6tZHWdBcfvCQ8DYVyolhUSS_nryVbvW2fZmaVqJme4EpofAWaLq89fCVND3jJvTrINhHVd0yXT8kH0YoyXGDZtQoMfGA_xG_iSA"

def app_headers():
    headers = {"Authorization": f"Bearer {token}"}
    return headers

def get_entries(url):
    resp = requests.get(easycla_prod_prefix + url + "pageSize=100", headers=app_headers()).json()
    # print("========")
    # print(resp)
    # print("========")
    ret = []
    if 'list' in resp:
        ret = resp['list']
    elif 'signatures' in resp:
        ret = resp['signatures']
    if 'nextKey' in resp:
        return ret + get_entries(url + f"nextKey={resp['nextKey']}")
    return ret

def get_easycla_gh_usernames():
    icla_signatures_url = f"/cla-group/{cla_group_id}/icla/signatures?"
    icla_signatures_raw = get_entries(icla_signatures_url)
    iclas = [i['github_username'] for i in icla_signatures_raw]
    easycla_gh_users = iclas

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
