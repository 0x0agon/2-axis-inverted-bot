# Complimentary Filter Class
# used to find and return the current filtered angle using
# a complimentary filter

import time
import math


class ComplimentaryFilter:

    

    def __init__(self):
       self.currentTime = time.time() #This variable is the time of the last check, initialized here
       self.filteredAngle = 0.0 #This is needed since the filteredAngle is a running average


    def getTimeSinceLast(self):
        #This function finds the elapsed time, and resents teh lastTimeCheck variable to the current time
        oldTime = self.currentTime
        now = time.time()
        self.currentTime = now
        elapsed = now-oldTime
        return elapsed

    def getAccelAngPosition(self, mainAxisValue, secondaryAxisValue):
        #This funciton finds the angle of the sensor relative to the main axis
        #It returns an angle
        #mainAxis and secondary Axis shoud be either 'x','y', or 'z'
        #NOTE: This only works for rotation about a single axis. Rotation about multiple axis will result in a
        #      result that is not accurate.
        accelPosition = math.atan2(mainAxisValue, secondaryAxisValue)*(180/math.pi)
        return accelPosition

    def getAccelRollPitch(self, Gx, Gy, Gz):
        #This function computes the roll and picth angles for motion in 3D space
        #Roll is the angle about the x-axis, Pitch is the angle about the y-axis
        #Yaw is currently unimplemented
        roll = math.atan2(Gy, Gz)*180/math.pi +5 #The +5 is for an angular offset, since it sits at -4.9 on a flat table
        pitch1 = math.sqrt(Gy*Gy + Gz*Gz)
        pitch = math.atan2(Gx, pitch1)*180/math.pi
        return roll, pitch

    def getGyroAngPositionChange(self, rotationAxisValue, elapsedTime):
        #This funciton finds the angular position change
        dt = elapsedTime
        gyroAngPositionChange = -1*rotationAxisValue*dt
        return gyroAngPositionChange

    def findFilteredAngle(self, gyroAngPositionChange, accelAngPosition):
        #This funciton takes in values from the accels and gyros to create an accurate 
        #estimation of the angle of the robot using a complimentary filter.
        #Use a roll or pitch angle for the accelAngPosition variable if operating in 3d space
        self.filteredAngle = (0.95*(self.filteredAngle + gyroAngPositionChange)) + (0.05*accelAngPosition)
        return self.filteredAngle
