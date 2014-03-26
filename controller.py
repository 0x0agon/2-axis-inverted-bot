import time
import math
import numpy as np

class Controller:

    def __init__(self):
        self. maxVoltage = 11.1 #Assumes the motors are running off 11.1 V battery
        self.rpmPerVolt = 0 #the rotational speed per volt
        self.wheelRadius = 0

        self.desiredAngle = 0.0 #Assumes you want to stand up initially
        self.desiredPosition = 0.0 #Assumes you want to stay still initially

        self.errorPendulum = 0.0 #Inits the error var for pendulum angle
        self.errorDeltaPendulum = 0.0 #Inits the error var for pendulum change in ang
        self.errorPenIntegral = 0.0 #Inits the error var for the pendulum integral term
        self.errorCart = 0.0 #Inits the error var for the cart position 
        self.errorDeltaCart = 0.0 #Inits the error var for the change in cart position
        self.errorCartIntegral = 0.0 #Inits the error var for the cart integral term
        
        self.cartErrorArray = np.linspace(0,0,15)
        self.pendulumErrorArray = np.linspace(0,0,15)

        self.Pinverted = 0.0
        self.Iinverted = 0.0
        self.Dinverted = 0.0
        self.Pcart = 0.0
        self.Icart = 0.0
        self.Dcart = 0.0
        self.gains = [[self.Pinverted, self.Iinverted, self.Dinverted],[self.Pcart, self.Icart, self.Dcart]]

        self.currentMotorVoltage = 0.0 #This keeps track of the output voltage for errors

    def changeDesiredAngle(self, newTargetAngle):
        #This function changes the desired angle variable
        #Typically, the angle should be set close to 0 to stand upright
        self.desiredAngle = newTargetAngle

    def changeDesiredPosition(self, newTargetPosition):
        #This function changes the desired position variable
        #Typically, the position should be set to 0, with other values
        #moving it forwards or backwards
        self.desiredPosition = newTargetPosition

    def determineOutput(self, filteredSensorAngle, cartPosition):
        #This function is the meat and potatoes of this class. It determines
        #the necessary motor output voltage from the sensorAngle and
        #cartPositionValue sensor values using two PID controllers.
        #sensorAngle should be in degrees and cartPositionValue should be
        #in inches.
        self.getErrors(filteredSensorAngle, cartPosition)
        outputPendulum = self.Pinverted*self.errorPendulum+self.Dinverted*self.errorDeltaPendulum+self.Iinverted*self.errorPenIntegral
        outputCart = self.Pcart*self.errorCart+self.Dcart*self.errorDeltaCart+self.Icart*self.errorCartIntegral
        output = outputPendulum - outputCart
        if filteredSensorAngle < 50 or filteredSensorAngle >-50:
            if math.fabs(output) > self.maxVoltage:
                if output> 0:
                    return self.maxVoltage - 0.1
                else:
                    return -1*self.maxVoltage + 0.1
            else:
                return output
        else:
            return 0.0
        


    def getErrors(self, filteredSensorAngle, cartPosition):
        #This function calculates and keeps track of error variables
        
        self.pendulumErrorArray =np.roll(self.pendulumErrorArray,1)
        self.errorPendulum = self.desiredAngle - filteredSensorAngle
        self.pendulumErrorArray[0:1] = self.errorPendulum#self.desiredAngle - filteredSensorAngle
        pendulumDerivativeArray = np.diff(self.pendulumErrorArray,1)
        self.errorDeltaPendulum = np.mean(pendulumDerivativeArray)
        if abs(self.errorPenIntegral) >= 150:
            self.errorPenIntegral = 149
        else:
            self.errorPenIntegral = self.errorPendulum + self.errorPenIntegral

        self.cartErrorArray= np.roll(self.cartErrorArray, 1)
        self.errorCart = self.desiredPosition - cartPosition
        self.cartErrorArray[0:1] = self.errorCart
        cartDerivativeArray = np.diff(self.cartErrorArray,1)
        self.errorDeltaCart = np.mean(cartDerivativeArray)
        self.errorCartIntegral = self.errorCart + self.errorCartIntegral
        
    def changeGain(self, invertedOrCartIndicator, pIOrDIndicator, value):
        #This function allows the user to change the gain value of any one
        #gain. The invertedOrCartIndicator should be 0 for inverted pendulum
        #gains and 1 for cart gains. The pIOrDIndicator indicates whether the P,
        #I, or D gain value is going to be changed

        self.gains[invertedOrCartIndicator][pIOrDIndicator] = value
        self.updateGainsFromList()

    def changePInv(self, value):
        #This function allows the user to change the gain of the proportional
        #inverted pendulum term directly
        self.Pinverted = value
        self.updateGainsFromVars()

    def changeIInv(self, value):
        #This function allows the user to change the gain of the integral
        #inverted pendulum term directly
        self.Iinverted = value
        self.updateGainsFromVars()

    def changeDInv(self, value):
        #This function allows the user to change the gain of the derivative
        #inverted pendulum term directly
        self.Dinverted = value
        self.updateGainsFromVars()

    def changePCart(self, value):
        #This function allows the user to change the gain of the proportional
        #cart term directly
        self.Pcart = value
        self.updateGainsFromVars()

    def changeICart(self, value):
        #This function allows the user to change the gain of the integral
        #cart term directly
        self.Icart = value
        self.updateGainsFromVars()

    def changeDCart(self, value):
        #This function allows the user to change the gain of the derivative
        #cart term directly
        self.Dcart = value
        self.updateGainsFromVars()


    def updateGainsFromList(self):
        #This function is meant to be used internally to programatically update
        #the gain values stored in each variable so that they match the values
        #stored inside the list 'gains'
        self.Pinverted = self.gains[0][0]
        self.Iinverted = self.gains[0][1]
        self.Dinverted = self.gains[0][2]
        self.Pcart = self.gains[1][0]
        self.Icart = self.gains[1][1]
        self.Dcart = self.gains[1][2]

    def updateGainsFromVars(self):
        #This function is meant to be used internally to programatically update
        #the gain values stored in each the list 'gains' so that they match the
        #values stored in each variable declaration
        self.gains[0][0] = self.Pinverted
        self.gains[0][1] = self.Iinverted
        self.gains[0][2] = self.Dinverted
        self.gains[1][0] = self.Pcart 
        self.gains[1][1] = self.Icart 
        self.gains[1][2] = self.Dcart

    
