import numpy as np
import pandas as pd

from flask import Flask, render_template , request
from pandas import DataFrame
import os.path
from os import path
import json

app = Flask(__name__)

# HOME 
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('index.html')

#NEWS 
@app.route("/news", methods=['POST', 'GET'])
def news():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('news.html')

#People
@app.route("/people", methods=['POST', 'GET'])
def people():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('people.html')

#Alumni
@app.route("/alumni", methods=['POST', 'GET'])
def alumni():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('alumni.html')

#Papers
@app.route("/publications", methods=['POST', 'GET'])
def publications():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('publications.html')

#Projects
@app.route("/projects", methods=['POST', 'GET'])
def projects():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('projects.html')

#contact
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('contact.html')
        

if __name__ == "__main__":
    app.run(debug = True)