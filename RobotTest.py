import Adafruit_BBIO.GPIO as gpio
import Adafruit_BBIO.PWM as pwm
import mpu6050
import ComplimentaryFilter
import controller
import motordriver
import carttracker

#Clean up GPIO and PWM pins from any aborted programs
gpio.cleanup()
pwm.cleanup()

#Create an mpu6050 object for the IMU sensor input
mpu = mpu6050.MPU6050()
mpu.initialize()

#Create two filter objects, one for each axis
xFilter = ComplimentaryFilter.ComplimentaryFilter()
yFilter = ComplimentaryFilter.ComplimentaryFilter()
gyroXAng = 0
gyroYAng = 0

#Create the driver object for the main drive wheel
driver = motordriver.MotorDriver()
driver.initialize()
driver.enable()

#Create a carttracker object to read the drive wheel encoder data
#Will eventually also need one for the Torque wheel encoder data
cart = carttracker.CartTracker()
cart.initialize(driver)

#Setup the callback events needed for the encoders
def event1Callback(channel):
    cart.updateState(gpio.input("P8_17"), gpio.input("P8_13"))
    cart.getEncoderUpdate()

def event2Callback(channel):
    cart.updateState(gpio.input("P8_17"), gpio.input("P8_13"))

#Setup the GPIO pin used for the drive wheel encoder and 
#create an event for the pin. 
gpio.setup("P8_17", gpio.IN) #This is the main encoder data pin
gpio.add_event_detect("P8_17", gpio.BOTH, callback=event1Callback)

gpio.setup("P8_13", gpio.IN) #This pin is used only to determine direction
gpio.add_event_detect("P8_13", gpio.BOTH, callback=event2Callback)

#Create the drive wheel controller object
troll = controller.Controller()
troll.changeDesiredAngle(2.32)

    #Change the Pendulum Gains
#troll.changePInv(1)
troll.changePInv(1.00) #1.72 is good for P alone
troll.changeDInv(0.00) #2.30
troll.changeIInv(0.00) #0.04

    #Change the Cart Gains
#troll.changePCart(6.0) #8
#troll.changeICart(0.02)
#troll.changeDCart(18.0) #25

while True:

        deltaGyroX = xFilter.getGyroAngPositionChange(mpu.getRealGyroData('x'), xFilter.getTimeSinceLast())
        deltaGyroY = yFilter.getGyroAngPositionChange(mpu.getRealGyroData('y'), yFilter.getTimeSinceLast())
        rollPitch = xFilter.getAccelRollPitch(mpu.getRealAccelData('x'),mpu.getRealAccelData('y'), mpu.getRealAccelData('z'))
        rollAngle = -rollPitch[0]
        pitchAngle = -rollPitch[1]
        gyroXAng = gyroXAng - deltaGyroX
        gyroYAng = gyroYAng + deltaGyroY
        yAngle = yFilter.findFilteredAngle(deltaGyroY, pitchAngle)
        xAngle = xFilter.findFilteredAngle(deltaGyroX, rollAngle)
        #print 'roll= ', rollAngle, 'pitch= ', pitchAngle, 'X Gyro= ', gyroXAng, 'Y Gyro = ', gyroYAng
        #print 'roll= ', xAngle, 'pitch= ', yAngle
    
        output = troll.determineOutput(xAngle, cart.currentPosition)
        driver.driveMotors(output,troll.maxVoltage)
        #print 'P = ', troll.errorPendulum, 'I = ', troll.errorPenIntegral, 'D = ', troll.errorDeltaPendulum
        #print 'Angle = ', xAngle, 'Accel= ', rollAngle, 'Gyro= ', gyroXAng
        #print 'Angle= ', xAngle, 'Encoder= ', cart.encoderTicCounter, 'Output= ', output
        print troll.pendulumErrorArray
        
