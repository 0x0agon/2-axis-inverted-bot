import time
import math
import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as pwm


class MotorDriver:

    #This class is used to send controller outputs signals to the motors
    #and handles the gpio necessary to correctly control the motor drivers

    def __init__(self):
        #This function creates an object of the MotorDriver Class
        #It also initializes the direction, enable, and pwm pin name variables
        #but does not yet set them, since their names are unknown.
        self.directionPin = 'pin not yet set'
        self.enablePin = 'pin not yet set'
        self.pwmPin = 'pin not yet set'

        self.direction = 0 

    def initialize(self):
        #This funciton sets up and initializes the I/O and pwm pins
        #It also defines the pin names for the objects variables.
        self.directionPin = "P8_14"
        self.enablePin = "P8_12"
        self.pwmPin = "P9_14"
        
        gpio.setup("P8_12", gpio.OUT) #Sets up the Direction Pin
        gpio.setup("P8_14", gpio.OUT) #Sets up the Enable Pin if used
        pwm.start("P9_14", 0) #Sets up the pwm line and sets it to 0

        gpio.output("P8_12", gpio.HIGH) #sets direction to high for no real reason
        gpio.output("P8_14", gpio.LOW) #sets the enable pin low, keeping if off until turned on

    def changePWMFreq(self, desiredFreq):
        #This function is used to change the frequency of the pwm signal
        pwm.set_frequency("P9_14", desiredFreq)


    def enable(self):
        #This function enables the motor driver board
        gpio.output(self.enablePin, gpio.HIGH)

    def sleep(self):
        #This function puts the board to sleep
        gpio.output(self.enablePin, gpio.LOW)

    def driveMotors(self, controllerOutput, MaxVoltage):
        #This function takes a desired motor voltage from the controller and
        #converts it into a pwm duty cycle based off of the MaxVoltage value
        #and a direction based on the sign of the controllerOutput
        if controllerOutput > 0:
            gpio.output(self.directionPin, gpio.HIGH)
        else:
            gpio.output(self.directionPin, gpio.LOW)
            

        dutyCycle = (abs(controllerOutput)/MaxVoltage)*100
        if dutyCycle > 100.0:
            pwm.set_duty_cycle("P9_14", 99.0)
        else:
            pwm.set_duty_cycle("P9_14", dutyCycle)

    def getDirection(self):
        #This function simply returns the current direction value
        direction = self.direction
        return direction

    def end(self):
        #This function is used to end the session, cleaning up all gpio pins
        #and pwm pins used
        pwm.stop("P9_14")
        pwm.cleanup("P9_14")
        gpio.cleanup()
        
        
        
    
