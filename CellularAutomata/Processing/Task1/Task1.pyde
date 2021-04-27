from read_file import *
from render_grid import *

def setup():
    """
    Does the initial setup for the visualizaiton by creating the data matrix, rendering it once and setting the frame rate

    :param :
    :return: 
    
    """
    
    size(800,800)    
    n, pedestrians, obstacles, targets, resolution = read_files('scenario_1.json')
    grid_t = populateGrid(pedestrians, obstacles, n, n, targets[0], targets[1])
    renderGrid(grid_t, n, resolution)
    frameRate(2)        


def draw():
    """
    Plots the data matrix repeatedly to represent the scenario

    :param :
    :return: 
    
    """    
    n, pedestrians, obstacles, targets, resolution = read_files('scenario_1.json')
    grid_t = populateGrid(pedestrians, obstacles, n,n,targets[0], targets[1])
    renderGrid(grid_t, n, resolution)
