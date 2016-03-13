# credit to http://tauserver.wtb.tue.nl/johan/3DprintFactory_ProductionPlanning/knapsack.py
# for teaching us how to use pulp to solve a knapsack-like problem

import glob
import pandas
import pulp


# create dataframe of past salaries
list = []
for file in glob.glob('../Data/SalaryHistory/*.csv'):
    list.append(pandas.read_csv(file, sep=';'))
pastsalaries = pandas.concat(list)
pastsalaries['DK Salary'] = pastsalaries['DK Salary'].astype(str).map(
    lambda ele: ele if ele == 'nan' else int(ele.replace('$', '').replace(',', '')))
del list


# create dataframe of past perfect lineups
pastwinners = pandas.read_csv('../Scraping/NumberFire/numberFireBestTeam.csv')
# # strip '$' from Salary, convert to integer
pastwinners['Salary'] = pastwinners['Salary'].map(lambda ele: int(ele.replace('$', '')))



# create cumulative, total to track accuracy
cum = 0
total = 0


for date in pastsalaries['Date'].unique():

    # isolate data for specific date
    specificDate = pastsalaries[pastsalaries['Date'] == date]

    # exclude players with missing salaries
    specificDate = specificDate[specificDate['DK Salary'] != 'nan']

    # exclude players with missing points
    #specificDate = specificDate[specificDate['DK Pts'] != 'nan']

    # initialize variables
    playerPositions = specificDate['Pos'].tolist()
    playerNames = specificDate['Name'].tolist()
    playerTeams = tuple(specificDate['Team'].unique())
    playerCosts = tuple(specificDate['DK Salary'])
    playerPoints = tuple(specificDate['DK Pts'])
    salaryCap = 50000
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
    problem += sum(playerInLineup[i] * playerCosts[i] for i in numOfPlayers) <= salaryCap

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

    # calculated predicted lineup
    predicted = set()
    if problem.solve() == 1:
        for pos in range(len(numOfPlayers)):
            if playerInLineup[pos].value() == 1:
                name = playerNames[pos]
                predicted.add(name)
    else:
        print 'Error finding solution'

    # convert date to alternative format to look up psat winners
    date = str(int(date))
    day = date[6:8][1] if int(date[6:8]) < 10 else date[6:8]
    month = date[4:6][1] if int(date[4:6]) < 10 else date[4:6]
    year = date[2:4]
    date = month + '-' + day + '-' + year

    # calculate ideal lineup
    ideal = set()
    for name in pastwinners[pastwinners['Date'] == date]['PlayerName']:
        name = name.split()
        name = name[1] + ', ' + name[0]
        ideal.add(name)


    # if all positions were predicted correctly, add 8 to cumulative
    # if no ideal data, remove from total
    # otherwise, print differences
    if len(predicted.intersection(ideal)) == 8:
        cum += 8
    elif len(ideal) == 0:
        total -= 8
    else:
        print predicted.difference(ideal)
        print ideal.difference(predicted)
        cum += len(predicted.intersection(ideal))

    total += 8

print 1.0 * cum / total












# points = 0
# cost = 0

# if solved, print players. otherwise, print error message
# if problem.solve() == 1:
#     for pos in range(len(numOfPlayers)):
#         if playerInLineup[pos].value() == 1:
#             print '%25s, Present = %1.0f, Position = %2s, Price = %5.f, Points = %3.2f, Team = %3s' \
#                   % (playerNames[pos], playerInLineup[pos].value(), playerPositions[pos], playerCosts[pos],
#                      playerPoints[pos], teams[pos])
#             points += playerPoints[pos]
#             cost += playerCosts[pos]
#     print points
#     print cost
# else:
#     print 'Error finding solution'