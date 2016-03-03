"""

Scrape team stats and team game logs from http://stats.nba.com/teams/

"""

from bs4 import BeautifulSoup
from pandas import DataFrame
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import sys

sys.settrace

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
del r

# identify links to each team's stats and game logs
team_index = soup.find_all('div', {'class': 'team-block__links'})
type(team_index[0].contents[3])
stats_URLs = []
game_log_URLs = []
for team_num in range(0, len(team_index)):
    stats_URLs.append('http://stats.nba.com' + team_index[team_num].contents[3]['href'])
    game_log_URLs.append('http://stats.nba.com' + team_index[team_num].contents[5]['href'])
del soup

# parse each team's game log
game_logs = {}

for game_log_URL in game_log_URLs:

    # TODO: add another loop for each year
    # e.g. http://stats.nba.com/team/#!/1610612738/gamelogs/?t=celtics&Season=2014-15&SeasonType=Regular%20Season
    # TODO: maybe add loop for type of season? e.g. pre, regular, playoffs

    # convert webpage to soup
    r = Render(game_log_URL)
    result = r.frame.toHtml()
    result = str(result.toAscii())
    log_soup = BeautifulSoup(result, 'lxml')
    del r

    # extract matchup
    matchups = [str(ele.text) for ele in log_soup.find_all('td', {'class': 'player'})]

    # extract all twenty columns
    matchup_data = log_soup.find_all('td', {'class': 'ng-binding'})

    # win/loss
    wl = [str(ele.text) for ele in matchup_data[0::20]]

    # minutes a player or team has played
    minutes = [str(ele.text) for ele in matchup_data[1::20]]

    # points scored
    points = [str(ele.text) for ele in matchup_data[2::20]]

    # field goals (2 and 3 pointers) made
    fgm = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[3::20]]

    # field goals (2 and 3 pointers) attempted
    fga = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[4::20]]

    # field goal percentage i.e. fgm/fga
    fgp = [float(str(ele.text)) for ele in matchup_data[5::20]]

    # 3 pointers made
    threepm = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[6::20]]

    # 3 pointers attempted
    threepa = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[7::20]]

    # 3 pointers percentage
    threepp = [float(str(ele.text)) for ele in matchup_data[8::20]]

    # free throws made
    ftm = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[9::20]]

    # free throws attempted
    fta = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[10::20]]

    # free throw percentage
    ftp = [float(str(ele.text)) for ele in matchup_data[11::20]]

    # offensive rebounds
    orb = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[12::20]]

    # defensive rebounds
    drb = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[13::20]]

    # total rebounds
    trb = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[14::20]]

    # assists
    ass = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[15::20]]

    # steals
    steals = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[16::20]]

    # blocks
    blocks = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[17::20]]

    # turnovers
    turnov = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[18::20]]

    # personal fouls
    fouls = [int(str(ele.text).strip(' \n\n\n\nVideo\nShotchart\n\n\n\n\n\n')) for ele in matchup_data[19::20]]

    # create dataframe and add to game logs hash
    game_logs[game_log_URL[52::]] = DataFrame(data={'W/L': wl, 'Minutes': minutes, 'Matchup': matchups,
                                                         'Points': points, 'FGM': fgm, 'FGA': fga, 'FG%': fgp,
                                                         '3PM': threepm, '3PA': threepa, '3P%': threepp, 'FTM': ftm,
                                                         'FTA': fta, 'FT%': ftp, 'OREB': orb, 'DREB': drb,
                                                         'Assists': ass, 'Steals': steals, 'Blocks': blocks,
                                                         'Turnovers': turnov, 'PF': fouls})


# parse each team's stat page
    pass