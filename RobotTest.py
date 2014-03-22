import Adafruit_BBIO.GPIO as gpio
import mpu6050
import ComplimentaryFilter
import controller
import motordriver
import carttracker

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

#Setup the GPIO pin used for the drive wheel encoder and 
#create an event for the pin. 
gpio.setup("P8_17", gpio.IN)
gpio.add_event_detect("P8_17", gpio.RISING)

#Create the drive wheel controller object
troll = controller.Controller()
troll.changeDesiredAngle(2.85)

    #Change the Pendulum Gains
troll.changePInv(0.01)
#troll.changePInv(2.70) #1.72 is good for P alone
#troll.changeDInv(1.65) #2.30
#troll.changeIInv(0.06) #0.04

    #Change the Cart Gains
troll.changePCart(0.5)

while True:
    if gpio.event_detected("P8_17"):
        cart.getEncoderUpdate()
    else:       #Will eventually need to add an elif for the other encoder
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
        print 'Angle= ', xAngle, 'Encoder= ', cart.encoderTicCounter, 'Position= ', cart.currentPosition
    
