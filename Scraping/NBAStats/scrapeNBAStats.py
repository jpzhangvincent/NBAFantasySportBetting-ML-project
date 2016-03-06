"""

Scrape team stats and team game logs from http://stats.nba.com/teams/

"""

import os
import pickle
import scrapeURLs
import scrapeGameLog

# if urls pickle files do not exist, create them
if not os.path.isfile('gamelogURLs.pkl') and not os.path.isfile('statsURLs.pkl'):
    scrapeURLs.scrapeURLs()

print 'scraped urls'

# import game log URLs and team stats URLs
game_log_URLs = pickle.load(open('gamelogURLs.pkl', 'rb'))
stats_URLs = pickle.load(open('statsURLs.pkl', 'rb'))

print 'imported pickle files'

# parse each team's game log
game_logs = {}

count = 1

for game_log_URL in game_log_URLs:

    print count

    count += 1

    df = scrapeGameLog.scrapeGameLog(game_log_URL)

    # create dataframe and add to game logs hash
    game_logs[game_log_URL[52::]] = df

# save to file
pickle.dump(game_log_URLs, open('gamelogs.pkl', 'wb'))
