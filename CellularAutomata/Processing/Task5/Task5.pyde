obstacles = []
targetX, targetY = 50, 10 
cols, rows = 50, 50
resolution = 15
grid_t = []
cost_function = []
rmax = 1.2
pedestrians = []
obstacles = []
time = 0
dijkstra_cost_function = []
INFINITY = 10000
density = 0.85
A_x, A_y = 20,10
B_x, B_y = 30,10
C_x, C_y = 30,9
countA = countB = countC = 0

def setup():
    global grid_t, cost_function, targetX, targetY, obstacles
    frameRate(2)
    size(900,900)

    setUpTest1()
    setUpTest4()
    setUpTest6()
    setUpTest7()
    
    grid_t = populateGrid(pedestrians, obstacles)
    cost_function = calculateCostFunction()
    dijkstra_cost_function = createDijkstraCostFunction()
    dijkstra_cost_function = [[x/(sqrt(pow(rows,2)+pow(cols,2))) for x in lst] for lst in dijkstra_cost_function]
    #renderCostFunction(dijkstra_cost_function)
    print grid_t
    renderGrid(grid_t)

def setUpTest1():
    global pedestrians, obstacles
    startX, startY = 1, 6
    N = 10
    pedestrians = [[1, 10]]
    obstacles = generateObstacles()

def setUpTest4():
    global pedestrians, obstacles
    startX, startY = 1, 6
    N = 10
    pedestrians = generatePedestrians(startX, startY, N)
    obstacles = generateObstacles()


def setUpTest6():
    global pedestrians, obstacles
    pedestrians = [[3,12],[5,12],[7,12],[9,12],[1,14],[3,14],[5,14],[7,14],[2,16],[4,16],[6,16],[8,16],[10,16]]
    obstacles = [[10,1],[10,1],[10,2],[10,3],[10,4],[10,5],[10,6],[10,7],[10,8],[10,9],[10,10],[1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],[10,10]]
    
def generateObstacles():
    global obstacles
    for i in range(50):
        obstacles.append([i,5])
        obstacles.append([i,15])
    return obstacles

def generatePedestrians(startX, startY, SpawnSize):
    global pedestrians, density
    numOfPedestrians = density * pow(SpawnSize, 2)
    print ('total = +', numOfPedestrians)
    for p in range(int(numOfPedestrians)):
            pedestrians.append([int(random(startX, startX + SpawnSize)), int(random(startY, startY + SpawnSize))])
    return pedestrians

def draw():
    
    global grid_t, cost_function, obstacles, time
    background('#000000') 
    pedestrians = updateTimeStep()
    grid_t = populateGrid(pedestrians, obstacles)
    renderGrid(grid_t)
    time+=1
    if time > 60:
        print countA, countB, countC
        noLoop()


def performTest1():
    obstacles = generateObstacles(cols, rows, 400)
    pedestrians = generatePedestrians(cols, rows, 20)

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
    global A_x, A_y, B_x, B_y, C_x, C_y
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
            '''    
            if (c == A_x and r == A_y) or (c == B_x and r == B_y) or (c == C_x and r == C_y):
                fill('#FFFF00')
                rect(x, y, resolution - 1, resolution - 1)
            '''    
            
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
    global pedestrians, countA, countB, countC
    for p in pedestrians: 
        p[0], p[1]  = findNextStepDijkstra(p)
        
        if p[0] == A_x and p[1] == A_y: 
            countA+=1
        
        elif p[0] == B_x and p[1] == B_y: 
            countB+=1
            
        elif p[0] == C_x and p[1] == C_y: 
            countC+=1
            
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
    neighbours = []
      
    if (node[0] - 1 >= 0 and grid_t[node[0] - 1][node[1]] != 'O'):
        neighbours.append([node[0] - 1, node[1]])
    
    if (node[0] + 1 < cols and grid_t[node[0] + 1][node[1]] != 'O'):
        neighbours.append([node[0] + 1, node[1]])

    if (node[1] - 1 >= 0 and grid_t[node[0]][node[1] - 1] != 'O'):
        neighbours.append([node[0], node[1] - 1])
    
    if (node[1] + 1 < rows and grid_t[node[0]][node[1] + 1] != 'O'):
        neighbours.append([node[0], node[1] + 1])
    return neighbours
