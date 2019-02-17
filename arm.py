import RPi.GPIO as GPIO 
import time

GPIO.setwarnings(False)

def softTurn(start,stop,servo):
	r = 1
	if start < stop:
		r*=-1
	for i in range(start,stop,r):
		servo.ChangeDutyCycle(i/10)
		time.sleep(.1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

p=GPIO.PWM(11,50)
q=GPIO.PWM(13,50)
r=GPIO.PWM(15,50)
q.start(2.5)
r.start(5)
print("first part")
time.sleep(1)
q.ChangeDutyCycle(5.6)
time.sleep(1)
r.ChangeDutyCycle(9)
time.sleep(.5)
q.ChangeDutyCycle(10)
time.sleep(1)
r.ChangeDutyCycle(5)
time.sleep(.5)
q.ChangeDutyCycle(5.6)
time.sleep(2)
q.ChangeDutyCycle(10)
time.sleep(.5)
r.ChangeDutyCycle(9)
time.sleep(.5)
q.ChangeDutyCycle(5.6)
time.sleep(1)
r.ChangeDutyCycle(5)
time.sleep(.5)
q.ChangeDutyCycle(3)
