#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# --- Config ---
IR_PIN = 18        # IR receiver input (BCM)
EMITTER_PIN = 5    # IR emitter output (BCM)
RGB_PIN = 12       # single-channel RGB control PWM pin (BCM) — change to your pin
PWM_FREQ = 1000
DEBOUNCE_MS = 200
STATUS_INTERVAL = 1.0
COMMON_ANODE = False   # False if common-cathode (drive HIGH to turn on)

# Duty values (0-100)
ON_DUTY = 100
OFF_DUTY = 0

count = 0
_last_event_time = 0.0

def now_ms():
    return time.time() * 1000.0

def setup():
    global pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(EMITTER_PIN, GPIO.OUT)
    GPIO.output(EMITTER_PIN, GPIO.HIGH)  # keep emitter ON
    GPIO.setup(RGB_PIN, GPIO.OUT)
    pwm = GPIO.PWM(RGB_PIN, PWM_FREQ)
    pwm.start(OFF_DUTY if not COMMON_ANODE else ON_DUTY)  # start off

def set_rgb_on():
    duty = ON_DUTY if not COMMON_ANODE else (100 - ON_DUTY)
    pwm.ChangeDutyCycle(duty)

def set_rgb_off():
    duty = OFF_DUTY if not COMMON_ANODE else (100 - OFF_DUTY)
    pwm.ChangeDutyCycle(duty)

def handle_ir(channel):
    global count, _last_event_time
    now = now_ms()
    if now - _last_event_time < DEBOUNCE_MS:
        return
    _last_event_time = now

    state = GPIO.input(IR_PIN)
    # Typical: HIGH = beam present, LOW = beam broken. Invert if your sensor differs.
    if state == GPIO.LOW:
        count += 1
        set_rgb_on()
        print(f"Beam disrupted! Count = {count}")
    else:
        set_rgb_off()
        print("Beam restored")

def loop():
    GPIO.add_event_detect(IR_PIN, GPIO.BOTH, callback=handle_ir, bouncetime=DEBOUNCE_MS)
    try:
        last_status = time.time()
        while True:
            if time.time() - last_status >= STATUS_INTERVAL:
                pin_state = GPIO.input(IR_PIN)
                print("Beam present" if pin_state == GPIO.HIGH else "Beam disrupted (holding)")
                last_status = time.time()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

def destroy():
    set_rgb_off()
    pwm.stop()
    GPIO.output(EMITTER_PIN, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

