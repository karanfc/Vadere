

""
"Function to populate the data for the simulation"
""
def populateGrid(pedestrians, obstacles, rows, cols, targetX, targetY):
    
    """
    Takes in data about the scenario and creates a grid matrix that contains the data representing the scenario.

    :param: lists of positions of pedestrians, obstacle and the target, number of rows and columns of the grid:
    :return: the data matrix representing the scenario
    
    """
    
    
    grid_t = [['0' for c in range(cols)] for r in range(rows)]
    
    #represent the target, pedestrian and obstacle positions by T, P and Q respectively
    
    grid_t[targetX - 1][targetY - 1] = 'T'
    for p in pedestrians:
        print("p is", p)
        grid_t[p[0] - 1][p[1] - 1] = 'P'
    for o in obstacles:
        grid_t[o[0] - 1][o[1] - 1] = 'O'
    return grid_t



def renderGrid(grid_t, n, resolution):
    
    """
    Takes in the data matrix and displays the scenario.

    :param: the data matrix representing the scenario, the dimension, resolution of the grid 
    :return:
    
    """
    
    rows = cols = n
    for c in range(cols):
        for r in range(rows):
            x = c * resolution
            y = r * resolution
            stroke('#000000')
            
            #blank cell is white
            
            if grid_t[c][r] == '0':
                fill('#ffffff')
                rect(x, y, resolution - 1, resolution - 1)

            #target cell is green
            
            elif grid_t[c][r] == 'T':
                fill('#00FF00')
                rect(x, y, resolution - 1, resolution - 1)

            #pedestrian cell is blue
            
            elif grid_t[c][r] == 'P':
                fill('#0000FF')
                rect(x, y, resolution - 1, resolution - 1)

            #pedestrian cell is red
            
            elif grid_t[c][r] == 'O':
                fill('#FF0000')
                rect(x, y, resolution - 1, resolution - 1)
