from flask import current_app, Flask, render_template, request
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg
import time
import sys
import threading
import os
import numpy as np

app = Flask("app")

@app.route('/', methods=['GET'])
def index():
    return refresh_page()

@app.route('/receive_message', methods=['POST'])
def receive_message():
    flag = list(request.form.keys())[0]
    state = request.form.get(flag)
    app.config[flag] = state
    return state


def refresh_page():
    with app.app_context():
        return render_template('index.html')

def start_server():
    app.config.update(
        ready = True,
        forward_pressed = "false",
        backward_pressed = "false",
        left_pressed = "false",
        right_pressed = "false",
    )
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

def get_ready():
    with app.app_context():
        config = app.config
        if('ready' not in config):
            return False
        else:
            return config['ready']

def get_left_message():
    with app.app_context():
        config = app.config
        if config['left_pressed'] == "true":
            return "left pressed"
        else:
            return ""

def get_right_message():
    with app.app_context():
        config = app.config
        if config['right_pressed'] == "true":
            return "right pressed"
        else:
            return ""

def get_forward_message():
    with app.app_context():
        config = app.config
        if config['forward_pressed'] == "true":
            return "forward pressed"
        else:
            return ""

def get_backward_message():
    with app.app_context():
        config = app.config
        if config['backward_pressed'] == "true":
            return "backward pressed"
        else:
            return ""

def shutdown_server():
    sys.exit(0)
