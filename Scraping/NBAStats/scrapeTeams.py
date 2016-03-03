"""

Scrape team stats and team game logs from http://stats.nba.com/teams/

"""

from bs4 import BeautifulSoup
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

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

# convert webpage to soup object
r = Render('http://stats.nba.com/teams/')
result = r.frame.toHtml()
result = str(result.toAscii())
soup = BeautifulSoup(result, 'lxml')

# identify links to each team's stats and game logs
team_index = soup.find_all('div', {'class': 'team-block__links'})
type(team_index[0].contents[3])
team_stats_URLs = []
team_game_log_URLs = []
for team_num in range(0, len(team_index)):
    team_stats_URLs.append('http://stats.nba.com/' + team_index[team_num].contents[3]['href'])
    team_game_log_URLs.append('http://stats.nba.com/' + team_index[team_num].contents[5]['href'])

# parse each team's game log
for team_game_log_URL in team_game_log_URLs:
    pass


# parse each team's stat page
    pass