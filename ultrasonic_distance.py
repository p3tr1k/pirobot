import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    distance = 0
    for i in range(5):
#        GPIO.output(GPIO_TRIGGER, False)
#        time.sleep(0.1)
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

#def priemer():
#    vzdial = 0
#    for i in range(5): 
#        vzdialenost = distance()
#        vzdial = vzdial + vzdialenost
#    vzdial = vzdial/5
#    return vzdial


if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
