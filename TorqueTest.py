import mpu6050
import ComplimentaryFilter
import controller
import torquedriver

mpu = mpu6050.MPU6050()
mpu.initialize()

xFilter = ComplimentaryFilter.ComplimentaryFilter()
yFilter = ComplimentaryFilter.ComplimentaryFilter()

tDriver = torquedriver.TorqueDriver()
tDriver.initialize()
tDriver.enable()

troll = controller.Controller()
troll.changeDesiredAngle(0.0)
troll.changePInv(5.0)

while True:
    deltaGyroY = yFilter.getGyroAngPositionChange(mpu.getRealGyroData('y'), yFilter.getTimeSinceLast())
    deltaGyroX = xFilter.getGyroAngPositionChange(mpu.getRealGyroData('x'), xFilter.getTimeSinceLast())
    rollPitch = xFilter.getAccelRollPitch(mpu.getRealAccelData('x'), mpu.getRealAccelData('y'), mpu.getRealAccelData('z'))
    rollAngle = -rollPitch[0]
    pitchAngle = -rollPitch[1]

    yAngle = yFilter.findFilteredAngle(deltaGyroY, pitchAngle)
    xAngle = xFilter.findFilteredAngle(deltaGyroX, rollAngle)

    output = troll.determineOutput(yAngle, 0, deltaGyroY, 0)
    tDriver.driveMotors(output, troll.maxVoltage)
    print output 
