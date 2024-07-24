# IP No 3 in a line problem

### INTRODUCTION

This project's goal is finding a feasible solution to `No 3 in a line` problem using Integer Programming. 

### PROBLEM DESCRIPTION

Given a grid of size `n x n`, the goal is to find a feasible solution to the problem of placing maximum elements on the grid such that no 3 elements are in a straight line.

### APPROACH

This can be found in `Report.pdf` file.

### REQUIREMENTS

- Python 3.6+
- Gurobi Optimizer
- Gurobi Python interface
- Matplotlib (for visualization)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install gurobipy matplotlib
   ```

2. **Set up Gurobi**:
   Follow the [official Gurobi installation guide](https://www.gurobi.com/documentation/9.1/quickstart_linux/software_installation_guid.html) to install Gurobi and obtain a license.

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

   Then you will be prompted to enter the grid size `n`. The script will then solve the problem using Gurobi and save the result as a image.

2. **View the results**:
   The visualizations will be saved as images in the current directory. For example, `n_15.png` shows the optimal solution for a 15x15 grid.