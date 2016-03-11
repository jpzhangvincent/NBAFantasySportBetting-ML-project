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
pastwinners = pandas.read_csv('Scraping/NumberFire/numberFireBestTeam.csv')
# strip '$' from Salary, convert to integer
pastwinners['Salary'] = pastwinners['Salary'].map(lambda ele: int(ele.replace('$', '')))



# calculate optimal lineup
playerCosts = (5,2,5,5,10,12,14,5,6)
playerPoints = (9,3,5,3,5,1,9,4,4)
salaryCap = 10
numOfPlayers = range(len(playerCosts))

problem = pulp.LpProblem("Optimal Line-Up", pulp.LpMaximize)

assign_vars = pulp.LpVariable.dicts("ItemInKnapsack",
              [i for i in numOfPlayers],
              0, 1, cat="Binary")


# objective: maximize sum of player points
problem += pulp.lpSum(assign_vars[i] * playerPoints[i] for i in numOfPlayers)

# constraints: each player can only be chosen at most once
for i in numOfPlayers:
    problem += pulp.lpSum(assign_vars[i]) <= 1

# constraints: sum of player costs must be less than or equal to the salary cap
problem += pulp.lpSum(assign_vars[i] * playerCosts[i] for i in numOfPlayers) <= salaryCap

# solve problem with the COIN CBC solver
#solver = pulp.PULP_CBC_CMD(options=[],keepFiles = 0, msg=1, fracGap=0, maxSeconds = "100")
#problem.solve(solver)
problem.solve()

# print solution
print("\n\nThe solution:\n")

print "Knapsack contains items:"
k=0
for i in numOfPlayers:
    if assign_vars[i].varValue > 0:
        k = k + assign_vars[i].varValue*playerCosts[i]
        print(i)
print "with cumulative volume:", round(k, 2), "\n"
solutionCost = sum(assign_vars[i].varValue * playerPoints[i]  for i in numOfPlayers)
print "\nThe solution contains:",round(solutionCost),"\n"


for v in problem.variables():
    print v.name, "=", v.varValue