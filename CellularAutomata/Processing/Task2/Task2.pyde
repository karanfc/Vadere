#Data regarding the positions of pedestrians, targets
obstacles = []
targetX, targetY = 20, 25
cols, rows = 50, 50
resolution = 15
grid_t = []
cost_function = []
t = 0
rmax = 3
pedestrians = []
pedestrians = [[5, 25]]
time = 0
INFINITY = 10000;

def setup():
    
    """
    Does the initial setup for the visualizaiton by creating the data matrix, rendering it once and setting the frame rate

    :param :
    :return: 
    
    """
    
    global grid_t, cost_function, targetX, targetY, obstacles

    size(900,900)
    grid_t = populateGrid(pedestrians)
    renderGrid(grid_t)
    cost_function = calculateCostFunction()  
    frameRate(2)        


def draw():
    
    """
    Plots the data matrix repeatedly to represent the scenario

    :param :
    :return: 
    
    """
    
    global grid_t, cost_function, i
    background('#000000') 
    pedestrians = updateTimeStep()
    grid_t = populateGrid(pedestrians)
    renderGrid(grid_t)


def calculateCostFunction():
    
    """
    Calculate the cost of each point. The distance of the point to the target cell

    :param :
    :return: matrix containing the cost values for each point.
    
    """    
    global grid_t
    cost_function = [[0 for c in range(cols)] for r in range(rows)]
    for c in range(cols):
        for r in range(rows):
            if grid_t[c][r] != 'O':
                cost = sqrt(pow(c - targetX + 1, 2) + pow(r - targetY + 1, 2))
                cost = cost / sqrt(pow(rows, 2) + pow(cols, 2))
                cost_function[c][r] = cost
            else:
                cost_function[c][r] = INFINITY
          
    return cost_function
 
    
def populateGrid(pedestrians):
    """
    Takes in data about the scenario and creates a grid matrix that contains the data representing the scenario.

    :param: lists of positions of pedestrians, obstacle and the target, number of rows and columns of the grid:
    :return: the data matrix representing the scenario
    
    """
    
    grid_t = [['0' for c in range(cols)] for r in range(rows)]
    grid_t[targetX - 1][targetY - 1] = 'T'
    for p in pedestrians:
        grid_t[p[0] - 1][p[1] - 1] = 'P'

    return grid_t

def renderGrid(grid_t):
    """
    Gets data in the data matrix and displays the scenario.

    :param: the data matrix representing the scenario 
    :return:
    
    """
    for c in range(cols):
        for r in range(rows):
            x = c * resolution
            y = r * resolution
            stroke('#000000')
            if grid_t[c][r] == '0':
                fill('#ffffff')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'T':
                fill('#00FF00')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'P':
                fill('#0000FF')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'O':
                fill('#FF0000')
                rect(x, y, resolution - 1, resolution - 1)
                
            
def findNextStep(p):
    """
    Finds the next step for a pedestrian in its journey to the target

    :param: the coordinates of the pedestrian 
    :return: the coordinates of the next position that the pedestrian takes
    
    """
    
    global pedestrians, grid_t
    next_x, next_y = p[0], p[1]  
    current_cost = cost_function[p[0] - 1][p[1] - 1] 
    
    if (p[0] - 1 > 0 and cost_function[p[0] - 2][p[1] - 1]  < current_cost and cost_function[p[0] - 2][p[1] - 1] > 0) and grid_t[p[0] - 2][p[1] - 1] != 'P':
        next_x, next_y = p[0] - 1, p[1] 
        current_cost = cost_function[p[0] - 2][p[1] - 1]
    
    if (p[0] + 1 < cols and cost_function[p[0]][p[1] - 1]  < current_cost and cost_function[p[0]][p[1] - 1] > 0) and grid_t[p[0]][p[1] - 1] != 'P':
        next_x, next_y = p[0] + 1, p[1] 
        current_cost = cost_function[p[0]][p[1] - 1]
        
    if (p[1] - 1 > 0 and cost_function[p[0] - 1][p[1] - 2]  < current_cost and cost_function[p[0] - 1][p[1] - 2] > 0) and grid_t[p[0] - 1][p[1] - 2] != 'P':
        next_x, next_y = p[0], p[1] - 1
        current_cost = cost_function[p[0] - 1][p[1] - 2] 
        
    if (p[1] + 1 < rows and cost_function[p[0] - 1][p[1]]  < current_cost and cost_function[p[0] - 1][p[1]] > 0) and grid_t[p[0] - 1][p[1]] != 'P':
        next_x, next_y = p[0], p[1] + 1
        current_cost = cost_function[p[0] - 1][p[1]]
    return next_x, next_y

        
def updateTimeStep():
    
    """
    For each pedestrian, find its next position in the grid. If the pedestrian 

    :param: the data matrix representing the scenario, the dimension, resolution of the grid 
    :return: the set of new coordinates for the pedestrians
    
    """
    global pedestrians
    for p in pedestrians: 
        p[0], p[1]  = findNextStep(p)
    return pedestrians
