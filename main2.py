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
def write(name, data, fileType = 'yaml'):
    if not name.endswith('.' + fileType):
        name += '.' + fileType
    
    with open('files/' + fileType + '/' + name, 'w') as outfile:
        if fileType == 'json': json.dump(data, outfile, indent=2)
        if fileType == 'yaml': yaml.dump(data, outfile, indent=2, default_flow_style=False)

def read(name, fileType = 'yaml'):
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
        newCode = int(input('Enter desimal value for', code, 'Final formatt:', final_formatted, ':'))
        
        currencyList[code] = newCode
        write('Currency', currencyList)

    price = initialFormat/(10 ** currencyList[code])

    return {
        'price': price,
        'priceNOK': currency.convert(price, code, 'NOK')
    }

def convertDateTime(date):
    if re.compile('^\d{1,2} \w{3}, \d{4}$').match(date):        # ex: 1 NOV, 2010
        date = datetime.datetime.strptime(date, '%d %b, %Y')
    elif re.compile('^\d{4}$').match(date):                     # ex: 2010
        date = datetime.datetime.strptime(date, '%Y')
    elif re.compile('^[A-Z]\w+ \d{1,2},? \d{4}$').match(date):  # ex: August 24, 1996
        date = datetime.datetime.strptime(date, '%B %d, %Y')
    elif re.compile('^[A-Z]\w{2} \w{4}$').match(date):          # ex: Aug 2005
        date = datetime.datetime.strptime(date, '%b %Y')
    elif re.compile('^[A-Z]\w{3,} \w{4}$').match(date):         # ex: June 2004
        date = datetime.datetime.strptime(date, '%B %Y')
    elif re.compile('^\w{1,2} [A-Z]\w+, \d{4}').match(date):    # ex: 5 April, 1997
        date = datetime.datetime.strptime(date, '%d %B %Y')
    elif re.compile('^\d{4} \\\\u.{4} \d{1,2} \\\\u.{4} \d{1,2} \\\\u.{4}$').match(date):    # ex: 2006 \u5e74 11 \u6708 29 \u65e5
        date = datetime.datetime.strptime(date, '%Y %% %m %% %d')
    elif re.compile('^\d{1,2} \w{3} \d{4}$').match(date):       # ex: 1 NOV 2010
        date = datetime.datetime.strptime(date, '%d %b %Y')
    else:
        print('Not known date:', date)

    return date.date()

# Add elements to list
def getCompany(name):
    global allGamesDetail

    oCompName = name
    
    modifyNames

    if name not in allGamesDetail['company']:
        if name in 


    return None

def getGame(name):
    return None

if __name__ == '__main__':
    allGamesResponse = read('allGames')['response']

    gamesCount = allGamesResponse['game_count']
    allGames = allGamesResponse['games']

    companyNames = read('companyNames')
    currency = read('currency')
    
    try:
        allGamesDetail = read('allGamesDetail')
    except:
        allGamesDetail = {
            'games': {},
            'company': {}
        }

        write('allGamesDetail', allGamesDetail)
    
    # main loop
    i = 0    
    for game in allGames:
        if i == 1000: # To just import some data
            break

        appID = str(game['appid'])

        if appID in allGamesDetail['games']:
            # Game already imported, look for updates
            gameDetail = allGamesDetail['games'][appID]

            # Check if dev info needs update
            if gameDetail['developer'] != None:
                for developer in gameDetail['developer']:
                    gameDetail['developer'][developer] = getCompany(developer)
            
            # Check if pub info needs update
            if gameDetail['publisher'] != None:
                for publisher in gameDetail['publisher']:
                    gameDetail['publisher'][publisher] = getCompany(publisher)

            

            


    