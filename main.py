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


def createGame(newGameDetail):
    allGames = readJson("All games")["response"]["games"]

    companyNames = readJson('companyNames')
    modifyNames = companyNames['modify']
    skipNames = companyNames['skip']
    failedNames = companyNames['failed']

    i = 0
    for game in allGames:
        if i == 1000:
            break

        appID = int(game["appid"])

        if str(appID) in newGameDetail['games']:
            for developer in newGameDetail['games'][str(appID)]['developer']:
                if developer not in newGameDetail['company']:

                    if developer in modifyNames:
                        devName = developer

                        if devName in modifyNames:
                            devName = modifyNames[devName]
                        elif devName in skipNames:
                            continue
                        elif devName in failedNames:
                            continue

                        print()
                        print()
                        print('Adding developer', devName)

                        devName = devName.replace(" ", "_")

                        try:
                            developerPage = WikipediaAPI.searchForWikiPage(devName)
                            developerData = WikipediaAPI.getWikiData(developerPage)

                            newGameDetail['company'][developer] = developerData
                        except:
                            companyNames['failed'].append(devName)
                            print('Failed to finde: ', devName)

                            writeJson('companyNames', companyNames)
                
            for publicher in newGameDetail['games'][str(appID)]['publisher']:
                if publicher not in newGameDetail['company']:
                    pubName = publicher

                    if pubName in modifyNames:
                        pubName = modifyNames[pubName]
                    elif pubName in skipNames:
                        continue
                    elif pubName in failedNames:
                        continue

                    print('Adding publisher', pubName)

                    pubName.replace(' ', '_')

                    try:
                        publicherPage = WikipediaAPI.searchForWikiPage(devName)
                        publicherData = WikipediaAPI.getWikiData(publicherPage)

                        newGameDetail['company'][publicher] = publicherData
                    except:
                        companyNames['failed'].append(publicher)
                        print('Failed to finde: ', publicher)
                        
                        writeJson('companyNames', companyNames)


            print('Skiping:', newGameDetail['games'][str(appID)]['name'])
        else:
            gameDetail = SteamAPI.getAppDetail(appID)[str(appID)]
            
            if gameDetail['success'] == False:
                continue
            
            gameDetail = gameDetail['data']

            print('Adding game', gameDetail['name'])

            gameDict = {
                'name': gameDetail['name'],
                'gameType': gameDetail['type'],
                'developer': (gameDetail['developers']) if "developers" in gameDetail else None,
                'publisher': gameDetail['publishers'],
                'platforms': [key for key in gameDetail['platforms'] if gameDetail['platforms'][key] == True],
                'releaceDate': gameDetail['release_date']['date'].replace("\u00a0", " "),
                'categories': ([key['description'] for key in gameDetail['categories']]) if "description" in gameDetail else None,
                'genres': ([key['description'] for key in gameDetail['genres']]) if "genres" in gameDetail else None,
                'metacritic': gameDetail['metacritic']['score'] if "metacritic" in gameDetail else None,
                'price': {
                    'final_formatted': gameDetail['price_overview']['final_formatted'] if "price_overview" in gameDetail else None,
                    'currency': gameDetail['price_overview']['currency'] if "price_overview" in gameDetail else None
                },
                'recommendations': gameDetail['recommendations'] if "recommendations" in gameDetail else None,
                'numDLC': len(gameDetail['dlc']) if "dlc" in gameDetail else None,
                'controllerSupport': gameDetail['controller_support'] if "controller_support" in gameDetail else 'none'

            }
            
            newGameDetail['games'][int(appID)] = gameDict

            if gameDict['developer'] != None:

                for developer in gameDict['developer']:
                    if developer not in newGameDetail['company']:
                        devName = developer

                        if devName in modifyNames:
                            devName = modifyNames[devName]
                        elif devName in skipNames:
                            continue
                        elif devName in failedNames:
                            continue

                        print('Adding developer', devName)

                        devName = devName.replace(" ", "_")

                        try:
                            developerPage = WikipediaAPI.searchForWikiPage(devName)
                            developerData = WikipediaAPI.getWikiData(developerPage)

                            newGameDetail['company'][developer] = developerData
                        except:
                            companyNames['failed'].append(developer)
                            print('Failed to finde: ', developer)

                            writeJson('companyNames', companyNames)

            for publicher in gameDict['publisher']:
                if publicher not in newGameDetail['company']:
                    pubName = publicher

                    if pubName in modifyNames:
                        pubName = modifyNames[pubName]
                    elif pubName in skipNames:
                        continue
                    elif pubName in failedNames:
                        continue

                    print('Adding publisher', pubName)

                    pubName.replace(' ', '_')

                    try:
                        publicherPage = WikipediaAPI.searchForWikiPage(devName)
                        publicherData = WikipediaAPI.getWikiData(publicherPage)

                        newGameDetail['company'][publicher] = publicherData
                    except:
                        companyNames['failed'].append(publicher)
                        print('Failed to finde: ', publicher)
                        
                        writeJson('companyNames', companyNames)


        writeJson('allGamesDetail', newGameDetail)

        i += 1

    return newGameDetail    


#newGameDetail = dict()
#newGameDetail['games'] = dict()
#newGameDetail['company'] = dict()

newGameDetail = readJson('allGamesDetail')
writeJson('AllGamesDetail', createGame(newGameDetail))



exit()
writeJson('All games', SteamAPI.getOwnedGames())

allGamesDetail = readJson('All games detail')
#allGamesDetail = dict()
#updateAllGames()

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