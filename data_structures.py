'''
* Team ID : 117
* Author List : Akshatha Nayak
* Filename : data_structures.py
* Theme : Antbot
* Functions : multidict(*args), getAH(bits), getSupply(bits)
* Global Variables : ids -> list of binary values of ArUco IDs
                     rah_dict -> multilevel dictionary for storing requirements of regular anthills
                     qah_dict -> multilevel dictionary for storing requirements of queen anthill
                     trash_rah_dict -> dictionary for storing regular anthill trash service requirements
                     trash_qah -> trash service requirements of queen anthill
'''
from utils import Camera

def multidict(*args):
    if len(args) > 1:
        return {arg:multidict(*args[1:]) for arg in args[0]}
    else:
        return args[0]

def getAH(s):
    return 'ah'+ str(int(s, 2))

def getSupply(s):
    #No Supply ->  00
    if s=='00':
        return 0
    #HoneyDew -> Red   ->  01
    if s=='01':
        return 'red'
    #Leaves   -> Green ->  10
    if s=='10':
        return 'green'
    #Wood     -> Blue  ->  11
    if s=='11':
        return 'blue'

#get Aruco IDs in binary format
#ids = cam.IDs
ids = ['00100101','01011010','11101101','00000010'] #example
qah_dict = multidict(['red', 'blue', 'green'], ['count', 'service_regions'], 0)
rah_dict = multidict(['red', 'blue', 'green'], ['total','ah0', 'ah1', 'ah2', 'ah3'], ['count', 'service_regions'], 0)
trash_rah_dict = {}
trash_qah = 0

for id in ids:
    #Queen Anthill
    if id[0]=='1':
        qah_num = getAH(id[1:3])
        #store service region 2 requirements
        if getSupply(id[3:5]):
            qah_dict[getSupply(id[3:5])]['count'] += 1
            qah_dict[getSupply(id[3:5])]['service_regions'] = [2]

        #store service region 1 requirements
        if getSupply(id[5:7]):
            qah_dict[getSupply(id[5:7])]['count'] += 1
            if qah_dict[getSupply(id[5:7])]['service_regions']:
                qah_dict[getSupply(id[5:7])]['service_regions'].append(1)
            else:
                qah_dict[getSupply(id[5:7])]['service_regions'] = [1]

        #store trash service requirement
        trash_qah = id[7]

    #Regular anthills
    else:
        ah_num = getAH(id[1:3])
        #store service region 2 requirements
        if getSupply(id[3:5]):
            rah_dict[getSupply(id[3:5])]['total']['count'] += 1
            rah_dict[getSupply(id[3:5])][ah_num]['count'] += 1
            rah_dict[getSupply(id[3:5])][ah_num]['service_regions'] = [2]

        #store service region 1 requirements
        if getSupply(id[5:7]):
            rah_dict[getSupply(id[5:7])]['total']['count'] += 1
            rah_dict[getSupply(id[5:7])][ah_num]['count'] += 1
            if rah_dict[getSupply(id[5:7])][ah_num]['service_regions']:
                rah_dict[getSupply(id[5:7])][ah_num]['service_regions'].append(1)
            else:
                rah_dict[getSupply(id[5:7])][ah_num]['service_regions'] = [1]

        #store trash service requirements of regual ranthills
        trash_rah_dict[getAH(id[1:3])] = id[7]

print(qah_dict)
print(rah_dict)
print(trash_rah_dict)
print(trash_qah)
