#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PIN = 18      # BOARD pin number for the single control signal
FREQ = 2000   # PWM frequency in Hz
ON_DUTY = 100 # duty cycle for "on" (0-100)
OFF_DUTY = 0  # duty cycle for "off"
INTERVAL = 5  # seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)

p = GPIO.PWM(PIN, FREQ)
p.start(OFF_DUTY)

try:
    while True:
        p.ChangeDutyCycle(ON_DUTY)
        time.sleep(INTERVAL)
        p.ChangeDutyCycle(OFF_DUTY)
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    pass
finally:
    p.stop()
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()

