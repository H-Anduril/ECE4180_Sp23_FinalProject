from flask import current_app, Flask, render_template, Response, request
import time
import sys
import threading
import os
from flask_socketio import SocketIO, emit
import numpy as np
import cv2
from webcamvideostream import WebcamVideoStream

app = Flask("app")

@app.route('/', methods=['GET'])
def index():
    return refresh_page()


def gen():
    video_camera = WebcamVideoStream()
    if video_camera == None:
        video_camera = WebcamVideoStream()
    while True:
#         if camera.stopped:
#             break
#         frame = camera.read()
        frame = video_camera.get_frame()
        if frame is not None:
#             ret, jpeg = cv2.imencode('.jpg',frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #else:
            # print("frame is none")

@app.route('/video_feed')
def video_feed():
    print("check")
#     return Response(gen(WebcamVideoStream().start()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def refresh_page():
    with app.app_context():
        return render_template('camera.html')

def start_server():
    app.config.update(
        armed = True,
        ready = True,
    )
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

def get_ready():
    with app.app_context():
        config = app.config
        if('ready' not in config):
            return False
        else:
            return config['ready']

def shutdown_server():
    sys.exit(0)
