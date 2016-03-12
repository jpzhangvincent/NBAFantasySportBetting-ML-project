# credit to http://tauserver.wtb.tue.nl/johan/3DprintFactory_ProductionPlanning/knapsack.py
# for teaching us how to use pulp to solve a knapsack-like problem

import glob
import numpy
import pandas
import pulp

# create dataframe of past salaries
list = []
for file in glob.glob('Data/SalaryHistory/*.csv'):
    list.append(pandas.read_csv(file, sep=';'))
pastsalaries = pandas.concat(list)
pastsalaries = pastsalaries.dropna()
pastsalaries['DK Salary'] = pastsalaries['DK Salary'].astype(str).map(
    lambda ele: int(ele.replace('$', '').replace(',', '')))
pastsalaries.head()

# create dataframe of past winning lineups
# pastwinners = pandas.read_csv('Scraping/NumberFire/numberFireBestTeam.csv')
# # strip '$' from Salary, convert to integer
# pastwinners['Salary'] = pastwinners['Salary'].map(lambda ele: int(ele.replace('$', '')))


specificDate = pastsalaries[pastsalaries['Date'] == 20160306]

specificDate.head()


# initialize variables
playerPositions = specificDate['Pos'].tolist()
playerNames = specificDate['Name'].tolist()
playerTeams = tuple(specificDate['Team'].unique())
playerCosts = tuple(specificDate['DK Salary'])
playerPoints = tuple(specificDate['DK Pts'])
salaryCap = 55000
numOfPlayers = range(len(playerCosts))

# create problem
problem = pulp.LpProblem("Optimal Line-Up", pulp.LpMaximize)

# create variable to represent each player
playerInLineup = pulp.LpVariable.dicts("Players", [i for i in numOfPlayers], 0, 1, cat="Binary")

# objective: maximize sum of player points
problem += pulp.lpSum(playerInLineup[i] * playerPoints[i] for i in numOfPlayers)

# constraint: each player can only be chosen at most once
for i in numOfPlayers:
    problem += pulp.lpSum(playerInLineup[i]) <= 1

# constraints: sum of player costs must be less than or equal to the salary cap
problem += pulp.lpSum(playerInLineup[i] * playerCosts[i] for i in numOfPlayers) <= salaryCap

# constraint: teams must have 8 players
problem += pulp.lpSum(problem.variables()) == 8

# constraint: 1 <= number of PG <= Max 3
pointguards = tuple(specificDate['Pos'] == 'PG')
problem += pulp.lpSum(playerInLineup[i] * pointguards[i] for i in numOfPlayers) >= 1
problem += pulp.lpSum(playerInLineup[i] * pointguards[i] for i in numOfPlayers) <= 3

# constraint: 1 <= number of SG <= Max 3
shootguards = tuple(specificDate['Pos'] == 'SG')
problem += pulp.lpSum(playerInLineup[i] * shootguards[i] for i in numOfPlayers) >= 1
problem += pulp.lpSum(playerInLineup[i] * shootguards[i] for i in numOfPlayers) <= 3

# constraint: 1 <= number of SF <= Max 3
smallforward = tuple(specificDate['Pos'] == 'SF')
problem += pulp.lpSum(smallforward[i] * playerInLineup[i] for i in numOfPlayers) >= 1
problem += pulp.lpSum(smallforward[i] * playerInLineup[i] for i in numOfPlayers) <= 3

# constraint: 1 <= number of PF <= Max 3
powerfoward = tuple(specificDate['Pos'] == 'PF')
problem += pulp.lpSum(powerfoward[i] * playerInLineup[i] for i in numOfPlayers) >= 1
problem += pulp.lpSum(powerfoward[i] * playerInLineup[i] for i in numOfPlayers) <= 3

# constraint: 1 <= number of C <= Max 2
centers = tuple(specificDate['Pos'] == 'C')
problem += pulp.lpSum(playerInLineup[i] * centers[i] for i in numOfPlayers) <= 2
problem += pulp.lpSum(playerInLineup[i] * centers[i] for i in numOfPlayers) >= 1

# create variables for teams
teamsInLineup = pulp.LpVariable.dicts("Teams", [i for i in specificDate['Team'].unique()], 0, 1, cat="Binary")
teams = tuple(specificDate['Team'])

# constraint: at least two different teams must be chosen
# TODO: test this constraint more thoroughly
# problem += pulp.lpSum(playerInLineup[i] * (teams[i] == key)
#                       for i in numOfPlayers for key in teamsInLineup.keys()) >= 3

# constraint: at least two different games must be chosen



# if solved, print players. otherwise, print error message
if problem.solve() == 1:
    for pos in range(len(numOfPlayers)):
        if playerInLineup[pos].value() == 1:
            print '%25s, Present = %1.0f, Position = %2s, Price = %5.f, Points = %3.2f, Team = %3s' \
                  % (playerNames[pos], playerInLineup[pos].value(), playerPositions[pos], playerCosts[pos],
                     playerPoints[pos], teams[pos])
else:
    print 'Error finding solution'
