import Adafruit_BBIO.GPIO as gpio
import carttracker
import motordriver

gpio.setup("P8_17", gpio.IN) #This sets up the pin we want to use to listen to the encoder
gpio.add_event_detect("P8_17", gpio.RISING)

driver = motordriver.MotorDriver()
driver.initialize()

cart = carttracker.CartTracker()
cart.initialize(driver)

driver.driveMotors(2,11) # This is done only to set a direction for the motors so that the cart tracker can grab that direction and find position and velocity

while True:
    if gpio.event_detected("P8_17"):
        cart.getEncoderUpdate()
        print cart.encoderTicCounter, cart.currentPosition, cart.currentVelocity, cart.elapsedTime
    else:
        pass
