import requests
import json

web_API_key = '847F14587C87812342426B63C04CC39C'
access_token = 'bcc18218801a7992ad7073ba5a1a612a'
pre_fill_steam_ID = '76561198049818407'

def getOwnedGames():
    param = {
        'key': '847F14587C87812342426B63C04CC39C',
        'steamid': '76561198049818407',
        'include_appinfo': 1  
    }

    r = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/', params=param)
    return r.json()

def getAppDetail(appID):
    param = {
        'appids': str(appID)
    }

    r = requests.get('http://store.steampowered.com/api/appdetails', params=param)
    return r.json()



if __name__ == '__main__':
    pass


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