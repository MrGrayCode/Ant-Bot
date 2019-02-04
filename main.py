from utils import Bot
from utils import Camera
from threading import Thread
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)
count = 0
ch = ''
bot = Bot()
while count < 2:
    ch = str(ser.readline())
    ch = ch[2]
    #print(ch)
    if ch == '1':
        bot.forward(40,25)
    elif ch == '2':
        bot.forward(40,30)
    elif ch == '3':
        bot.forward()
    elif ch == '4':
        bot.forward(25,40)
    elif ch == '5':
        bot.forward(30,40)
    elif ch == '6':
        #print("[NODE]")
        count += 1

t = 0
ids = []
cam = Camera()
t1 = Thread(target=cam.getArucoID)
t2 = Thread(target=bot.right,args=(20,20))
#print("LLLLL")
t2.start()
t1.start()
#print("HERE")
t1.join()
t2.join()
