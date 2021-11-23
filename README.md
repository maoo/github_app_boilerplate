# FINOS GitHub App - Org members sync

## Local run

```
pip3 install -r requirements.txt

# export GH_SECRET=11d1392f039276b9c85847198187e74da378ec66
export GH_APP_ID=153610
export GH_PRIVATE_KEY="./finos-gh-org-sync.2021-11-22.private-key.pem"
export GH_PAT="..."

# To run the webhook and intercept events
python3 -m webservice

# To invite a user
python3 webservice/gh-invite.py
```

On a new terminal
```
ngrok http 8080
```

## Read more
- https://github.com/Mariatta/gh_app_demo
- https://gist.github.com/pelson/47c0c89a3522ed8da5cc305afc2562b0
