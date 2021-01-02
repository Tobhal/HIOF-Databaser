import SteamAPI
import WikipediaAPI
#import Database
import json
import pretty_errors

def writeJson(name, data):
    if not name.endswith('.json'):
        name += '.json'
    
    with open("files/" + name, 'w') as outfile:
        json.dump(data, outfile, indent=2)

def readJson(name):
    if not name.endswith('.json'):
        name += '.json'

    with open("files/" + name) as jsonFile:
        data = json.load(jsonFile)

    return data

def updateAllGames():
    global allGamesDetail

    allGames = readJson('All games')['response']['games']
    gameIndex = 0
    gamesMax = int(readJson('All games')['response']['game_count'])

    for game in allGames:
        gameIndex += 1

        appID = game['appid']

        if allGamesDetail.get(str(appID)) == None:  # If the key (appID) dues not exist
            app = SteamAPI.getAppDetail(appID)      # Get the app info form the Steam Store API

            #if app[str(appID)]['success'] == False:     # If the awnser from Steam was false remove the game from the all games list
            #    allGamesOld = readJson('All games')
            #    allGamesOld['response']['game_count'] -= 1
            #    gamesMax -= 1
            #    gameIndex -= 1
            #
            #    del allGamesOld['response']['games'][gameIndex - 1]
            #    writeJson('All games', allGamesOld)
            #    print(f'fail on game {game["name"]}')
            #else:
            allGamesDetail[appID] = app[str(appID)]

            print(f'({gameIndex:3}/{gamesMax}) | {str(app[str(appID)]["success"]):5} | {game["name"]} ')

            writeJson('All games detail', allGamesDetail)
        else:
            print(f'Skip {game["name"]}')

writeJson('All games', SteamAPI.getOwnedGames())

allGamesDetail = readJson('All games detail')
#allGamesDetail = dict()
updateAllGames()

exit()

allGames = readJson('All games')['response']['games']
allGamesDetail = readJson('All games detail')

i = 0
for game in allGames:
    if i >= 1000:
        break

    if allGamesDetail[str(game['appid'])]['success'] == False:
        continue

    gameDetail = allGamesDetail[str(game['appid'])]['data']

    print(f"""{gameDetail['name']} | {gameDetail['steam_appid']}
        Type: {gameDetail['type']} | Dev: {gameDetail['developers']} | Pub: {gameDetail['publishers']}
        Platforms: {[key for key in gameDetail['platforms'] if gameDetail['platforms'][key] == True]}
        Categories: {[key['description'] for key in gameDetail['categories']]}
        Releace Date: {gameDetail['release_date']['date']} """)

    if "metacritic" in gameDetail:
        print(f"""        Metacritic: {gameDetail['metacritic']['score']} """)

    if "price_overview" in gameDetail:
        print(f"""        Price: {gameDetail['price_overview']['initial_formatted']} | Currency: {gameDetail['price_overview']['currency']} """)
    
    if "genres" in gameDetail:
        print(f"""        Genres: {[key['description'] for key in gameDetail['genres']]} """)

    if "recommendations" in gameDetail:
        print(f"""        Recommendations: {gameDetail['recommendations']['total']} """)

    if "dlc" in gameDetail:
        print(f"""        Num DLC: {len(gameDetail['dlc'])} """)

    if "controller_support" in gameDetail:
        print(f"""        Controller support = {gameDetail['controller_support']} """)

    #print(game['name'], "|", game['appid'])

    print()
    i += 1


# MySQL tutorial
# https://www.datacamp.com/community/tutorials/mysql-python