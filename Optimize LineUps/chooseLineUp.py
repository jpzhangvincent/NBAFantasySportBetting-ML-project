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
tie = 0
win = 0
lose = 0
total = 0

idealvspredicted = pandas.DataFrame()


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
    teams = specificDate['Team'].tolist()
    playerTeams = tuple(specificDate['Team'].unique())
    playerCosts = tuple(specificDate['DK Salary'])
    playerPoints = tuple(specificDate['DK Pts'])
    salaryCap = 50000
    numOfPlayers = range(len(playerCosts))

    # create problem
    problem = pulp.LpProblem("Optimal Lineup", pulp.LpMaximize)

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
    predictedcost = 0
    predictedpoints = 0

    predicted = set()
    if problem.solve() == 1:
        for pos in range(len(numOfPlayers)):
            if playerInLineup[pos].value() == 1:
                name = playerNames[pos]
                predicted.add(name)
                predictedcost += playerCosts[pos]
                predictedpoints += playerPoints[pos]
                # print '%25s, Position = %2s, Price = %5.f, Points = %3.2f, Team = %3s' \
                #       % (playerNames[pos], playerPositions[pos], playerCosts[pos],
                #          playerPoints[pos], teams[pos])
        # print '\nTotal Team Cost: %5d\nTotal Team Points: %3.2f' % (predictedcost, predictedpoints)
    else:
        print 'Error finding solution'

    # convert date to alternative format to look up past winners
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

    idealcost = sum(pastwinners[pastwinners['Date'] == date]['Salary'])
    idealpoints = sum(pastwinners[pastwinners['Date'] == date]['FP'])

    # print '\nTotal Team Cost: %5d\nTotal Team Points: %3.2f' % (idealcost, idealpoints)


    if idealpoints > 0 and idealpoints == predictedpoints:
        tie += 1
    elif idealpoints > 0 and idealpoints < predictedpoints:
        win += 1
    elif idealpoints > 0:
        lose += 1
    else:
        total -= 1
    total += 1

print 'Win: ', float(win) / total
print 'Tie: ', float(tie) / total
print 'Lose: ', float(lose) / total
print 'Total: ', float(win+lose+tie) / total


