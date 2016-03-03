'''

This script scrapes NumberFire's Daily Fantasy Projections for Draftkings.

TODO: Currently, the script grabs predictions for FanDuel. Need to somehow switch to DraftKings.

'''


import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *
from bs4 import BeautifulSoup


# Take this class for granted.Just use result of rendering.
class Render(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

url = 'http://www.numberfire.com/nba/fantasy/full-fantasy-basketball-projections'
r = Render(url)  
result = r.frame.toHtml()

result = str(result.toAscii())

soup = BeautifulSoup(result, 'lxml')

data = []
table = soup.find("table", attrs={'class': 'data-table xsmall'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    print cols
