import math
import requests
import requests_cache
import json
from flask import Flask
from markupsafe import escape
import re

app = Flask(__name__)

@app.route('/cotdplayers')
def application():
    link = "https://trackmania.io/api/cotd/0"
    headers = {
        'User-Agent': 'Displays number of players in COTD using a Twitch command. For questions about this project, contact me on Discord: Johnnycyan',
    }
    with requests_cache.enabled('cotd_cache', backend='sqlite', expire_after=20):
        page = requests.get(link, headers=headers).text
    jsonLoading = json.loads(page)
    players = jsonLoading["competitions"][2]["players"]
    cotdDate = jsonLoading["competitions"][2]["name"]
    cotdCheck = cotdDate
    cotdDate = re.search('\d\d\d\d-\d\d-\d\d', cotdDate).group()[5:10]
    #check if cotdDate ends with #1
    if cotdCheck.endswith("#1"):
        pass
    else:
        return f"COTD {escape(cotdDate)} has not been played yet."
    if players == 0:
        return f"COTD {escape(cotdDate)} has not been played yet."
    else:
        divs = int(math.ceil(players / 64))
        return f"COTD {escape(cotdDate)} Players: {escape(players)}, Divs: {escape(divs)}"

if __name__ == "__main__":
    app.run()