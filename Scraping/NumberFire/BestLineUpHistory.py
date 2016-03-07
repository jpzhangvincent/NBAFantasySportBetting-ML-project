"""

Scrapes

"""

import json
import urllib
import urllib2
from datetime import date, datetime, timedelta
import random

USER_AGENTS_FILE = "user_agents.txt"





def getNumberFireURL(searchfor,header):
    # f=open('numberfire2.txt','a+')
    query = urllib.urlencode({'q': searchfor})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query

    req = urllib2.Request(url,None,header)

    search_results = urllib2.urlopen(req).read()

    results = json.loads(search_results)
    data = results['responseData']
    hits = data['results']
    for h in hits:
        if "numberfire" and 'yesterday' in h['url']:
            print h['url']
          # f.write(h['url']+"\n")




def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta



def LoadUserAgents(uafile=USER_AGENTS_FILE):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas


uas = LoadUserAgents()



# getNumberFireURL("Yesterday's Perfect NBA DFS Lineups 2015-11-16")

SEARCH_TEXT_PREFIX= "Yesterday's Perfect NBA DFS Lineups "

for result in perdelta(date(2015, 11, 16), datetime.now().date(), timedelta(days=1)):
    print result
    # time.sleep(randint(30,100))
    ua = random.choice(uas)  # select a random user agent
    headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : ua}

    # getNumberFireURL(SEARCH_TEXT_PREFIX+str(result),headers)


