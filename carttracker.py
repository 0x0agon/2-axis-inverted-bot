#This code creates the cart tracker class, which is responsible
#for taking in encoder data from the gear motors and returning
#the wheel speed, position, and possibly acceleration as needed

import math
import time
import Adafruit_BBIO.GPIO as gpio


class CartTracker:

    #This class sets up the necessary gpio in order to read the
    #motor encoders so that accurate wheel speed, position, and 
    #acceleration can be found and passed to other classes.

    def __init__(self):
        #This funciton creates an object of the CartTracker class

        self.encoderDataPin1 = 'pin not yet set, initialize object'
        self.currentVelocity = 0.0
        self.previousVelocity = 0.0

        self.currentPosition = 0.0
        self.previousPosition = 0.0

        self.currentTime = time.time
        self.elapsedTime = 1000

        self.encoderTicCounter = 0

        self.wheelDiameter = 4 #This is the diameter of the wheel in inches
        self.gearRatio = 1/29 #This is the ratio of the number of times the motor spins compared to one rotation of the wheel axis

    def initialize(self, motorDriverObjectName):
        #This function sets up the I/O needed

        self.motorDriverObjectName = motorDriverObjectName #Stores the name of the specific object so that the current motor direction can be found programmatically

        self.encoderDataPin1 = "P8_17" #This is the pin for the encoder data bits

        gpio.setup(self.encoderDataPin1, gpio.IN) #This sets the pin up to read the incoming bits from the encoder

        gpio.add_event_detect(self.encoderDataPin1, gpio.RISING) #This tells the BBB to create an event when the encoder data pin changes from low to high.
                                                                 #We will use this to increment the counter without stopping the program.


    def getDirection(self,motorDriverObjectName):
        #This grabs the direction from the motor driver object
        #The value should either be a 0 or a 1

        self.direction = motorDriverObjectName.getDirection()

    def findPosition(self):
        #This function calculates the current position relative to where the robot started
        #using the encoder tic counter, the radius of the wheel, and the gear ratio of the motor
        
        self.previousPosition = self.currentPosition
        self.currentPosition = self.encoderTicCounter * self.gearRatio * self.wheelDiameter

    def findVelocity(self):
        #This function calculates the current velocity based on the elapsed time, 
        #currentPosition, and previous position

        self.previousVelocity = self.currentVelocity
        self.currentVelocity = (self.currentPosition - self.previousPosition)/self.elapsedTime

    #The following code should run whenever an event is detected
    #Which should only occur when the encoder data bit switches
    #from a 0 to a 1.
    if gpio.event_detected("P8_17"):
        oldTime = self.currentTime
        self.currentTime = time.time()
        self.elapsedTime = self.currentTime - oldTime #This gives the elapsed time for position and velocity calculations

        self.encoderTicCounter = self.encoderTicCounter + (-1)**self.getDirection(self.motorDriverObjectName)

    
