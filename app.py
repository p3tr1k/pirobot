#/usr/bin/env python
from flask import Flask, render_template, Response
from camera import Camera
import time
import pantilthat

import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

###########################################################
GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    distance = 0
    for i in range(5):
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.01)
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


###########################################################
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

@app.route("/")
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame =  camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

###
@app.route('/light')
def light():
        state = GPIO.input(23)
        if state == 1:
            GPIO.output(23, GPIO.LOW)
        else:
            GPIO.output(23, GPIO.HIGH)

@app.route('/forward')
def forward():
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)

        while True:
            x = distance()
            if x < 35:
                stop()
                break
            else:
                pass


@app.route('/reverse')
def reverse():
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)

@app.route('/stop')
def stop():
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

@app.route('/left')
def left():
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
        time.sleep(0.2)
        stop()

@app.route('/right')
def right():
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)
        time.sleep(0.2)
        stop()



###
@app.route("/cam_left")
def cam_left():
        x = pantilthat.get_pan()
        if x + 20 > 90:
            x = 90
        else:
            x += 20
        pantilthat.pan(x)


@app.route("/cam_right")
def cam_right():
        x = pantilthat.get_pan()
        if x - 20 < -90:
            x = -90
        else:
            x -= 20
        pantilthat.pan(x)

@app.route("/cam_up")
def cam_up():
        x = pantilthat.get_tilt()
        if x - 20 < -90:
            x = -90
        else:
            x -= 20
        pantilthat.tilt(x)

@app.route("/cam_down")
def cam_down():
        x = pantilthat.get_tilt()
        if x + 20 > 90:
            x = 90
        else:
            x += 20
        pantilthat.tilt(x)

@app.route("/cam_center")
def cam_center():
        pantilthat.pan(3)
        time.sleep(0.5)
        pantilthat.tilt(-5)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
