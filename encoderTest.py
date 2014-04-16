import Adafruit_BBIO.GPIO as gpio
import carttracker
import motordriver
import time

gpio.setup("P8_17", gpio.IN) #This sets up the pin we want to use to listen to the encoder
#gpio.add_event_detect("P8_17", gpio.BOTH, callback=event1Callback)

gpio.setup("P8_13", gpio.IN)
#gpio.add_event_detect("P8_13", gpio.BOTH, callback=event2Callback)

driver = motordriver.MotorDriver()
driver.initialize()

cart = carttracker.CartTracker()
cart.initialize(driver)

def event1Callback(channel):
    cart.updateState(gpio.input("P8_17"), gpio.input("P8_13"))
    cart.getEncoderUpdate()

def event2Callback(channel):
    cart.updateState(gpio.input("P8_17"), gpio.input("P8_13"))

gpio.add_event_detect("P8_17", gpio.BOTH, callback=event1Callback)
gpio.add_event_detect("P8_13", gpio.BOTH, callback=event2Callback)

while True:
    previousTime = time.time()
    #if gpio.event_detected("P8_17"):
    #    cart.updateState(gpio.input("P8_17"),gpio.input("P8_13"))
    #    cart.getEncoderUpdate()
    #    #print cart.encoderTicCounter, cart.currentPosition, cart.currentVelocity, cart.elapsedTime
    #    print 'direction= ', cart.direction, 'encoder= ', cart.encoderTicCounter
    #else:
    #    pass
    #if gpio.event_detected("P8_13"):
    #    cart.updateState(gpio.input("P8_17"),gpio.input("P8_13"))
        
    #else:
    #    pass        
    elapsed = time.time() - previousTime

    print cart.direction, 'elapsed= ', elapsed
    
