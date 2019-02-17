from utils import Bot
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(0.5)
serial_output = ''

bot = Bot()

while True:
    serial_output = str(ser.readline())
    serial_output = serial_output[2:-5]
    if serial_output == 'N':
        print("[NODE]")
    else:
        leftMotorSpeed,rightMotorSpeed = map(int,serial_output.split(','))
        print("[{},{}]".format(leftMotorSpeed,rightMotorSpeed))
        bot.forward(leftMotorSpeed,rightMotorSpeed)

