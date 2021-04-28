import json


def read_files(filename):
    
    """
    Reads the json scenario data file and returns the data read from it.

    :param : filename:
    :return: size of grid, positions of pedestrians, obstacles and targets, resolution of the grid
    
    """
    
    # Opening JSON file
    f = open(filename)

    # returns JSON object as
    # a dictionary
    data_scn = json.load(f)

    n = data_scn['scenario_details'][0]['N']
    
    pedestrians = (data_scn['scenario_details'][0]['pedestrians'])
    obstacles = (data_scn['scenario_details'][0]['obstacles'])
    target = (data_scn['scenario_details'][0]['target'])
    
    resolution = (data_scn['scenario_details'][0]['resolution'])

    # Closing file
    f.close()

    return n, pedestrians, obstacles, target, resolution
