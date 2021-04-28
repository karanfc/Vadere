#gloabsl vars
targetX, targetY = 40, 40
cols, rows = 80, 80
resolution = 12
grid_t = []
cost_function = []
t = 0
rmax = 1.1
pedestrians = []
pedestrians = [[10, 40], [16,22],[16, 58],[40, 70], [40, 10], [22, 16]]#pedestrains with distance 30m from target
time = 0
INFINITY = 10000;


##
#initial grid display
##
def setup():
    global grid_t, cost_function, targetX, targetY
    size(900,900)
    grid_t = populateGrid(pedestrians)
    renderGrid(grid_t)
    cost_function = calculateCostFunction(grid_t)  
    frameRate(2)        



def populateGrid(pedestrians):
    grid_t = [['0' for c in range(cols)] for r in range(rows)] #set empty grid
    grid_t[targetX - 1][targetY - 1] = 'T' #insert Target in grid
    for p in pedestrians:
        grid_t[p[0] - 1][p[1] - 1] = 'P' #instert pedestrains in grid
   
    return grid_t


def renderGrid(grid_t):
    for c in range(cols):#cols=80
        for r in range(rows):#rows=80
            x = c * resolution
            y = r * resolution
            stroke('#000000')
            if grid_t[c][r] == '0':#white empty spaces
                fill('#ffffff')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'T':#green target
                fill('#00FF00')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'P':#blue pedestrians
                fill('#0000FF')
                rect(x, y, resolution - 1, resolution - 1)
    
                      
def calculateCostFunction(grid_t):
    cost_function = [[0 for c in range(cols)] for r in range(rows)] #cost function is a matrix of zeros (80x80)
    for c in range(cols):
        for r in range(rows):
            cost = sqrt(pow(c - targetX + 1, 2) + pow(r - targetY + 1, 2)) #calculate euclidian distance from point to traget
            cost = cost / sqrt(pow(rows, 2) + pow(cols, 2)) #normalizing
            cost_function[c][r] = cost
    return cost_function

                
##
#grid update
##                
def draw():
    global grid_t, cost_function
    background('#000000') 
    updated_pedestrians = updateTimeStep(pedestrians, grid_t)
    if(updated_pedestrians!='T'):
        grid_t = populateGrid(updated_pedestrians)
    renderGrid(grid_t)
       
         
def updateTimeStep(pedestrians, grid_t):
    for p in pedestrians: 
        p[0], p[1]  = findNextStep(p, pedestrians, grid_t)#new pedestrian position
        if p[0] == targetX and p[1] == targetY: 
            pedestrians.remove(p)
    return pedestrians

        
##
#checking neighbors
##     
def findNextStep(current_p,pedestrains, grid_t):
    next_x, next_y = current_p[0], current_p[1]  
    current_cost = cost_function[current_p[0] - 1][current_p[1] - 1] 
    #up
    if (current_p[0] - 1 > 0 and cost_function[current_p[0] - 2][current_p[1] - 1] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 2, current_p[1] - 1, rmax) < current_cost) and grid_t[current_p[0] - 2][current_p[1] - 1] != 'P' and cost_function[current_p[0] - 2][current_p[1] - 1]>0:
            next_x, next_y = current_p[0] - 1, current_p[1] 
            current_cost = cost_function[p[0] - 2][current_p[1] - 1] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 2, current_p[1] - 1, rmax)
    #down
    if (current_p[0] + 1 < cols and cost_function[current_p[0]][current_p[1] - 1] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0], current_p[1] - 1, rmax) < current_cost) and grid_t[current_p[0]][current_p[1] - 1] != 'P' and cost_function[current_p[0]][current_p[1] - 1]>0:
            next_x, next_y = current_p[0] + 1, current_p[1] 
            current_cost = cost_function[current_p[0]][current_p[1] - 1] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0], current_p[1] - 1, rmax)
    #left 
    if (current_p[1] - 1 > 0 and cost_function[current_p[0] - 1][current_p[1] - 2] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 1, current_p[1] - 2, rmax) < current_cost) and grid_t[current_p[0] - 1][current_p[1] - 2] != 'P' and cost_function[current_p[0] - 1][current_p[1] - 2]>0:
            next_x, next_y = current_p[0], current_p[1] - 1
            current_cost = cost_function[current_p[0] - 1][current_p[1] - 2] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 1, current_p[1] - 2, rmax)
   #right 
    if (current_p[1] + 1 < rows and cost_function[current_p[0] - 1][current_p[1]] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 1, current_p[1], rmax) < current_cost) and grid_t[current_p[0] - 1][current_p[1]] != 'P' and cost_function[current_p[0] - 1][current_p[1]]>0:
            next_x, next_y = current_p[0], current_p[1] + 1
            current_cost = cost_function[current_p[0] - 1][current_p[1]] + proximityToOtherPedestrians(current_p, pedestrians, current_p[0] - 1, current_p[1], rmax)
    return next_x, next_y
    

    
##
#interaction between two individuals
##                        
def proximityToOtherPedestrians(current_p, pedestrians, p_x, p_y, r_max):
    proximityFactor = 0
    for p in pedestrians: 
        if (p[0] != current_p[0] and p[1] != current_p[1]):
            r = pow(p[0] - p_x,2) + pow(p[1] - p_y,2) 
            if(r < pow(r_max, 2)):
                proximityFactor = proximityFactor + exp(pow(r - pow(r_max, 2), -1))
    return proximityFactor
