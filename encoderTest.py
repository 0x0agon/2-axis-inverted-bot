import Adafruit_BBIO.GPIO as gpio
import carttracker
import motordriver

gpio.setup("P8_17", gpio.IN) #This sets up the pin we want to use to listen to the encoder
gpio.add_event_detect("P8_17", gpio.RISING)

gpio.setup("P8_13", gpio.IN)
gpio.add_event_detect("P8_13", gpio.RISING)

driver = motordriver.MotorDriver()
driver.initialize()

cart = carttracker.CartTracker()
cart.initialize(driver)


while True:
    if gpio.event_detected("P8_17"):
        cart.getEncoderUpdate()
        #print cart.encoderTicCounter, cart.currentPosition, cart.currentVelocity, cart.elapsedTime
        print 'time 1= ', self.currentTime
    elif gpio.event_detected("P8_13"):
        cart.updateLine2Time()
        print 'time 2= ', self.previousTimeLine2
    else:
        pass        
