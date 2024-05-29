from gurobipy import GRB, Model, quicksum #*
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np


def Output(m):
    # Print the result
    status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'} #this is how a 'dictionary'
                                                                                            #is defined in Python
    status = m.status

    print('The optimization status is ' + status_code[status])
    if status == 2:
        # Retrieve variables value
        print('Optimal solution:')
        for v in m.getVars():
            print(str(v.varName) + " = " + str(v.x))
        print('Optimal objective value: ' + str(m.objVal) + "\n")

m = Model('no_three')

#problem definition: find a feasible solution to the following problem
# you have a n * n grid, and you want to place maximum number of dots on it such that no three dots are in the same line

n = 8

#variables
x = m.addVars(n, n, vtype=GRB.BINARY, name = ["x_" + str(i) + "_" + str(j) for i in range(n) for j in range(n)])

#objective
m.setObjective(x.sum(), GRB.MAXIMIZE)

#approach
# We hold every possible slope in a list by adding every possible i,j pair to the list
# At the same time, we hold the slope value in a set to avoid redundant i,j pairs (e.g 2,4 and 4,8 are the same)

slopes = [] # represents slope of i/j, stored as tuples inside
slopeSet = set() # to avoid redundant i,j pairs
for i in range(1,n):
    for j in range(1,n):
        if (i/ j) not in slopeSet: #avoid redundant i,j pairs
            if not (i/j > n/2) and not (j/i > n/2):
                slopes.append((i, j))
                slopeSet.add((i/ j))

# add this for vertical and horizontal lines
slopes.append((0, 1))
slopes.append((1, 0))


for a in range(n):
    for b in range(n):
        for i,j in slopes:
            # no need to check for -j, since we are checking for right side of the every cell,
            # but checking for left side of the cell would be redundant (if statement holds for right side of the leftmost cell, it also holds for left side of the rightmost cell)
            m.addConstr(quicksum(x[(a + i * k), (b + j * k)] for k in range(n) if a + i * k >= 0 and a + i * k < n and b + j * k >= 0 and b + j * k < n) <= 2)
            m.addConstr(quicksum(x[(a - i * k), (b + j * k)] for k in range(n) if a - i * k >= 0 and a - i * k < n and b + j * k >= 0 and b + j * k < n) <= 2)

m.optimize()

# Output(m)

## Below this line is the visualization of the solution

# print(slopes)

points = []
for v in m.getVars():
    if v.x == 1:
        points.append([v.index//n, v.index%n])


#verify solution - this part is not necessary, but it is a good practice to verify the solution by code
flag = True
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        for k in range(j + 1, len(points)):
            x1, y1 = points[i]
            x2, y2 = points[j]
            x3, y3 = points[k]
            if (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1): # check if the three points are in the same line by checking if the slopes are equal
            # it is same as (y2 - y1) / (x2 - x1) == (y3 - y1) / (x3 - x1), but we avoid division by zero by cross multiplication
                print("Three points are in the same line")
                print(points[i], points[j], points[k])
                flag = False
if flag:
    print("Solution is correct")
    print("Visualizing the solution")
else:
    print("Solution is incorrect")
    print("Exiting the program")
    exit()

# make a plot of the solution
fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(0, n)
ax.set_ylim(0, n)
ax.set_xticks(np.arange(n + 1))
ax.set_yticks(np.arange(n + 1))
ax.grid(True, which='both', color='k', linestyle='-', linewidth=1)

# Add blue squares for the selected points
for point in points:
    square = patches.Rectangle(point, 1, 1, fill=True, color='blue')
    ax.add_patch(square)

plt.savefig(f'n_{n}.png')  # Save the plot to a PNG file
plt.close(fig)  # Close the figure to free up memory







# Iteration 2:
#  1.0     0.0     0.0     0.0     0.0     0.0     2.0     0.0     178.0
#  0.0     0.273   1.0     0.0     0.0     0.0     0.045   0.0     9.364
#  0.0     0.273   0.0     1.0     0.0     0.0     0.045   0.0     0.364
#  0.0     -5.455  0.0     0.0     1.0     0.0     0.091   0.0     5.727

# Optimal basis:
# [0, 2, 3, 4]
# Optimal value:
#  178.0
# Optimal solution (basic variables in the order of the basis):
#  9.364
#  0.364
#  5.727

# .................................