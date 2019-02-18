from utils import Bot
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(0.5)
base_speed = 80
serial_output = 1

prev_reading = ''
node_count = 0

bot = Bot()
#bot.forward(50,50)
'''while node_count < 2:
    serial_output = str(ser.readline())
    serial_output = serial_output[2:-5]
    if serial_output == 'N':
        print("[NODE]")
        if prev_reading != 'N':
            node_count += 1
    else:
        motor_speed = float(serial_output)
        print("[{}]".format(motor_speed))
        bot.forward(base_speed - motor_speed,base_speed + motor_speed)
    prev_reading = serial_output
'''
for _ in range(10000):
   bot.right(50,50)
print(serial_output)
while serial_output != -10:
    serial_output = str(ser.readline())
    serial_output = float(serial_output[2:-5])
    print(serial_output)
    bot.right(90,90)
bot.stop()
