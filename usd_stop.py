import time
import RPi.GPIO as GPIO
import app

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    distance = 0
    for i in range(5):
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.1)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        vzdialenost = TimeElapsed * 17150
        distance = distance + vzdialenost

    distance /= 5

    return distance

def stop():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)



x = distance()
while True:
    y = app.state
    print(y)
    x = distance()
    if x < 35 and y == 'frw':
        stop()
        print('stop')
        continue
    else:
        pass

