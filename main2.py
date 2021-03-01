import SteamAPI
import WikipediaAPI
#import Database
import json
import yaml
import datetime
import re
from currency_converter import CurrencyConverter

allGamesDetail = None
companyNames = None
currency = None

# Handle files
def write(name, data, fileType = 'json'):
    if not name.endswith('.' + fileType):
        name += '.' + fileType
    
    with open('files/' + fileType + '/' + name, 'w') as outfile:
        if fileType == 'json': json.dump(data, outfile, indent=2)
        if fileType == 'yaml': yaml.dump(data, outfile, indent=2, default_flow_style=False)

def read(name, fileType = 'json'):
    if not name.endswith('.' + fileType):
        name += '.' + fileType

    with open('files/' + fileType + '/' + name) as infile:
        if fileType == 'json': return json.load(infile)
        if fileType == 'yaml': return yaml.load(infile, Loader=yaml.FullLoader)

# Handle convertions
def convertCurrency(initialFormat, code, final_formatted):
    currencyList = read('currency')
    currency = CurrencyConverter()

    if code not in currencyList:
        print('Enter desimal value for', code, 'Final formatt:', final_formatted, ':')
        newCode = int(input())
        
        currencyList[code] = newCode
        write('Currency', currencyList)

    price = initialFormat/(10 ** currencyList[code])

    return {
        'price': price,
        'priceNOK': round(currency.convert(price, code, 'NOK'), 2)
    }

def convertDateTime(date):
    if re.compile('^\d{1,2} \w{3}, \d{4}$').match(date):            # ex: 1 NOV, 2010
        date = datetime.datetime.strptime(date, '%d %b, %Y')
    elif re.compile('^\d{4}/\d{4}$').match(date):                   # ex: 1998/1999
        date = datetime.datetime.strptime(date, '%Y/')
    elif re.compile('^\d{4} .+').match(date):                                # ex: 1991 in
        date = datetime.datetime.strftime(date, '%Y ')
    elif re.compile('^\d{1,2} \w+ \d{4}$').match(date):             # ex: 28 March 1986
        date = datetime.datetime.strptime(date, '%d %B %Y')
    elif re.compile('^\d{4}$').match(date):                         # ex: 2010
        date = datetime.datetime.strptime(date, '%Y')
    elif re.compile('^[A-Z]\w{2} \d{1,2},? \d{4}$').match(date):    # ex: Nov 16, 2016
        date = datetime.datetime.strptime(date, '%b %d, %Y')
    elif re.compile('^[A-Z]\w{3,} \d{1,2},? \d{4}$').match(date):   # ex: August 24, 1996
        date = datetime.datetime.strptime(date, '%B %d, %Y')
    elif re.compile('^[A-Z]\w{2} \w{4}$').match(date):              # ex: Aug 2005
        date = datetime.datetime.strptime(date, '%b %Y')
    elif re.compile('^[A-Z]\w{3,} \w{4}$').match(date):             # ex: June 2004
        date = datetime.datetime.strptime(date, '%B %Y')
    elif re.compile('^\w{1,2} [A-Z]\w+, \d{4}').match(date):        # ex: 5 April, 1997
        date = datetime.datetime.strptime(date, '%d %B %Y')
    elif re.compile('^\d{4} \\\\u.{4} \d{1,2} \\\\u.{4} \d{1,2} \\\\u.{4}$').match(date):    # ex: 2006 \u5e74 11 \u6708 29 \u65e5
        date = datetime.datetime.strptime(date, '%Y %% %m %% %d')
    elif re.compile('^\d{1,2} \w{3} \d{4}$').match(date):           # ex: 1 NOV 2010
        date = datetime.datetime.strptime(date, '%d %b %Y')
    elif re.compile('^\d{1,2}\. \w+ \d{4}$').match(date):           # ex: 20. Juni 2013
        date = datetime.datetime.strptime(date, '%d %B %Y')
    elif re.compile('^\d{1,2} \w+ \d{4}$').match(date):             # ex: 20 February 2012
        date = datetime.datetime.strptime(date, '%d, %b, %Y')
    else:
        print('Not known date:', date)

    return date.date()

# Add elements to list
def addCompany(name):
    global allGamesDetail

    oCompName = name
    
    modifyNames = companyNames['modify']

    if name not in allGamesDetail['company']:
        if name in modifyNames:
            name = modifyNames[name]
        elif name in companyNames['skip']:
            return
        elif name in companyNames['failed']:
            return

    if name not in allGamesDetail['company']:
        try:
            companyPage = WikipediaAPI.searchForWikiPage(name)
            companyData = WikipediaAPI.getWikiData2(companyPage)
        except:
            print('Failed to finde', oCompName)
            companyNames['failed'].append(oCompName)
            write('companyNames', companyNames, fileType='json')
        else:
            allGamesDetail['company'][name] = companyData

def prosessGames(l = 1000):
    global allGamesDetail, companyNames, currency

    allGamesResponse = read('allGames')['response']

    gamesCount = allGamesResponse['game_count']
    allGames = allGamesResponse['games']
    allGamesLen = allGamesResponse['game_count']

    companyNames = read('companyNames')
    currency = read('currency')
    
    try:
        allGamesDetail = read('allGamesDetail')
    except:
        allGamesDetail = dict()
        allGamesDetail['games'] = dict()
        allGamesDetail['company'] = dict()

        write('allGamesDetail', allGamesDetail)

    # main loop
    i = 0    
    for game in allGames:
        if i >= l: # To just import some data
            break

        appID = str(game['appid'])

        if appID in allGamesDetail['games']:
            # Game already imported, look for updates
            gameDetail = allGamesDetail['games'][appID]

            # Check if dev info needs update
            if gameDetail['developer'] != None:
                for developer in gameDetail['developer']:
                    addCompany(developer)
            
            # Check if pub info needs update
            if gameDetail['publisher'] != None:
                for publisher in gameDetail['publisher']:
                    addCompany(publisher)
            
            print(f"{i + 1:3}/{allGamesLen}| Skiping: {allGamesDetail['games'][appID]['name']}")
        else:
            singleGameDetail = SteamAPI.getAppDetail(appID)[appID]

            if singleGameDetail['success'] == False:
                print(f"{i + 1:3}/{allGamesLen}| Failed to import {appID}")
                continue
            
            singleGameDetail = singleGameDetail['data']
            print(f"{i + 1:3}/{allGamesLen}| Adding: {singleGameDetail['name']}")

            if 'price_overview' in singleGameDetail:
                price = convertCurrency(singleGameDetail['price_overview']['initial'], singleGameDetail['price_overview']['currency'], singleGameDetail['price_overview']['final_formatted'])

            date = singleGameDetail['release_date']['date'].replace("\u00a0", " ")

            gameDict = {
                'name': singleGameDetail['name'],
                'gameType': singleGameDetail['type'],
                'developer': (singleGameDetail['developers']) if "developers" in singleGameDetail else None,
                'publisher': singleGameDetail['publishers'],
                'platforms': [key for key in singleGameDetail['platforms'] if singleGameDetail['platforms'][key] == True],
                'releaceDate': str(convertDateTime(date)) if date != '' else None,
                'categories': ([key['description'] for key in singleGameDetail['categories']]) if "description" in singleGameDetail else None,
                'genres': ([key['description'] for key in singleGameDetail['genres']]) if "genres" in singleGameDetail else None,
                'metacritic': singleGameDetail['metacritic']['score'] if "metacritic" in singleGameDetail else None,
                'price': {
                    'initial': singleGameDetail['price_overview']['initial'] if "price_overview" in singleGameDetail else None,
                    'final_formatted': price['price'] if "price_overview" in singleGameDetail else None,
                    "price_NOK": price['priceNOK'] if "price_overview" in singleGameDetail else None,
                    'currency': singleGameDetail['price_overview']['currency'] if "price_overview" in singleGameDetail else None
                },
                'recommendations': singleGameDetail['recommendations'] if "recommendations" in singleGameDetail else None,
                'numDLC': len(singleGameDetail['dlc']) if "dlc" in singleGameDetail else 0,
                'controllerSupport': singleGameDetail['controller_support'] if "controller_support" in singleGameDetail else 'none'
            }

            allGamesDetail['games'][int(appID)] = gameDict

            if gameDict['developer'] != None:
                for dev in gameDict['developer']:
                    addCompany(dev)
            
            if gameDict['publisher'] != None:
                for pub in gameDict['publisher']:
                    addCompany(pub)

        write('allGamesDetail', allGamesDetail)
        i += 1

if __name__ == '__main__':
    prosessGames(l=0)
    