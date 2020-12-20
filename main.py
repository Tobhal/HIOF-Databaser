import SteamAPI
import WikipediaAPI
import Database
import mysql.connector
import json

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

allGames = readJson('All Games')
appDetail = readJson('Single game')

wikiPage = WikipediaAPI.searchForWikiPage('fromsoftware')
wikiData = WikipediaAPI.getWikiData(wikiPage)
print(wikiData)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=input("Type password: ")
)

cursor = db.cursor()



# MySQL tutorial
# https://www.datacamp.com/community/tutorials/mysql-python