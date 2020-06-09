import os
import logging
import socket
from flask import Flask, jsonify, request

import json
from distilbert import run_prediction

HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())

log = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'host_name': HOST_NAME,
        'app_name': APP_NAME,
        'ip': IP,
        'port': PORT,
        'home_dir': HOME_DIR,
        'host': socket.gethostname()
    })

@app.route("/qa/ask", methods=['POST'])
def ask():
    data = request.get_json()
    print(data)
    question = data['question']
    context = data['context']

    predictions = run_prediction([question], context)
    return predictions

@app.route("/test", methods=['GET','POST'])
def run_test():
    context = "New Zealand (Māori: Aotearoa) is a sovereign island country in the southwestern Pacific Ocean. It has a total land area of 268,000 square kilometres (103,500 sq mi), and a population of 4.9 million. New Zealand's capital city is Wellington, and its most populous city is Auckland."
    question = "What's the largest city?"

    predictions = run_prediction([question], context)
    return predictions

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
