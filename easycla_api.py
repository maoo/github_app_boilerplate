import requests

resp = requests.get('https://easycla.linuxfoundation.org/api/v2/...')

json = resp.json()

res = json['result'][0]

print(res)