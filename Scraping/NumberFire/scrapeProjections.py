"""

Scrapes NumberFire's Daily Fantasy Projections for Draftkings.

TODO: Currently, the script grabs predictions for FanDuel. Need to somehow switch to DraftKings.

"""


import sys
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *
from bs4 import BeautifulSoup
import csv


# class to capture web page as rendered
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
# print(result)
soup = BeautifulSoup(result, 'lxml')

data = []
table = soup.find("table", attrs={'class': 'data-table xsmall','id':'complete-projection'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')


table_head = table.find('thead').find('tr',attrs={'class':'bottom'})
labels = table_head.find_all('th')

header=[]
for label in labels:
    header.append(label.getText().strip())

print(header)

writer=csv.writer(open("salaryDetails.csv",'wb'))
writer.writerow(header)

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    print cols
    writer.writerow(cols)
