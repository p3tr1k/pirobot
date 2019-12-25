#/usr/bin/env python
from flask import Flask, render_template, Response
from camera import Camera
import time

import RPi.GPIO as GPIO

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

#@app.route("/")
#def index():
#    return render_template('index.html')

def gen(camera):
    while True:
        frame =  camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def json():
    return render_template('json.html')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

###
@app.route('/dopredu')
def dopredu():
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
###
@app.route("/<action>")
def  action(action):
    if action  == "forward":
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
    if action == "reverse":
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)
    if action == "left":
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

    if action == "right":
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

    if action == "stop":
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

#    patStat = GPIO.input(5)
#    sestStat = GPIO.input(6)
#    trinastStat = GPIO.input(13)
#    devatnastStat = GPIO.input(19)

#    templateData = {
#        "jedna" : jednaStat
#    }
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
