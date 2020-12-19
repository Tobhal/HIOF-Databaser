import requests
import json

web_API_key = '847F14587C87812342426B63C04CC39C'
access_token = 'bcc18218801a7992ad7073ba5a1a612a'
pre_fill_steam_ID = '76561198049818407'

appID = None

paramSteam = {
    'allGames': {
        'key': web_API_key,
        'steamid': pre_fill_steam_ID,
        'include_appinfo': 1
    },
    'singleGameDetail': {
        'appids': 1091500
    }
}

def getOwnedGames():
    pass

def getAppDetail(appID):
    pass


r = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/', params=paramSteam['allGames'])
allGames = r.json()

with open('allGames.json', 'w') as outfile:
    json.dump(allGames, outfile, indent=2)



appID = allGames['response']['games'][0]['appid']
r = requests.get('http://store.steampowered.com/api/appdetails', params=paramSteam['singleGameDetail'])
singleGame = r.json()

with open('singleGame.json', 'w') as outfile:
    json.dump(singleGame, outfile, indent=2)


# ---------------------
# API calls to get info 
# ---------------------

# get all owned games:
## https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/
### Params:
#### key: string
#### steamID: uint64
#### include_appinfo: Bool
#### include_played_free_games: Bool
#### appids_filter: uint32
#### include_free_sub: Bool 
#### skip_invetted_apps: Bool 

# get app info:
## http://store.steampowered.com/api/appdetails
### Params:
#### appids: uint32


# -----------
# Web scraper
# -----------
# https://realpython.com/beautiful-soup-web-scraper-python/
#



# -------------
# Wikipedia API
# -------------
# https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&props=claims&titles=CD_Projekt&format=json
# 
# 