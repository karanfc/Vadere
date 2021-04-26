obstacles = []
targetX, targetY = 40, 40
cols, rows = 80, 80
resolution = 15
grid_t = []
cost_function = []
t = 0
rmax = 5
#pedestrians = []
pedestrians = [[10, 40], [16,22],[16, 58],[22, 64], [40, 70], [40, 10], [22, 16]]
time = 0

def setup():
    global grid_t, cost_function, targetX, targetY

    #pedestrians = generatePedestrians(cols, rows, 20)
    size(900,900)
    grid_t = populateGrid(pedestrians)
    renderGrid(grid_t)
    cost_function = calculateCostFunction()  
    frameRate(2)        

def generatePedestrians(cols, rows, N):
    global pedestrians
    for i in range(N):
        pedestrians.append([int(random(cols)), int(random(rows))])
    return pedestrians

def draw():
    global grid_t, cost_function
    background('#000000') 
    pedestrians = updateTimeStep()
    grid_t = populateGrid(pedestrians)
    renderGrid(grid_t)


def calculateCostFunction():
    cost_function = [[0 for c in range(cols)] for r in range(rows)]
    for c in range(cols):
        for r in range(rows):
            cost = sqrt(pow(c - targetX + 1, 2) + pow(r - targetY + 1, 2))
            cost = cost / sqrt(pow(rows, 2) + pow(cols, 2))
            cost_function[c][r] = cost  
    return cost_function

def renderCostFunction(cost_function):
     for c in range(cols):
        for r in range(rows):
            x = c * resolution
            y = r * resolution
            stroke('#000000')
            fill(cost_function[c][r] * 255)
            rect(x, y, resolution - 1, resolution - 1)   
    
def populateGrid(pedestrians):
    grid_t = [['0' for c in range(cols)] for r in range(rows)]
    grid_t[targetX - 1][targetY - 1] = 'T'
    for p in pedestrians:
        grid_t[p[0] - 1][p[1] - 1] = 'P'
    return grid_t

def renderGrid(grid_t):
    for c in range(cols):
        for r in range(rows):
            x = c * resolution
            y = r * resolution
            stroke('#000000')
            if grid_t[c][r] == '0':
                fill('#ffffff')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'T':
                fill('#E45FFF')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'P':
                fill('#E45634')
                rect(x, y, resolution - 1, resolution - 1)
                
            
def findNextStep(p):
    global pedestrians, grid_t
    next_x, next_y = p[0], p[1]  
    current_cost = cost_function[p[0] - 1][p[1] - 1] 
    
    if (p[0] - 1 > 0 and cost_function[p[0] - 2][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0] - 2, p[1] - 1) < current_cost) and grid_t[p[0] - 2][p[1] - 1] != 'P':
        next_x, next_y = p[0] - 1, p[1] 
        current_cost = cost_function[p[0] - 2][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0] - 2, p[1] - 1)
    
    if (p[0] + 1 < cols and cost_function[p[0]][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0], p[1] - 1) < current_cost) and grid_t[p[0]][p[1] - 1] != 'P':
        next_x, next_y = p[0] + 1, p[1] 
        current_cost = cost_function[p[0]][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0], p[1] - 1)
        
    if (p[1] - 1 > 0 and cost_function[p[0] - 1][p[1] - 2] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1] - 2) < current_cost) and grid_t[p[0] - 1][p[1] - 2] != 'P':
        next_x, next_y = p[0], p[1] - 1
        current_cost = cost_function[p[0] - 1][p[1] - 2] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1] - 2)
        
    if (p[1] + 1 < rows and cost_function[p[0] - 1][p[1]] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1]) < current_cost) and grid_t[p[0] - 1][p[1]] != 'P':
        next_x, next_y = p[0], p[1] + 1
        current_cost = cost_function[p[0] - 1][p[1]] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1])
    return next_x, next_y
    
def updateTimeStep():
    global pedestrians
    for p in pedestrians: 
        p[0], p[1]  = findNextStep(p)
        if p[0] == targetX and p[1] == targetY: 
            pedestrians.remove(p)
    return pedestrians
        
def proximityToOtherPedestrians(p, pedestrians, px, py):
    proximityFactor = 0
    global rmax
    for pd in pedestrians: 
        if (pd[0] != p[0] and pd[1] != p[1]):
            r2 = pow(pd[0] - px,2) + pow(pd[1] - py,2) 
            if(r2 < pow(rmax, 2)):
                proximityFactor = proximityFactor + exp(pow(r2 - pow(rmax, 2), -1))     
    return proximityFactor
