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
src = (7,3) #initialize location
current_direction = "U"	#directed upwards on the grid

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

def service(id, sr, sr_num):
    global getSupply, path_actions
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

def trash_service(id):
    global trash_locations, path_actions, current_direction
    #if AH has trash service requirement
    if id[7] != '0':
        ah_loc = getLoc[id[1:3]]['ah']
        dir = getDir[id[1]]['ah']
        path_actions += getMovesTo(ah_loc, dir)
        #Case#1: (trash, supply) -> if SR2 has supply requirement, SR1 has trash
        if id[3:5] != '00':
            dir = getDir[id[1]]['sr1']
            trash_loc = getLoc[id[1:3]]['sr1']
        #if SR2 has no supply requirement
        else:
            #Case#2: (supply, trash) -> if SR1 has supply requirement, SR2 has trash
            if id[5:7] != '00':
                dir = getDir[id[1]]['sr2']
                trash_loc = getLoc[id[1:3]]['sr2']
            #Case#3 & #4 (no service, trash) & (trash, no service)
            else:
                #scan for trash on left (sr1)
                path_actions.append("SCAN TRASH")
                #if trash found in SR1
                if getLoc[id[1:3]]['sr1'] in trash_locations:
                    dir = getDir[id[1]]['sr1']
                    trash_loc = getLoc[id[1:3]]['sr1']
                #if trash not found in SR1, it is in SR2
                else:
                    dir = getDir[id[1]]['sr2']
                    trash_loc = getLoc[id[1:3]]['sr2']

        #go to the service region in AH requiring trash service and pick trash
        path_actions += getMovesTo(ah_loc, dir)
        path_actions.append("PICK TRASH")
        trash_locations.remove(trash_loc)

        #go to trash deposit zone and deposit trash
        path_actions += getMovesTo((7,10), "U")  #coordinates of Trash Deposit Zone
        path_actions.append("DEPOSIT TRASH")

#get Aruco IDs in binary format
#ids = cam.IDs
getLoc = {  '00': {'sr1': (1,11),  'sr2': (3,11), 'ah': (2,11)},
            '01': {'sr1': (11,11), 'sr2': (13,11), 'ah': (12,11)},
            '10': {'sr1': (13,5),  'sr2': (11,5), 'ah': (12,5)},
            '11': {'sr1': (3,5),   'sr2': (1,5), 'ah': (2,5)} }
getDir = {  '0': {'sr1': "L",  'sr2': "R", 'ah': "U"},
            '1': {'sr1': "R",   'sr2': "L", 'ah': "D"} }

#####################SAMPLE CONFIGURATION###################
ids = ['00100001','01011010','11101001','00000100'] #example
getSupply = {'01': [(3,3), (9,3)],  #red -> Honey Dew
             '10': [(5,3)],         #green -> Leaves
             '11': [(1,3), (11,3)]} #blue -> Wood
trash_locations = [(13,11), (3,5)]
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

#Service queen anthill if it exists
qid = queen(ids)
if qid:
    #process trash service requirements
    trash_service(qid)
    #process SR2 for supply requirements
    service(qid, qid[3:5], 'sr2')
    #process SR1 for supply requirements
    service(qid, qid[5:7], 'sr1')

#service other anthills
for id in ids:
    if id != qid:
        #process trash service requirements
        trash_service(id)
        #process SR2 for supply requirements
        service(id, id[3:5], 'sr2')
        #process SR1 for supply requirements
        service(id, id[5:7], 'sr1')

#return to start position
path_actions += getMovesTo((7,1), "D")
path_actions.append("BUZZER")

#display actions
for i in path_actions:
    print(i, end=", ")
    if len(i)>1:
        print("")
