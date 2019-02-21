'''
* Team ID : 117
* Author List : Akshatha Nayak
* Filename : path_planning.py
* Theme : Antbot
* Functions : getLocations()
* Global Variables :
'''

from utils import AStarGraph
#from utils import Camera

graph = AStarGraph()

def queen(ids):
    for id in ids:
        if id[0]=='1':
            return id
    return 0

def getPath(ids):
    actions = []

    #go to each supply location in shrub region and scan it
    supply_locations = [(5,1), (3,1), (1,1), (9,1), (11,1), (13,1)] #coordinates of supply locations
    for sl in supply_locations:
        actions.append(sl)
        actions.append("SCAN SUPPLY")

    #go to central node and read all the ArUco markers
    actions.append((7,8)) #add the coordinates of central node
    actions.append("READ ARUCO")

    #Service queen anthill if it exists
    qid = queen(ids)
    if qid:
        #if QAH has trash service requirement
        if qid[7]:
            #if SR2 has supply requirement, SR1 has trash
            if qid[3:5] != '00':
                trash_loc = getLoc[qid[1:3]]['sr1']
            else:
                trash_loc = getLoc[qid[1:3]]['sr2']

            #go to the service region in QAH requiring trash service and pick trash
            actions.append(trash_loc)
            actions.append("PICK")

            #go to trash deposit zone and deposit trash
            actions.append((7,10))  #coordinates of Trash Deposit Zone
            actions.append("DEPOSIT")

        #if SR2 has service requirement
        if qid[3:5] != '00':
            s_locs = getSupply[qid[3:5]]
            d = 1000
            for s in s_locs:
                #find distance of supply locations from central node
                result, cost = AStarGraph.AStarSearch((7,8), s, graph)
                #find nearest supply location
                if cost < d:
                    d = cost
                    s_loc = s
            #go to nearest supply location and pick supply
            actions.append(s_loc)
            actions.append("PICK")
            getSupply[qid[3:5]].remove(s_loc)


    #service other anthills

    #return final list of actions to be done
    return actions

#get Aruco IDs in binary format
#ids = cam.IDs
ids = ['00100101','01011010','11101101','00000010'] #example
getSupply = {'01': [(3,1), (9,1)],  #red -> Honey Dew
             '10': [(5,1)],         #green -> Leaves
             '11': [(1,1), (11,1)]} #blue -> Wood
getLoc = {  '00': {'sr1': (1,11),  'sr2': (3,11)},
            '01': {'sr1': (11,11), 'sr2': (13,11)},
            '10': {'sr1': (13,5),  'sr2': (11,5)},
            '11': {'sr1': (3,5),   'sr2': (1,5)}}

src = (7,1) #initialize with start node location
current_direction = "U"	#directed upwards on the grid

actions = getPath(ids)
#actions = [(7,8), (3,1), (3,5)]   #sample locations list

#get directions for visiting all locations in the list
'''
for loc in actions:
    dest = loc
    result, cost = AStarGraph.AStarSearch(src, dest, graph)
    current_direction, directions, moves = AStarGraph.get_directions(result, current_direction, graph)
    print ("Route: ", result)
    print ("Cost: ", cost)
    print("Directions: ", directions)
    print("Moves: ", moves)
    print("Currently facing: ", current_direction)
    src = loc
'''
print(actions)
