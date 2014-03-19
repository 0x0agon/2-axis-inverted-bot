import time
import math
import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as pwm


class TorqueDriver:

    #This class is used to send controller output signals to the torque wheel 
    #motor and handles the gpio necessary to correctly control the motor 
    #drivers. This class is a copy of the motordriver.py class, with the
    #pin locations changed. This is needed since the pin locations have to
    #hard coded in.

    def __init__(self):
        #This function creates an object of the TorqueDriver Class
        #It also initializes the direction, enable, and pwm pin name variables
        #but does not yet set them, since their names are unknown.
        directionPin = 'pin not yet set'
        enablePin = 'pin not yet set'
        pwmPin = 'pin not yet set'


    def initialize(self):
        #This funciton sets up and initializes the I/O and pwm pins
        #It also defines the pin names for the objects variables.
        self.directionPin = "P8_18"
        self.enablePin = "P8_16"
        self.pwmPin = "P9_16"
        
        gpio.setup("P8_18", gpio.OUT) #Sets up the Direction Pin
        gpio.setup("P8_16", gpio.OUT) #Sets up the Enable Pin if used
        pwm.start("P9_16", 0) #Sets up the pwm line and sets it to 0

        gpio.output("P8_18", gpio.HIGH) #sets direction to high for no real reason
        gpio.output("P8_16", gpio.LOW) #sets the enable pin low, keeping if off until turned on

    def changePWMFreq(self, desiredFreq):
        #This function is used to change the frequency of the pwm signal
        pwm.set_frequency("P9_16", desiredFreq)


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
        if controllerOutput > 1:
            gpio.output(self.directionPin, gpio.HIGH)
        else:
            gpio.output(self.directionPin, gpio.LOW)

        dutyCycle = (math.fabs(controllerOutput)/MaxVoltage)*100
        if dutyCycle > 100.0:
            pwm.set_duty_cycle("P9_16", 99.0)
        else:
            pwm.set_duty_cycle("P9_16", dutyCycle)

    def end(self):
        #This function is used to end the session, cleaning up all gpio pins
        #and pwm pins used
        pwm.stop("P9_16")
        pwm.cleanup("P9_16")
        gpio.cleanup()
        
        
        
    
