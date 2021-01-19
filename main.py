import SteamAPI
import WikipediaAPI
#import Database
import json
import pretty_errors
import datetime
import re
from currency_converter import CurrencyConverter

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

def convertCurrency(initialFormat, code, final_formatted):
    currencyList = readJson('Currency')
    currency = CurrencyConverter()

    if code not in currencyList:
        print()
        print()
        print('Enter desimal value for', code, 'Final formatt:', final_formatted)
        newCode = int(input())
        
        currencyList[code] = newCode
        writeJson('Currency', currencyList)

    price = initialFormat/(10 ** currencyList[code])

    return {
        'price': price,
        'priceNOK': currency.convert(price, code, 'NOK')
    }

def convertDateTime(date):
    patternDate1 = re.compile('^\d{1,2} \w{3},? \d{4}$') # ex: 1 NOV, 2010
    patternDate2 = re.compile('^\d{4}$') # ex: 2010
    patternDate3 = re.compile('^[A-Z]\w+ \d{1,2},? \d{4}$') # ex: August 24, 1996
    patternDate4 = re.compike('^[A-Z]\w+ \w{4}$') #ex: June 2004

    if patternDate1.match(date):
        date = datetime.datetime.strptime(date, '%d %b, %Y')
    elif patternDate2.match(date):
        date = datetime.datetime.strptime(date, '%Y')
    elif patternDate3.match(date):
        date = datetime.datetime.strptime(date, '%B %d, %Y')
    elif patternDate4.match(date):
        date = dateTime.datetime.strptime(date, '%B %Y')

    return date

def createGame(newGameDetail):
    allGames = readJson("All games")["response"]["games"]

    companyNames = readJson('companyNames')
    modifyNames = companyNames['modify']
    skipNames = companyNames['skip']
    failedNames = companyNames['failed']

    i = 0
    for game in allGames:
        if i == 50:
            break

        appID = int(game["appid"])

        if str(appID) in newGameDetail['games']:
            if newGameDetail['games'][str(appID)]['developer'] == None:
                continue

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


            print(f"{i:3} | Skiping: {newGameDetail['games'][str(appID)]['name']}")
        else:
            gameDetail = SteamAPI.getAppDetail(appID)[str(appID)]
            
            if gameDetail['success'] == False:
                continue
            
            gameDetail = gameDetail['data']

            print(f"{i:3} | Adding: {gameDetail['name']}")

            if 'price_overview' in gameDetail:
                price = convertCurrency(gameDetail['price_overview']['initial'], gameDetail['price_overview']['currency'], gameDetail['price_overview']['final_formatted'])

            date = gameDetail['release_date']['date'].replace("\u00a0", " ")

            gameDict = {
                'name': gameDetail['name'],
                'gameType': gameDetail['type'],
                'developer': (gameDetail['developers']) if "developers" in gameDetail else None,
                'publisher': gameDetail['publishers'],
                'platforms': [key for key in gameDetail['platforms'] if gameDetail['platforms'][key] == True],
                'releaceDate': str(convertDateTime(date)),
                'categories': ([key['description'] for key in gameDetail['categories']]) if "description" in gameDetail else None,
                'genres': ([key['description'] for key in gameDetail['genres']]) if "genres" in gameDetail else None,
                'metacritic': gameDetail['metacritic']['score'] if "metacritic" in gameDetail else None,
                'price': {
                    'initial': gameDetail['price_overview']['initial'] if "price_overview" in gameDetail else None,
                    'final_formatted': price['price'] if "price_overview" in gameDetail else None,
                    "price_NOK": price['priceNOK'] if "price_overview" in gameDetail else None,
                    'currency': gameDetail['price_overview']['currency'] if "price_overview" in gameDetail else None
                },
                'recommendations': gameDetail['recommendations'] if "recommendations" in gameDetail else None,
                'numDLC': len(gameDetail['dlc']) if "dlc" in gameDetail else None,
                'controllerSupport': gameDetail['controller_support'] if "controller_support" in gameDetail else 'none'

            }
            # gameDetail['release_date']['date'].replace("\u00a0", " ")
            newGameDetail['games'][appID] = gameDict

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
                            print('WikiAPI: Failed to finde', developer)

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

#companyNames = dict()

newGameDetail = readJson('allGamesDetail')
writeJson('AllGamesDetail', createGame(newGameDetail))

# developerData['founded'] = convertDateTime(developerData['founded'])

# MySQL tutorial
# https://www.datacamp.com/community/tutorials/mysql-python