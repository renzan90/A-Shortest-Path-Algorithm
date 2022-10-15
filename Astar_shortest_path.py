import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image
from commandline import get_coordinates
from get_map import get_map
import os
import time


class Node:
    def __init__(self, y, x):
        self._y = y
        self._x = x

        self._binaryvalue = map[y][x]
        
        self._g = 0
        self._h = 0
        self._f = self._g + self._h

        self._cords = (x, y)

def initialize_nodes(origin, goal, map):
    startnode_y, startnode_x = origin
    endnode_y, endnode_x = goal

    start_node = Node(startnode_y, startnode_x)
    goal_node = Node(endnode_y, endnode_x)

    start_node._value = map[startnode_y][startnode_x]
    goal_node._value = map[endnode_y][endnode_x] 

    current_node = Node(startnode_y, startnode_x)

    return start_node, goal_node, current_node

def eight_neighbours(current_node, map):

    
    if current_node._y != map.shape[0]:
        sw_node = Node(current_node._y-1, current_node._x-1)
        s_node = Node(current_node._y-1, current_node._x)
        se_node = Node(current_node._y-1, current_node._x+1)
        
    else:
        sw_node = None
        s_node = None
        se_node = None

    if current_node._y != 0:
        nw_node = Node(current_node._y+1, current_node._x-1)
        n_node = Node(current_node._y+1, current_node._x)
        ne_node = Node(current_node._y+1, current_node._x+1)

    else:
        nw_node = None
        n_node = None
        ne_node = None

    if current_node._x != 0:
        w_node = Node(current_node._y, current_node._x-1)
    else:
        w_node = None
    
    if current_node._x != map.shape[1]:
        e_node = Node(current_node._y, current_node._x+1)
    else:
        e_node = None

    neighbours = [w_node, e_node, nw_node, n_node, ne_node, sw_node, s_node, se_node]

    return neighbours


#This function calculates the 'f' value of neighbouring nodes, selects the lowest and then per-
#-forms calculations to check if:
# 1.- There are multiple nodes with the same f value. Therefore we try to collect all nodes in the visited/open
#       list with the same f value from lines 81 to 103
# 
# 2. -Lines 108 to 120 concern with searching for the lower Heuristic value in case if we find multiple nodes
#        with the same f value

def calculate_values(current_node, goal_node, path, visited):

    storeall_fvalues = []


    for neighbour_node in visited:
        neighbour_node._g = current_node._g + 1
        neighbour_node._h = ((neighbour_node._x - goal_node._x)**2) + ((neighbour_node._y - goal_node._y)**2)
        neighbour_node._f = neighbour_node._g + neighbour_node._h
        storeall_fvalues.append(neighbour_node._f)


    
    minimumfnodes = [visited[index] for index, val in enumerate(storeall_fvalues) if val == min(storeall_fvalues)]
    
    if len(minimumfnodes) > 1:
        minh_nodes = []
        for node in minimumfnodes:
            minh_nodes.append(node._h)
            if node._h == min(minh_nodes):
                chosen_node = node
            
           
    else:
        chosen_node = minimumfnodes[-1]

 
    remaining_nodes =  [visited[index] for index, old_node in enumerate(visited) if old_node._f < chosen_node._f and old_node not in path]

    if remaining_nodes:
        smallestf_value = min([old_node._f for old_node in remaining_nodes])
        smallestf_nodes = [node for node in remaining_nodes if node._f == smallestf_value]

        if len(smallestf_nodes) > 1:
            smallesth_value = min([old_node._h for old_node in smallestf_nodes])
            chosen_node = smallesth_value
        else:
            chosen_node = smallestf_nodes[0]

    return chosen_node



def search(origin, goal, coordinates, map):

    visited = []
    path = []

    start_node, goal_node, current_node = initialize_nodes(origin, goal, map)  

    current_node._g = current_node._h = current_node._f = 0

    visited.append(current_node)


    while not current_node._cords == goal_node._cords:

        print("new current_node", current_node._x, current_node._y)
        calculated_node_neighbours = eight_neighbours(current_node, map)

        valid_node_neighbours = [nodes for nodes in calculated_node_neighbours if nodes._binaryvalue == 1]

        
        for node in valid_node_neighbours:
            for pathnode in path:
                if node._cords == pathnode._cords:
                    if node in valid_node_neighbours:
                        valid_node_neighbours.remove(node)
                    else:
                        continue
                else:
                    continue   
              
        
        for valid_neighbour in valid_node_neighbours:
            for pathnode in path:
                if valid_neighbour._cords == pathnode._cords:
                    if valid_neighbour in valid_node_neighbours:
                        valid_node_neighbours.remove(valid_neighbour)


        visited = visited + valid_node_neighbours


        path.append(current_node)

        visited.remove(current_node)

        current_node = calculate_values(current_node, goal_node, path, visited)
        
        print(current_node._cords, goal_node._cords)

        path_values =[]
        for pathnode in path:
            path_values.append(pathnode._binaryvalue)

        path_cords = []
        for pathcord in path:
            np.array(path_cords)
            path_cords.append(pathcord._cords)


    return path_values, path_cords
    


def result_output(path_cords, pathvalues, image):

    path_cords_numpy = np.array(path_cords)
    
    pathfile = "path.txt"
    with open(pathfile, 'w') as f:
        f.write(str(pathvalues))


    plt_image = plt.imread(image)

    #xpoints, ypoints = np.array([500, 200]), np.array([200, 300])
    
    #x, y =path_cords_numpy.T
    plt.plot(*zip(*path_cords), color="red", linewidth=2)
    plt.axis('off')

    plt.imshow(plt_image)
    plt.show()






if __name__ == '__main__':

    start_time = time.time()
    
    coordinates, map, image = get_map('station_threshold.jpg')


    origin, goal = get_coordinates(coordinates, map)


    pathvalues, final_path = search(origin, goal, coordinates, map)

    result_output(final_path, pathvalues, image)

    time_taken = start_time - time.time()
    print(time_taken)