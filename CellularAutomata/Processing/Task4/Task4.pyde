obstacles = []
targetX, targetY = 10, 10
cols, rows = 10, 10
resolution = 50
grid_t = []
cost_function = []
rmax = 1.2
pedestrians = []
#pedestrians = [[10, 40], [16,22],[16, 58],[22, 64], [40, 70], [40, 10], [22, 16]]
obstacles = [[5, 1], [5,2], [5,3], [5,4],[5,6],[5,7],[5,8],[5,9],[5,10]]
time = 0
dijkstra_cost_function = []
INFINITY = 100;

def setup():
    print 'Start'
    global grid_t, cost_function, targetX, targetY, obstacles
    #obstacles = generateObstacles(cols, rows, 20)
    #print obstacles
    frameRate(2)
    pedestrians = generatePedestrians(4, rows, 5)
    size(900,900)
    grid_t = populateGrid(pedestrians, obstacles)
    #renderGrid(grid_t)
    cost_function = calculateCostFunction()
    dijkstra_cost_function = createDijkstraCostFunction()
    dijkstra_cost_function = [[x/(sqrt(pow(rows,2)+pow(cols,2))) for x in lst] for lst in dijkstra_cost_function]
    #print dijkstra_cost_function
    #renderCostFunction(dijkstra_cost_function)
    delay(3000)      

def generateObstacles(cols, rows, N):
    global obstacles
    for i in range(N):
        obstacles.append([int(random(cols)), int(random(rows))])
    return obstacles

def generatePedestrians(cols, rows, N):
    global pedestrians
    for i in range(N):
        pedestrians.append([int(random(cols)), int(random(rows))])
    return pedestrians

def draw():
    global grid_t, cost_function, obstacles
    background('#000000') 
    pedestrians = updateTimeStep()
    grid_t = populateGrid(pedestrians, obstacles)
    renderGrid(grid_t)


def calculateCostFunction():
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

def renderCostFunction(cost_function):
    global grid_t
    for c in range(cols):
        for r in range(rows):
                x = c * resolution
                y = r * resolution
                stroke('#000000')
                fill(cost_function[c][r] * 255)
                rect(x, y, resolution - 1, resolution - 1)   
                
    
def populateGrid(pedestrians, obstacles):
    grid_t = [['0' for c in range(cols)] for r in range(rows)]
    grid_t[targetX - 1][targetY - 1] = 'T'
    for p in pedestrians:
        grid_t[p[0] - 1][p[1] - 1] = 'P'
    for o in obstacles:
        grid_t[o[0] - 1][o[1] - 1] = 'O'
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
                fill('#00FF00')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'P':
                fill('#0000FF')
                rect(x, y, resolution - 1, resolution - 1)
                
            elif grid_t[c][r] == 'O':
                fill('#FF0000')
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

def findNextStepDijkstra(p):
    global pedestrians, grid_t, dijkstra_cost_function
    next_x, next_y = p[0], p[1]  
    current_cost = dijkstra_cost_function[p[0] - 1][p[1] - 1] 
    
    if (p[0] - 1 > 0 and dijkstra_cost_function[p[0] - 2][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0] - 2, p[1] - 1) < current_cost) and grid_t[p[0] - 2][p[1] - 1] != 'P':
        next_x, next_y = p[0] - 1, p[1] 
        current_cost = dijkstra_cost_function[p[0] - 2][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0] - 2, p[1] - 1)
    
    if (p[0] + 1 < cols and dijkstra_cost_function[p[0]][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0], p[1] - 1) < current_cost) and grid_t[p[0]][p[1] - 1] != 'P':
        next_x, next_y = p[0] + 1, p[1] 
        current_cost = dijkstra_cost_function[p[0]][p[1] - 1] + proximityToOtherPedestrians(p, pedestrians, p[0], p[1] - 1)
        
    if (p[1] - 1 > 0 and dijkstra_cost_function[p[0] - 1][p[1] - 2] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1] - 2) < current_cost) and grid_t[p[0] - 1][p[1] - 2] != 'P':
        next_x, next_y = p[0], p[1] - 1
        current_cost = dijkstra_cost_function[p[0] - 1][p[1] - 2] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1] - 2)
        
    if (p[1] + 1 < rows and dijkstra_cost_function[p[0] - 1][p[1]] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1]) < current_cost) and grid_t[p[0] - 1][p[1]] != 'P':
        next_x, next_y = p[0], p[1] + 1
        current_cost = dijkstra_cost_function[p[0] - 1][p[1]] + proximityToOtherPedestrians(p, pedestrians, p[0] - 1, p[1])
        
    return next_x, next_y
    
def updateTimeStep():
    global pedestrians
    for p in pedestrians: 
        p[0], p[1]  = findNextStepDijkstra(p)
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

def createDijkstraCostFunction():
    global grid_t, INFINITY, dijkstra_cost_function, rows, cols, targetX, targetY
    dijkstra_cost_function = [[INFINITY for c in range(cols)] for r in range(rows)]
    dijkstra_cost_function[targetX - 1][targetY - 1] = 0
    visited = set()
    while True: 
        node = getSmallestDistanceNode(visited)
        if node == None:
            break
        visited.add(node)
        nodeX, nodeY = node
        node_neighbours = getAllNeighbours(node)
        
        for neighbour in node_neighbours:
            neighbourX, neighbourY = neighbour
            new_distance = (dijkstra_cost_function[nodeX][nodeY] + sqrt(pow(nodeX - neighbourX, 2) + pow(nodeY - neighbourY, 2))) 
            if new_distance < dijkstra_cost_function[neighbourX][neighbourY]:
                dijkstra_cost_function[neighbourX][neighbourY] = new_distance 
    
    return dijkstra_cost_function

def getSmallestDistanceNode(visited):
    global grid_t, rows, cols, dijkstra_cost_function
    current_selected_node = None
    current_min_distance = INFINITY
    for c in range(cols):
        for r in range(rows):
            if dijkstra_cost_function[c][r] < current_min_distance and (c, r) not in visited:
                current_selected_node = (c, r)
                current_min_distance = dijkstra_cost_function[c][r]        
    return current_selected_node

def getAllNeighbours(node):
    global grid_t, rows, cols
    print node
    neighbours = []
      
    if (node[0] - 1 >= 0 and grid_t[node[0] - 1][node[1]] != 'O'):
        neighbours.append([node[0] - 1, node[1]])
    
    if (node[0] + 1 < cols and grid_t[node[0] + 1][node[1]] != 'O'):
        neighbours.append([node[0] + 1, node[1]])

    if (node[1] - 1 >= 0 and grid_t[node[0]][node[1] - 1] != 'O'):
        neighbours.append([node[0], node[1] - 1])
    
    if (node[1] + 1 < rows and grid_t[node[0]][node[1] + 1] != 'O'):
        neighbours.append([node[0], node[1] + 1])
    print neighbours
    return neighbours
