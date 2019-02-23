'''
* Team ID : 117
* Author List : Akshatha Nayak
* Filename : path_planning.py
* Theme : Antbot
* Functions : getLocations()
* Global Variables :
'''

from utils import AStarGraph

graph = AStarGraph()
src = (7,3) #initialize location
current_direction = "U"	#directed upwards on the grid

getLoc = {  '00': {'sr1': (1,11),  'sr2': (3,11), 'ah': (2,11)},
            '01': {'sr1': (11,11), 'sr2': (13,11), 'ah': (12,11)},
            '10': {'sr1': (13,5),  'sr2': (11,5), 'ah': (12,5)},
            '11': {'sr1': (3,5),   'sr2': (1,5), 'ah': (2,5)} }
getDir = {  '0': {'sr1': "L",  'sr2': "R", 'ah': "U"},
            '1': {'sr1': "R",   'sr2': "L", 'ah': "D"} }

def queen(ids):
    for id in ids:
        if id[0]=='1':
            return id
    return 0

def getMovesTo(dest, final_direction):
    global src, current_direction
    result, cost = AStarGraph.AStarSearch(src, dest, graph)
    current_direction, directions, moves = AStarGraph.get_directions(result, current_direction, final_direction, graph)
    current_direction = final_direction
    src = dest
    return directions

def service(ids, getSupply):
    path_actions = []
    #Service queen anthill if it exists
    qid = queen(ids)
    if qid:
        #process trash service requirements
        trash_service(qid, path_actions)
        #process SR2 for supply requirements
        supply_service(qid, qid[3:5], 'sr2', getSupply, path_actions)
        #process SR1 for supply requirements
        supply_service(qid, qid[5:7], 'sr1', getSupply, path_actions)

    #service other anthills
    for id in ids:
        if id != qid:
            #process trash service requirements
            trash_service(id, path_actions)
            #process SR2 for supply requirements
            supply_service(id, id[3:5], 'sr2', getSupply, path_actions)
            #process SR1 for supply requirements
            supply_service(id, id[5:7], 'sr1', getSupply, path_actions)

    #return to start position and turn on buzzer
    path_actions += getMovesTo((7,1), "D")
    path_actions.append("BUZZER")
    return path_actions

def supply_service(id, sr, sr_num, getSupply, path_actions):
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
        path_actions += getMovesTo(s_loc, "D")
        path_actions.append("PICK SUPPLY")
        getSupply[sr].remove(s_loc)

        #deposit supply in the required service region
        dir = getDir[id[1]][sr_num]
        path_actions += getMovesTo(getLoc[id[1:3]]['ah'], dir)
        path_actions.append("DEPOSIT SUPPLY")

def trash_service(id, path_actions):
    global current_direction
    #if AH has trash service requirement
    if id[7] != '0':
        ah_loc = getLoc[id[1:3]]['ah']
        dir = getDir[id[1]]['ah']
        path_actions += getMovesTo(ah_loc, dir) #now facing the wall
        #perform trash pick up routine
        path_actions.append("SCAN & PICK TRASH")
        if dir=="U":
            current_direction = "D"
        else:
            current_direction = "U"
        #now facing the anthill exit
        #go to trash deposit zone and deposit trash
        path_actions += getMovesTo((7,10), "U")  #coordinates of Trash Deposit Zone
        path_actions.append("DEPOSIT TRASH")

###########################DELETE THIS###############################
#####################SAMPLE CONFIGURATION###################
ids = ['00100001','01011010','11101001','00000100'] #example
getSupply = {'01': [(3,3), (9,3)],  #red -> Honey Dew
             '10': [(5,3)],         #green -> Leaves
             '11': [(1,3), (11,3)]} #blue -> Wood
#############################################################

#scan all supplies in the shrub region
path_actions = []
#go to each supply location in left shrub region and scan it (camera on left, so no turns)
path_actions = ["F", "L", "F", "SCAN", "F", "SCAN", "F", "SCAN"]
#turn around and go to the right end of shrub region
path_actions = path_actions + ["B"] + ["F"]*6
#turn and scan supplies in shrub region from right to left
path_actions += ["B", "SCAN", "F", "SCAN", "F", "SCAN", "F"]
#turn right (current pos -> (7,3))
path_actions += ["R"]

#go to central node (7,8) and read all the ArUco markers
path_actions += getMovesTo((7,8),"U") #add the coordinates of central node
path_actions.append("READ ARUCO")

#do all servicing, return to start, buzzer on
print(service(ids, getSupply))
