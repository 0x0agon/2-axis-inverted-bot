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

        self.currentTime = time.time()
        self.elapsedTime = 1000 

        self.encoderTicCounter = 0

        self.direction = 0

        self.newState = 0
        self.oldState = 0
      
        self.wheelDiameter = 4.0 #This is the diameter of the wheel in inches
        self.gearRatio = (1.0/29) #This is the ratio of the number of times the motor spins compared to one rotation of the wheel axis

    def initialize(self, motorDriverObjectName):
        #This function sets up the I/O needed

        self.motorDriverObjectName = motorDriverObjectName #Stores the name of the specific object so that the current motor direction can be found programmatically

        self.encoderDataPin1 = "P8_17" #This is the pin for the encoder data bits, only a reference for the user

        #gpio.setup(self.encoderDataPin1, gpio.IN) #This sets the pin up to read the incoming bits from the encoder

        #gpio.add_event_detect("P8_17", gpio.RISING) #This tells the BBB to create an event when the encoder data pin changes from low to high.
                                                    #We will use this to increment the counter without stopping the program.

    def getEncoderUpdate(self):
        #This funciton should be triggered whenever the encoder bit changes
        #This funciton updates the position, velocity, elapsed time, current time, and direction variables

        self.findDirection() #It is important to find the direction before updating the time

        self.encoderTicCounter = self.encoderTicCounter + (-1) ** self.direction #This increments or decrements the counter according to direction of the motor spin


    def updateState(self,lineAValue, lineBValue):
        #This funciton serves to update the time since the last
        #rising edge on encoder data line 2
        
        self.oldState = self.newState

        if lineAValue == 0 and lineBValue == 0:
            self.newState = 0
        elif lineAValue == 0 and lineBValue == 1:
            self.newState = 1
        elif lineAValue == 1 and lineBValue == 1:
            self.newState = 2
        elif lineAValue == 1 and lineBValue == 0:
            self.newState = 3
        else:
            print "Congrats, the encoder found the mythical 5th state. You've broken digital logic."
            

    def findDirection(self):
        #This function finds the difference between encoder pulses in time
        #from which the direction can be found
        #The value should either be a 0 or a 1

        #if self.oldState == 0 and self.newState == 1:
        #    self.direction = 0
        #elif self.oldState == 1 and self.newState == 2:
        #    self.direction = 0
        #elif self.oldState == 2 and self.newState == 3:
        #    self.direction = 0
        #elif self.oldState == 3 and self.newState == 0:
        #    self.direction = 0
        #elif self.oldState == 0 and self.newState == 3:
        #    self.direction = 1
        #elif self.oldState == 3 and self.newState == 2:
        #    self.direction = 1
        #elif self.oldState == 2 and self.newState == 1:
        #    self.direction = 1
        #elif self.oldState == 1 and self.newState == 0:
        #    self.direction = 1
        #else:
        #    self.direction = self.direction
        if 3>(self.newState - self.oldState) >= 1 or (self.newState - self.oldState) <= -3:
            self.direction = 0
        elif -3<(self.newState - self.oldState) <= -1 or (self.newState - self.oldState) >= 3:
            self.direction = 1
        else:
            pass


    def findPosition(self):
        #This function calculates the current position relative to where the robot started
        #using the encoder tic counter, the radius of the wheel, and the gear ratio of the motor
        
        self.previousPosition = self.currentPosition
        self.currentPosition = (self.encoderTicCounter/16.0) * self.gearRatio * self.wheelDiameter

        #This is for velocity calculations
        self.oldTime = self.currentTime
        self.currentTime = time.time()
        self.elapsedtime = self.currentTime - self.oldTime
        return self.currentPosition

    def findVelocity(self):
        #This function calculates the current velocity based on the elapsed time, 
        #currentPosition, and previous position

        self.previousVelocity = self.currentVelocity
        self.currentVelocity = (self.currentPosition - self.previousPosition)/self.elapsedTime
        return self.currentVelocity
    
        #The following code should run whenever an event is detected
        #Which should only occur when the encoder data bit switches
        #from a 0 to a 1.
       # if gpio.event_detected("P8_17"):
       #     oldTime = self.currentTime
       #     self.currentTime = time.time()
       #     self.elapsedTime = self.currentTime - oldTime #This gives the elapsed time for position and velocity calculations

       #     self.encoderTicCounter = self.encoderTicCounter + (-1) ** self.direction
       # else:
       #     pass
    
