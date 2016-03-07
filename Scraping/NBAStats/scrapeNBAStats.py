"""

Scrape team stats and team game logs from http://stats.nba.com/teams/

"""

import os
import pickle
import scrapeURLs
import scrapeGameLog

# if urls pickle files do not exist, create them
if not os.path.isfile('../../Data/gamelogURLs.pickle') and not os.path.isfile('../../Data/statsURLs.pickle'):
    scrapeURLs.scrapeURLs()

print 'scraped urls'

# import game log URLs and team stats URLs
game_log_URLs = pickle.load(open('../../Data/gamelogURLs.pickle', 'rb'))
stats_URLs = pickle.load(open('../../Data/statsURLs.pickle', 'rb'))

print 'imported pickle files'

# parse each team's game log
game_logs = {}

for game_log_URL in game_log_URLs:

    df = scrapeGameLog.scrapeGameLog(game_log_URL)

    # create dataframe and add to game logs hash
    game_logs[game_log_URL[52::]] = df

# save to file
pickle.dump(game_log_URLs, open('../../Data/gamelogs.pickle', 'wb'))
