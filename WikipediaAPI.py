import requests
from bs4 import BeautifulSoup
import main
import pretty_errors
import lxml
import re

#page = requests.get('https://en.wikipedia.org/wiki/CD_Projekt')
#page = requests.get('https://en.wikipedia.org/wiki/FromSoftware')
#page = requests.get('https://en.wikipedia.org/wiki/Ubisoft')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Ubisoft')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Valve_Corporation')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Cryteck_Studios')
#page = requests.get('https://en.wikipedia.org/w/index.php?search=Crytek')


def searchForWikiPage(searchText):
    print('WikiAPI search:', searchText)
    return requests.get('https://en.wikipedia.org/w/index.php?search=' + searchText)

def getWikiData(page):
    soup = BeautifulSoup(page.content, 'lxml')
    results = soup.find(id='mw-content-text')
    job_elems = results.find('table', class_='infobox vcard')
    job_data = job_elems.findAll("tr")

    dataOut = {
        'Type': None,
        'Industry': None,
        'Founded': '1970-01-01',
        'Founder': None,
        'Founders': None,
        'Headquarters': None,
        'Area served': None,
        'Number of employees': 0,
        'Parent': None,
        'Native name': None,
        'Romanized': None,
        'Website': None
    }

    reNewLine = re.compile('^\n$')
    reNewLineInWord = re.compile('\\\\n')
    reUnicodeDach = re.compile('\u2013')
    reThing = re.compile("\\\\'\w+\\\\'")

    for line in job_data:
        line = line.findAll(text=True)

        if not line:
            continue

        for element in line:
            if reNewLine.match(element):
                line.remove(element)

            if reNewLineInWord.match(element):
                element.replace('\n', '')

            if reUnicodeDach.match(element):
                element.replace('\u2013', '-')

            if reQoute.match(element):
                re.sub("\\\\'\w+\\\\'", '')

        if line[0] == 'Founded':
            dataOut[line[0]] = str(main.convertDateTime(re.sub('\xa0' , ' ', line[1])))

        elif line[0] == 'Founder':
            dataOut[line[0]] = re.split(', ', line[1])

        elif line[0] == 'Founders':
            dataOut[line[0]] = []
            founder = [line[i + 1] for i in range(len(line) - 1)] if len(line) > 2 else line[1]

            if len(line) > 2:
                for part in founder:
                    if not re.compile('\n').match(part):
                        dataOut[line[0]].append(part)
            else:
                dataOut[line[0]].append(line[1])

        elif line[0] == 'Headquarters':
            dataOut[line[0]] = ''
            city = [line[i + 1] for i in range(len(line) - 1)] if len(line) > 3 else line[1]

            for part in city:
                dataOut[line[0]] += part

        elif line[0] == 'Website':
            dataOut[line[0]] = ''
            page = [line[i + 1] for i in range(len(line) - 1)] if len(line) > 2 else line[1]

            for part in page:
                dataOut[line[0]] += part

            if re.compile('^www.\w+.\w+.+\n.+$').match(dataOut[line[0]]):
                dataOut[line[0]] = re.compile(' ').split(dataOut[line[0]])[0]

        elif line[0] == 'Parent':
            for element in line:
                if re.compile('\(\d{4}-\d{4}\)').match(element):
                    re.sub('\(\d{4}-\d{4}\)', '')

            dataOut[line[0]] = []
            parent = [line[i + 1] for i in range(len(line) - 1)] if len(line) > 2 else line[1]

            if len(line) > 2:
                for part in parent:
                    if not re.compile('\w').match(part):
                        pass
                    else:
                        dataOut[line[0]].append(part)
            else:
                dataOut[line[0]].append(line[1])

        elif line[0] == 'Number of employees':
            nummber = line[1]

            nummber = nummber.replace(u'\xa0', u' ')

            if re.compile('^\w+ \d+$').match(nummber):
                nummber = nummber.split()[1]

            #if re.compile('^\[A-z]+.?\[A-z]+.?\[A-z]+$').match(nummber):
                #nummber = line[2]

            #if re.compile('^[A-z]+ \([A-z]+\)$'):
                #nummber = line[2]

            if re.compile('^Est.').match(nummber):
                nummber = str(nummber.split()[1])
                tmp = nummber.split(',')
                nummber = tmp[0] + tmp[1]

            if re.compile('^~').match(nummber):
                nummber = nummber.replace('~', '')
            
            if re.compile('^ ?\d+,?\d+ (.+)').match(nummber):
                nummber = nummber.split()[0]

            if re.compile('^\d+ \(\d+\)').match(nummber):
                nummber = nummber.split()[0]

            if re.compile('\d+.+').match(nummber):
                nummber = nummber.split()[0]

            if re.compile('\d+–\d+').match(nummber):
                nummber = str(int((int(nummber.split('–')[0]) + int(nummber.split('–')[1]) / 2)))

            if re.compile('\d+\+').match(nummber):
                nummber = nummber.split('+')[0]

            if re.compile('^\d+,\d+\+').match(nummber):
                nummber = nummber.split('+')[0]
                tmp = nummber.split(',')
                nummber = tmp[0] + tmp[1]

            if re.compile(' ?\d+,\d+').match(nummber):
                tmp = nummber.split(',')
                nummber = tmp[0] + tmp[1]

            if re.compile('≈\d+ \(\d+\)').match(nummber):
                nummber = nummber.split('≈')[1]
                nummber = nummber.split()[0]

            if re.compile('≈\d+').match(nummber):
                nummber = nummber.split('≈')[1]

            if re.compile('>\d+ \(\d+\)').match(nummber):
                nummber = nummber.split('>')[1]
                nummber = nummber.split()[0]

            if re.compile('>\d+').match(nummber):
                nummber = nummber.split('>')[1]

            if re.compile('<\d+').match(nummber):
                nummber = nummber.split('<')[1]

            dataOut[line[0]] = int(nummber)

        elif line[0] in dataOut:
            dataOut[line[0]] = [line[i + 1] for i in range(len(line) - 1)] if len(line) > 2 else line[1]

    return dataOut

if __name__ == '__main__':
    page = searchForWikiPage('ubisoft')

    print(getWikiData(page))


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