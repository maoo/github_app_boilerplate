# FINOS GitHub App - Org members sync

## Local run

```
pip3 install -r requirements.txt

export GH_APP_ID=...
export GH_PRIVATE_KEY=...
export GH_PAT="..."

# To run the webhook and intercept events
python3 -m webservice

# To Run Org member sync
python3 webservice/org_member_sync.py
```

On a new terminal
```
ngrok http 8080
```

## Read more
- https://github.com/Mariatta/gh_app_demo
- https://gist.github.com/pelson/47c0c89a3522ed8da5cc305afc2562b0
