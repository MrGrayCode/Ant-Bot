'''
* Team ID : 117
* Author List : Ebey Abraham
* Filename : bot.py
* Theme : Antbot
* Functions : forward(int),backward(int),left(int),right(int),stop()
* Global Variables : NONE
'''
import RPi.GPIO as GPIO

class Bot:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        #motor_pins stores the values of the pins to interface the motor in the order - 1A 1B 1E 2A 2B 2E
        self.motor_pins = [33,35,37,36,38,40] 
        for motor_pin in self.motor_pins:
            GPIO.setup(motor_pin,GPIO.OUT)
        self.left_motor = GPIO.PWM(self.motor_pins[2],100)
        self.right_motor = GPIO.PWM(self.motor_pins[5],100)

    '''
    * Function Name : forward
    * Input : duty_cycle (optional) -> the duty cycle of PWM output
    * Output : Moves bot forward
    * Logic : move left and right motors in same direction
    * Example Call : forward(25)
    '''
    def forward(self,duty_cycle = 50):
        print("[FORWARD]")
        self.left_motor.start(duty_cycle)
        self.right_motor.start(duty_cycle)
        GPIO.output(self.motor_pins[0],GPIO.LOW)
        GPIO.output(self.motor_pins[1],GPIO.HIGH)
        GPIO.output(self.motor_pins[3],GPIO.LOW)
        GPIO.output(self.motor_pins[4],GPIO.HIGH)
    
    '''
    * Function Name : backward
    * Input : duty_cycle (optional) -> the duty cycle of PWM output
    * Output : Moves bot backward
    * Logic : move left and right motors in same direction
    * Example Call : backward(25)
    '''
    def backward(self,duty_cycle = 50):
        print("[BACKWARD]")
        self.left_motor.start(duty_cycle)
        self.right_motor.start(duty_cycle)
        GPIO.output(self.motor_pins[0],GPIO.HIGH)
        GPIO.output(self.motor_pins[1],GPIO.LOW)
        GPIO.output(self.motor_pins[3],GPIO.HIGH)
        GPIO.output(self.motor_pins[4],GPIO.LOW)

    '''
    * Function Name : left
    * Input : duty_cycle (optional) -> the duty cycle of PWM output
    * Output : Moves bot left
    * Logic : move left and right motors in opposite direction
    * Example Call : left(25)
    '''
    def left(self,duty_cycle = 50):
        print("[LEFT]")
        self.left_motor.start(duty_cycle)
        self.right_motor.start(duty_cycle)
        GPIO.output(self.motor_pins[0],GPIO.HIGH)
        GPIO.output(self.motor_pins[1],GPIO.LOW)
        GPIO.output(self.motor_pins[3],GPIO.LOW)
        GPIO.output(self.motor_pins[4],GPIO.HIGH)

    '''
    * Function Name : right
    * Input : duty_cycle (optional) -> the duty cycle of PWM output
    * Output : Moves bot right
    * Logic : move left and right motors in opposite direction
    * Example Call : right(25)
    '''
    def right(self,duty_cycle = 50):
        print("[RIGHT]")
        self.left_motor.start(duty_cycle)
        self.right_motor.start(duty_cycle)
        GPIO.output(self.motor_pins[0],GPIO.LOW)
        GPIO.output(self.motor_pins[1],GPIO.HIGH)
        GPIO.output(self.motor_pins[3],GPIO.HIGH)
        GPIO.output(self.motor_pins[4],GPIO.LOW)

    '''
    * Function Name : stop
    * Input : NONE
    * Output : stops the motors
    * Logic : -
    * Example Call : stop()
    '''
    def stop(self):
        print("[STOP]")
        self.left_motor.stop()
        self.right_motor.stop()
        GPIO.output(self.motor_pins[2],GPIO.LOW)
        GPIO.output(self.motor_pins[5],GPIO.LOW)

if __name__ == "__main__":
    bot = Bot()
    bot.forward()