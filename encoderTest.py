import Adafruit_BBIO.GPIO as gpio
import carttracker
import motordriver

gpio.setup("P8_17", gpio.IN) #This sets up the pin we want to use to listen to the encoder
gpio.add_event_detect("P8_17", gpio.BOTH)

gpio.setup("P8_13", gpio.IN)
gpio.add_event_detect("P8_13", gpio.BOTH)

driver = motordriver.MotorDriver()
driver.initialize()

cart = carttracker.CartTracker()
cart.initialize(driver)


while True:
    if gpio.event_detected("P8_17"):
        cart.updateState(gpio.input("P8_17"),gpio.input("P8_13"))
        cart.getEncoderUpdate()
        #print cart.encoderTicCounter, cart.currentPosition, cart.currentVelocity, cart.elapsedTime
        print 'direction= ', cart.direction, 'encoder= ', cart.encoderTicCounter
    else:
        pass
    if gpio.event_detected("P8_13"):
        cart.updateState(gpio.input("P8_17"),gpio.input("P8_13"))
        
    else:
        pass        
