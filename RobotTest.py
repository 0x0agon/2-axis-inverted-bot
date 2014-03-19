import mpu6050
import ComplimentaryFilter
import controller
import motordriver

mpu = mpu6050.MPU6050()
mpu.initialize()

xFilter = ComplimentaryFilter.ComplimentaryFilter()
yFilter = ComplimentaryFilter.ComplimentaryFilter()
#gyroXAng = 0
#gyroYAng = 0

driver = motordriver.MotorDriver()
driver.initialize()
driver.enable()

troll = controller.Controller()
troll.changeDesiredAngle(0.65)
troll.changePInv(2.20) #1.72 is good for P alone
troll.changeDInv(1.65) #2.30
troll.changeIInv(0.075) #0.04

while True:
    deltaGyroX = xFilter.getGyroAngPositionChange(mpu.getRealGyroData('x'), xFilter.getTimeSinceLast())
    deltaGyroY = yFilter.getGyroAngPositionChange(mpu.getRealGyroData('y'), yFilter.getTimeSinceLast())
    rollPitch = xFilter.getAccelRollPitch(mpu.getRealAccelData('x'),mpu.getRealAccelData('y'), mpu.getRealAccelData('z'))
    rollAngle = -rollPitch[0]
    pitchAngle = -rollPitch[1]
    #gyroXAng = gyroXAng - deltaGyroX
    #gyroYAng = gyroYAng + deltaGyroY
    yAngle = yFilter.findFilteredAngle(deltaGyroY, pitchAngle)
    xAngle = xFilter.findFilteredAngle(deltaGyroX, rollAngle)
    #print 'roll= ', rollAngle, 'pitch= ', pitchAngle, 'X Gyro= ', gyroXAng, 'Y Gyro = ', gyroYAng
    #print 'roll= ', xAngle, 'pitch= ', yAngle
    output = troll.determineOutput(xAngle, 0 ,deltaGyroX, 0)
    driver.driveMotors(output,troll.maxVoltage)
    print 'P = ', troll.errorPendulum, 'I = ', troll.errorPenIntegral, 'D = ', troll.errorDeltaPendulum
    #print 'Angle = ', xAngle

