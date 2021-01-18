import requests
from bs4 import BeautifulSoup
import pretty_errors

#page = requests.get('https://en.wikipedia.org/wiki/CD_Projekt')
#page = requests.get('https://en.wikipedia.org/wiki/FromSoftware')
#page = requests.get('https://en.wikipedia.org/wiki/Ubisoft')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Ubisoft')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Valve_Corporation')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Cryteck_Studios')
page = requests.get('https://en.wikipedia.org/w/index.php?search=Crytek')


def searchForWikiPage(searchText):
    print('WikiAPI search:', searchText)
    return requests.get('https://en.wikipedia.org/w/index.php?search=' + searchText)

def getWikiData(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mw-content-text')
    job_elems = results.find('table', class_='infobox vcard')
    texts = job_elems.findAll(text=True)

    dataOut = {
        'type': None,
        'industry': None,
        'founded': None,
        'founder': None,
        'founders': None,
        'headquarters': None,
        'area served': None,
        'number of employees': None,
        'parent': None,
        'native name': None,
        'romanized': None,
        'website': None
    }

    for i in range(len(texts)):
        text = texts[i].lower()

        if text == 'headquarters':
            dataOut[text] = texts[i + 1], texts[i + 3]

        elif text == 'website':
            if texts[i + 1] == 'www':
                dataOut[text] = texts[i + 1] + texts[i + 2] + texts[i + 3]
                continue
            else:
                dataOut[text] = texts[i + 1]

        if text == 'romanized':
            dataOut[text] = texts[i + 2]

        elif text in dataOut:
            dataOut[text] = texts[i + 1].replace('\u00a0', ' ')

    return dataOut

#page = searchForWikiPage('Godot_(game_engine)')

#print(getWikiData(page))


# -----------
# Web scraper
# -----------
# https://realpython.com/beautiful-soup-web-scraper-python/
#



# -------------
# Wikipedia API
# -------------
# https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&props=claims&titles=CD_Projekt&format=json

# ----------------
# Wikipedia search
# ----------------
# https://en.wikipedia.org/w/index.php?search=name
#
## Other
## https://en.wikipedia.org/w/index.php?search=name&title=Special%3ASearch&wprov=acrw1_0
## https://en.wikipedia.org/w/index.php?search=name&title=Special%3ASearch&wprov=acrw1_-1&fulltext=1