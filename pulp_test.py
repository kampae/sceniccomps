import pulp

dist = {("A", "B"): 10.0,
        ("A", "C"): 15.0,
        ("A", "D"): 12.0,
        ("A", "E"): 30.0,
        ("A", "F"): 50.0,
        ("B", "C"): 5.0,
        ("B", "D"): 7.0,
        ("B", "E"): 16.0,
        ("B", "F"): 40.0,
        ("C", "E"): 8.0,
        ("C", "D"): 9.0,
        ("C", "F"): 30.0,
        ("D", "E"): 4.0,
        ("D", "F"): 20.0,
        ("E", "F"): 10.0}
probs= {"A": .2,
       "B": .3,
       "C": .9,
       "D": .3,
       "E": .5,
       "F": .8}
node_list = ["A", "B", "C", "D", "E", "F"]
max_dist = 50

y = pulp.LpVariable.dicts("y", dist, lowBound=0, upBound=1, cat=pulp.LpInteger)

mod = pulp.LpProblem("Scenic Routes", pulp.LpMaximize)

# Objective
mod += sum([probs[k[0]]*y[k] for k in dist])

# CONSTRAINTS:

# route is shorter than max distance
mod += sum([dist[k] * y[k] for k in dist]) <= max_dist

# every node is visited no more than one time
for point in range(1, len(node_list)-1):
    mod += sum([y[k] for k in dist if node_list[point] in k[0]]) <= 1
    mod += sum([y[k] for k in dist if node_list[point] in k[1]]) <= 1
    mod += sum([y[k] for k in dist if node_list[point] in k[0]]) == sum([y[k] for k in dist if node_list[point] in k[1]])
    
# start point is start point
mod += sum([y[k] for k in dist if node_list[0] in k[0]]) == 1
mod += sum([y[k] for k in dist if node_list[0] in k[1]]) == 0

# end point is end point
mod += sum([y[k] for k in dist if node_list[len(node_list)-1] in k[0]]) == 0
mod += sum([y[k] for k in dist if node_list[len(node_list)-1] in k[1]]) == 1


# Solve
mod.solve()
for t in dist:
    if(y[t].value() == 1):
        print(t)