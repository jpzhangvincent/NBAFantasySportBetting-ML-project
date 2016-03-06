__author__ = 'rylan'

from bs4 import BeautifulSoup
import pickle

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import sys

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


def scrapeURLs():

    # convert webpage to soup object
    r = Render('http://stats.nba.com/teams/')
    result = str(r.frame.toHtml().toAscii())
    del r
    soup = BeautifulSoup(result, 'lxml')
    del result

    # identify links to each team's stats and game logs
    team_index = soup.find_all('div', {'class': 'team-block__links'})
    soup.decompose()

    game_log_URLs = []
    stats_URLs = []

    # record urls for each team and each game log
    for team_num in range(0, len(team_index)):
        stats_URLs.append('http://stats.nba.com' + team_index[team_num].contents[3]['href'])
        game_log_URLs.append('http://stats.nba.com' + team_index[team_num].contents[5]['href'])

    # pickle urls
    pickle.dump(game_log_URLs, open('../../Data/gamelogURLs.pickle', 'wb'))
    pickle.dump(stats_URLs, open('../../Data/statsURLs.pickle', 'wb'))
