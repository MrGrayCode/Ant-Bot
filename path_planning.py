from utils import AStarGraph
from data_structures import *

graph = AStarGraph()
src = (7,1) #initialize with start node location
current_direction = "U"	#directed upwards on the grid

#locations = getLocations()
locations = [(7,8), (3,1), (3,5)]   #sample locations list

#get directions for visiting all locations in the list
for loc in locations:
    dest = loc
    result, cost = AStarGraph.AStarSearch(src, dest, graph)
    current_direction, directions, moves = AStarGraph.get_directions(result, current_direction, graph)
    print ("Route: ", result)
    print ("Cost: ", cost)
    print("Directions: ", directions)
    print("Moves: ", moves)
    print("Currently facing: ", current_direction)
    src = loc
