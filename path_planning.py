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

def service(id, sr, getSupply, actions):
    if sr != '00':
        s_locs = getSupply[sr]
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
        actions.append("PICK SUPPLY")
        getSupply[sr].remove(s_loc)

        #deposit supply in the required service region
        actions.append(getLoc[id[1:3]]['sr2'])
        actions.append("DEPOSIT SUPPLY")

def trash_service(id, trash_locations, actions):
    #if AH has trash service requirement
    if id[7] != '0':
        #Case#1: (trash, supply) -> if SR2 has supply requirement, SR1 has trash
        if id[3:5] != '00':
            trash_loc = getLoc[id[1:3]]['sr1']
        #if SR2 has no supply requirement
        else:
            #Case#2: (supply, trash) -> if SR1 has supply requirement, SR2 has trash
            if id[5:7] != '00':
                trash_loc = getLoc[id[1:3]]['sr2']
            #Case#3 & #4 (no service, trash) & (trash, no service)
            else:
                #go to sr1 and scan for trash
                actions.append(getLoc[id[1:3]]['sr1'])
                actions.append("SCAN TRASH")
                #if trash found in SR1
                if getLoc[id[1:3]]['sr1'] in trash_locations:
                    trash_loc = getLoc[id[1:3]]['sr1']
                #if trash not found in SR1, it is in SR2
                else:
                    trash_loc = getLoc[id[1:3]]['sr2']

        #go to the service region in AH requiring trash service and pick trash
        actions.append(trash_loc)
        actions.append("PICK TRASH")
        trash_locations.remove(trash_loc)

        #go to trash deposit zone and deposit trash
        actions.append((7,10))  #coordinates of Trash Deposit Zone
        actions.append("DEPOSIT TRASH")

def getPath(ids, getSupply):
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
        #process trash service requirements
        trash_service(qid, trash_locations, actions)
        #process SR2 for supply requirements
        service(qid, qid[3:5], getSupply, actions)
        #process SR1 for supply requirements
        service(qid, qid[5:7], getSupply, actions)

    #service other anthills
    for id in ids:
        if id != qid:
            #process trash service requirements
            trash_service(id, trash_locations, actions)
            #process SR2 for supply requirements
            service(id, id[3:5], getSupply, actions)
            #process SR1 for supply requirements
            service(id, id[5:7], getSupply, actions)

    #return final list of actions to be done
    return actions

#get Aruco IDs in binary format
#ids = cam.IDs
ids = ['00100001','01011010','11101001','00000100'] #example
getSupply = {'01': [(3,1), (9,1)],  #red -> Honey Dew
             '10': [(5,1)],         #green -> Leaves
             '11': [(1,1), (11,1)]} #blue -> Wood
getLoc = {  '00': {'sr1': (1,11),  'sr2': (3,11)},
            '01': {'sr1': (11,11), 'sr2': (13,11)},
            '10': {'sr1': (13,5),  'sr2': (11,5)},
            '11': {'sr1': (3,5),   'sr2': (1,5)}}
trash_locations = [(13,11), (3,5)]

src = (7,1) #initialize with start node location
current_direction = "U"	#directed upwards on the grid
actions = getPath(ids, getSupply)

'''
for i in range(0, len(actions)-1, 2):
    print(actions[i], actions[i+1])
'''

#get directions for visiting all locations in the list
path_actions = []
for act in actions:
    if len(act)==2: #check for coordinates
        dest = act
        result, cost = AStarGraph.AStarSearch(src, dest, graph)
        current_direction, directions, moves = AStarGraph.get_directions(result, current_direction, graph)
        '''
        print ("Route: ", result)
        print ("Cost: ", cost)
        print("Directions: ", directions)
        print("Moves: ", moves)
        print("Currently facing: ", current_direction)
        '''
        path_actions += directions
        src = act
    else:
        path_actions.append(act)

for i in path_actions:
    print(i, end=", ")
    if len(i)>1:
        print("")
