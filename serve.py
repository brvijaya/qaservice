"""
Simple flask server for the interface
"""

import os
import json

from flask import Flask, request, redirect, url_for
from flask import render_template
from distilbert import run_prediction

# -----------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello():
    return("Hello from qa service!")

@app.route("/qa/ask", methods=['POST'])
def ask():
    data = request.get_json()
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
    app.run()