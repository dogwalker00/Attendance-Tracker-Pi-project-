#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

IrPin  = 18   # receiver (BOARD numbering in your original)
EmitterPin = 5  # emitter on physical pin 5 (BOARD mode)
count = 0

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EmitterPin, GPIO.OUT)
    GPIO.output(EmitterPin, GPIO.HIGH)  # keep emitter always ON

def cnt(ev=None):
    global count
    count += 1
    print('Received infrared. cnt =', count)

def loop():
    GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=cnt) # wait for falling
    try:
        while True:
            print("no signal")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def destroy():
    GPIO.output(EmitterPin, GPIO.LOW)  # turn off emitter on cleanup
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

