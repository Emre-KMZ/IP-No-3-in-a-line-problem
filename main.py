from gurobipy import GRB, Model, quicksum
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def Output(model):
    status_code = {1: 'LOADED', 2: 'OPTIMAL', 3: 'INFEASIBLE', 4: 'INF_OR_UNBD', 5: 'UNBOUNDED'}
    status = model.status
    print(f'The optimization status is {status_code[status]}')
    
    if status == GRB.OPTIMAL:
        print('Optimal solution:')
        for v in model.getVars():
            print(f'{v.varName} = {v.x}')
        print(f'Optimal objective value: {model.objVal}\n')


def verify_solution(points, n):
    # Only used for verifying the solution. Thus, not needed for the optimization
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                x3, y3 = points[k]
                if (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1):
                    print("Three points are in the same line")
                    print(points[i], points[j], points[k])
                    return False
    return True


def plot_solution(points, n):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_xticks(np.arange(n + 1))
    ax.set_yticks(np.arange(n + 1))
    ax.grid(True, which='both', color='k', linestyle='-', linewidth=1)

    for point in points:
        square = patches.Rectangle(point, 1, 1, fill=True, color='blue')
        ax.add_patch(square)

    plt.savefig(f'n_{n}.png')
    plt.close(fig)


def main():
    n = 8
    model = Model('no_three')

    x = model.addVars(n, n, vtype=GRB.BINARY, name="x")

    model.setObjective(quicksum(x[i, j] for i in range(n) for j in range(n)), GRB.MAXIMIZE)

    slopes = [] # represents slope of i/j, stored as tuples inside
    slopeSet = set() # to avoid redundant i,j pairs
    for i in range(1,n):
        for j in range(1,n):
            if (i/ j) not in slopeSet: #avoid redundant i,j pairs
                if not (i/j > n/2) and not (j/i > n/2):
                    slopes.append((i, j))
                    slopeSet.add((i/ j))
    slopes += [(0, 1), (1, 0)]

    for a in range(n):
        for b in range(n):
            for i, j in slopes:
                model.addConstr(quicksum(x[a + i * k, b + j * k] for k in range(n) if 0 <= a + i * k < n and 0 <= b + j * k < n) <= 2)
                model.addConstr(quicksum(x[a - i * k, b + j * k] for k in range(n) if 0 <= a - i * k < n and 0 <= b + j * k < n) <= 2)

    model.optimize()
    Output(model)

    points = [(v.index // n, v.index % n) for v in model.getVars() if v.x == 1]

    if verify_solution(points, n):
        print("Solution is correct\nVisualizing the solution")
        plot_solution(points, n)
    else:
        print("Solution is incorrect\nExiting the program")
        exit()


if __name__ == "__main__":
    main()
