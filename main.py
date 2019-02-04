'''
* Team ID : 117
* Author List : Ebey Abraham
* Filename : main.py
* Theme : Antbot
* Functions : 
* Global Variables : ser -> Object for serial communication
                     count -> stores the number of nodes detected
                     ch -> stores the string received from the arduino serial port
'''
from utils import Bot
from utils import Camera
from threading import Thread
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)
count = 0
ch = ''
bot = Bot()

#move the bot forward till it reaches the second node (the central node)
while count < 2:
    ch = str(ser.readline())
    ch = ch[2]
    #print(ch)
    if ch == '1':
        #case 1: turn coarse right
        bot.forward(40,25)
    elif ch == '2':
        #case 2: turn soft right
        bot.forward(40,30)
    elif ch == '3':
        #case 1: move straight
        bot.forward()
    elif ch == '4':
        #case 4: turn coarse left
        bot.forward(25,40)
    elif ch == '5':
        #case 5: turn soft left
        bot.forward(30,40)
    elif ch == '6':
        #case 6: bot has reached a node
        #print("[NODE]")
        count += 1

#intialise the Camera object
cam = Camera()

#to identify the aruco markers from the central node
#we move the robot in the clockwise direction and detect the aruco markers using the getArucoID function
#we use two separate threads and run them simultaneously 

t1 = Thread(target=cam.getArucoID)
t2 = Thread(target=bot.right,args=(20,20))
t2.start()
t1.start()
t1.join()
t2.join()
