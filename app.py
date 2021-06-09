import numpy as np
import pandas as pd
import csv

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
        with open(app.root_path + '/data/Home_news.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            news = []
            for row in data : 
                news.append(row)
        
        with open(app.root_path + '/data/Home_Slider.csv') as csvFile:
            data2 = csv.reader(csvFile, delimiter='|')
            next(data2)
            sliderImageList = []
            for row2 in data2 : 
                sliderImageList.append(row2)
        #print(sliderImageList)
        return render_template('index.html', news=news,sliderImageList=sliderImageList)

#NEWS 
@app.route("/news", methods=['POST', 'GET'])
def news():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        with open(app.root_path + '/data/news.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            next(data)
            news = []
            i = 1
            for row in data : 
                row.append(i)
                news.append(row)
                i = i + 1
        return render_template('news.html', news=news)


#NEWS DETAILS   
@app.route("/newsDetails/<int:newsId>", methods=['POST', 'GET'])
def newsDetails(newsId):
    if request.method == 'POST':
        return "This is index post method!"
    else:
        print(newsId)
        with open(app.root_path + '/data/news.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            next(data)
            news = []
            i = 1
            for row in data : 
                if i == newsId : 
                    news.append(row)
                i = i + 1
            print(news)
        return render_template('newsDetails.html', news=news)


#People
@app.route("/people", methods=['POST', 'GET'])
def people():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        with open(app.root_path + '/data/PhdStudents.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            next(data)
            phdList = []
            for row in data : 
                phdList.append(row)
        print(phdList)
        return render_template('people.html',phdList=phdList)

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
        with open(app.root_path + '/data/papers.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            next(data)
            papersList = []
            for row in data : 
                papersList.append(row)
        #print(papersList)
        return render_template('publications.html',papersList=papersList)

#Projects
@app.route("/projects", methods=['POST', 'GET'])
def projects():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        
        with open(app.root_path + '/data/projects.csv') as csvFile:
            data = csv.reader(csvFile, delimiter='|')
            next(data)
            projectList = []
            for row in data : 
                projectList.append(row)
        return render_template('projects.html',projectList=projectList)

#contact
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('contact.html')
        
@app.route("/sliderDemo", methods=['POST', 'GET'])
def sliderDemo():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('sliderDemo.html')
if __name__ == "__main__":
    app.run(debug = True)