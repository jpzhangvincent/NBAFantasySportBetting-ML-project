# credit to http://tauserver.wtb.tue.nl/johan/3DprintFactory_ProductionPlanning/knapsack.py
# for teaching us how to use pulp to solve a knapsack-like problem

import glob
import pandas
import pulp

# create dataframe of past salaries
list = []
for file in glob.glob('Data/SalaryHistory/*.csv'):
    list.append(pandas.read_csv(file, sep=';'))
pastsalaries = pandas.concat(list)
pastsalaries = pastsalaries.dropna()
pastsalaries['DK Salary'] = pastsalaries['DK Salary'].astype(str).map(lambda ele: int(ele.replace('$', '').replace(',','')))
pastsalaries.head()

# create dataframe of past winning lineups
# pastwinners = pandas.read_csv('Scraping/NumberFire/numberFireBestTeam.csv')
# # strip '$' from Salary, convert to integer
# pastwinners['Salary'] = pastwinners['Salary'].map(lambda ele: int(ele.replace('$', '')))


specificDate = pastsalaries[pastsalaries['Date'] == 20160306]


# initialize variables

playerNames = specificDate['Name'].tolist()
playerCosts = tuple(specificDate['DK Salary'])
playerPoints = tuple(specificDate['DK Pts'])
salaryCap = 55000
numOfPlayers = range(len(playerCosts))

# create problem
problem = pulp.LpProblem("Optimal Line-Up", pulp.LpMaximize)

# create variable to represent each player
player_vars = pulp.LpVariable.dicts("Players", [i for i in numOfPlayers], 0, 1, cat="Binary")

# objective: maximize sum of player points
problem += pulp.lpSum(player_vars[i] * playerPoints[i] for i in numOfPlayers)

# constraints: each player can only be chosen at most once
for i in numOfPlayers:
    problem += pulp.lpSum(player_vars[i]) <= 1

# constraints: sum of player costs must be less than or equal to the salary cap
problem += pulp.lpSum(player_vars[i] * playerCosts[i] for i in numOfPlayers) <= salaryCap

# if solved, print players. otherwise, print error message
if problem.solve() == 1:
    for pos in range(len(problem.variables())):
        print '%30s, Present = %1.0f' % (playerNames[pos], problem.variables()[pos].varValue)
else:
    print 'Error finding solution'