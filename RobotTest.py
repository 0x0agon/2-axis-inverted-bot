import mpu6050
import ComplimentaryFilter
mpu = mpu6050.MPU6050()
mpu.initialize()

xFilter = ComplimentaryFilter.ComplimentaryFilter()
yFilter = ComplimentaryFilter.ComplimentaryFilter()
#gyroXAng = 0
#gyroYAng = 0

while True:
    deltaGyroX = xFilter.getGyroAngPositionChange(mpu.getRealGyroData('x'), xFilter.getTimeSinceLast())
    deltaGyroY = yFilter.getGyroAngPositionChange(mpu.getRealGyroData('y'), yFilter.getTimeSinceLast())
    rollPitch = xFilter.getAccelRollPitch(mpu.getRealAccelData('x'),mpu.getRealAccelData('y'), mpu.getRealAccelData('z'))
    rollAngle = -rollPitch[0]
    pitchAngle = -rollPitch[1]
    #gyroXAng = gyroXAng + deltaGyroX
    #gyroYAng = gyroYAng + deltaGyroY
    yAngle = yFilter.findFilteredAngle(deltaGyroY, pitchAngle)
    xAngle = xFilter.findFilteredAngle(deltaGyroX, rollAngle)
    #print 'roll= ', rollAngle, 'pitch= ', pitchAngle, 'X Gyro= ', gyroXAng, 'Y Gyro = ', gyroYAng
    print 'roll= ', xAngle, 'pitch= ', yAngle
