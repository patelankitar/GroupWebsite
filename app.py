import pyodbc
import numpy as np
import pandas as pd
import time
import geopandas
import redis
import hashlib
from flask import Flask, render_template , request
import datetime
import matplotlib.pyplot as plt
import random
from pandas import DataFrame
import pickle
from sklearn.cluster import KMeans
import os.path
from os import path
import seaborn as sns
from random import randrange
import matplotlib
import json
matplotlib.use('Agg')


app = Flask(__name__)


# Configure Database URI: 
server = '6331assign1.database.windows.net'
database = '6331assignment1'
username = 'sqladmin'
password = 'Serveradmin1234'   
driver= '{ODBC Driver 17 for SQL Server}'

#setup db connection to sql server
def init_db():
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    return cursor

cursor = init_db()

# home route
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return "This is index post method!"
    else:
        return render_template('index.html')

@app.route("/q1", methods=['POST', 'GET'])
def q1():
    if request.method == 'POST':
        col1Value  = request.form['col1']
        col2Value  = request.form['col2']  
        errormessage = ""

        if (col1Value == "" or col2Value == ""):
            errormessage = "Please enter valid input"
            return render_template('q1.html',errorMessage=errormessage)
        else:
            #sql = "SELECT party_detailed,  sum(candidatevotes) FROM [dbo].[presidentialelect] where year = "+ col1Value +" and state_po = '"+ col2Value +"'  group by party_detailed"
            sql = "SELECT  top 6 party_detailed , ROUND(CAST((candidatevotes * 100.0 / totalVotes) AS FLOAT), 2) AS Percentage1   FROM [dbo].[presidentialelect] where year = " + col1Value + " and state_po = '" + col2Value +"' ORDER BY Percentage1 desc "
            cursor.execute(sql)
            
            df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))

            if(len(df) <= 0):
                errormessage = "No results found"
                return render_template('q1.html',errorMessage=errormessage)
            else:
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]

                # print (json.dumps(d))
                
                xAxisLabel = "Candidate"
                yAxisLabel = "# of Votes"
                chartLabel = "% Votes for each party"
        
                chartType = request.form['chartSelect']
                print(chartType)
                #if(chartType=="pi"):

                return render_template('piChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
    else:
        return render_template('q1.html')


@app.route("/q2", methods=['POST', 'GET'])
def q2():
    if request.method == 'POST':
        yearStartValue  = request.form['yearStart']
        yearEndValue  = request.form['yearEnd']  
        stateValue  = request.form['state']  
        
        errormessage = ""

        if (yearStartValue == "" or yearEndValue == "" or stateValue==""):
            errormessage = "Please enter valid input"
            return render_template('q2.html',errorMessage=errormessage)
        else:
            sql = "SELECT distinct CONVERT(varchar(10), [year]), totalVotes FROM [dbo].[presidentialelect]  where year >= " + yearStartValue + " and year <=  " + yearEndValue + " AND state_po in ('"+stateValue+"')"
            cursor.execute(sql)
            
            df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))

            if(len(df) <= 0):
                errormessage = "No results found"
                return render_template('q2.html',errorMessage=errormessage)
            else:
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]

                #print (json.dumps(d))
                
                xAxisLabel = "Year"
                yAxisLabel = "Total Votes"
                chartLabel = "Total Votes per Year"
        
                #chartType = request.form['chartSelect']
                #print(chartType)
                #if(chartType=="pi"):

                return render_template('scatterChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
    else:
        return render_template('q2.html')


@app.route("/q3", methods=['POST', 'GET'])
def q3():
    if request.method == 'POST':
        yearStartValue  = request.form['yearStart']
        yearEndValue  = request.form['yearEnd']  
        stateValue  = request.form['state'] 

        errormessage = ""

        if (yearStartValue == "" or yearEndValue == "" or stateValue==""):
            errormessage = "Please enter valid input"
            return render_template('q3.html',errorMessage=errormessage)
        else:
            sql = "SELECT candidate, CONVERT(varchar(10), [year])  FROM [dbo].[presidentialelect]  where year >= " + yearStartValue + " and year <=  " + yearEndValue + " AND state_po in ('"+stateValue+"') GROUP BY candidate,Year"
            cursor.execute(sql)
            
            df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))

            if(len(df) <= 0):
                errormessage = "No results found"
                return render_template('q3.html',errorMessage=errormessage)
            else:
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]

                # print (json.dumps(d))
                
                xAxisLabel = "Year"
                yAxisLabel = "Candidate"
                chartLabel = "Candidate per Year"
        
                #chartType = request.form['chartSelect']
                #print(chartType)
                #if(chartType=="pi"):

                return render_template('hBarChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
    else:
        return render_template('q3.html')


@app.route("/q4", methods=['POST', 'GET'])
def q4():
    if request.method == 'POST':
        col1Value  = request.form['col1']
        col2Value  = request.form['col2']  
        errormessage = ""

        if (col1Value == "" or col2Value == ""):
            errormessage = "Please enter valid input"
            return render_template('q4.html',errorMessage=errormessage)
        else:
            sql = "SELECT party_detailed,  sum(candidatevotes) FROM [dbo].[presidentialelect] where year = "+ col1Value +" and state_po = '"+ col2Value +"'  group by party_detailed"
            cursor.execute(sql)
            
            df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))

            if(len(df) <= 0):
                errormessage = "No results found"
                return render_template('q4.html',errorMessage=errormessage)
            else:
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]

                # print (json.dumps(d))
                
                xAxisLabel = "Candidate"
                yAxisLabel = "# of Votes"
                chartLabel = "Number of Votes per Candidate"
        
                #chartType = request.form['chartSelect']
                #print(chartType)
                #if(chartType=="pi"):

                return render_template('barChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
    else:
        return render_template('q4.html')


@app.route("/q5", methods=['POST', 'GET'])
def q5():
    if request.method == 'POST':
        col1Value  = request.form['col1']
        col2Value  = request.form['col2']  
        errormessage = ""

        if (col1Value == "" or col2Value == ""):
            errormessage = "Please enter valid input"
            return render_template('q5.html',errorMessage=errormessage)
        else:
            sql = "SELECT  party_simplified,  ROUND(CAST((sum(candidatevotes) * 100.0 / totalVotes) AS FLOAT), 2) AS [Percentage] FROM [dbo].[presidentialelect] WHERE year = " + col1Value + " AND state_po in ('" + col2Value + "') GROUP by party_simplified ,totalVotes"
            cursor.execute(sql)
            
            df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))

            if(len(df) <= 0):
                errormessage = "No results found"
                return render_template('q5.html',errorMessage=errormessage)
            else:
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]

                # print (json.dumps(d))
                
                xAxisLabel = "Candidate"
                yAxisLabel = "# of Votes"
                chartLabel = "Number of Votes per Candidate"
        
                #chartType = request.form['chartSelect']
                #print(chartType)
                #if(chartType=="pi"):
                
                return render_template('piChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
    else:
        return render_template('q5.html')


@app.route("/barChart", methods=['POST', 'GET'])
def barChart():
        # cursor.execute("select locationSource, count(mag) as mag_count  from [dbo].[earthquakeMonthData] where mag > 4.1 and mag < 4.3 group by locationSource ")
        # df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
        # d = [
        #     dict([
        #         (colname, row[i])
        #         for i,colname in enumerate(df.columns)
        #     ])
        #     for row in df.values
        # ]
        # print (json.dumps(d))

        #d= [{"x": "ak", "y": 2}, {"x": "nc", "y": 1}, {"x": "ok", "y": 1}, {"x": "pr", "y": 1}, {"x": "us", "y": 90}]
        # d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
        # xAxisLabel = "Magnitude"
        # yAxisLabel = "# of earthquake"
        # chartLabel = "I changed this text to Test"
        # return render_template('barChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
        return render_template('barChart.html')

@app.route("/hBarChart", methods=['POST', 'GET'])
def hBarChart():
        # cursor.execute("select locationSource, count(mag) as mag_count  from [dbo].[earthquakeMonthData] where mag > 4.1 and mag < 4.3 group by locationSource ")
        # df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
        # d = [
        #     dict([
        #         (colname, row[i])
        #         for i,colname in enumerate(df.columns)
        #     ])
        #     for row in df.values
        # ]
        # print (json.dumps(d))

        # d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
        # xAxisLabel = "Number of earthquake"
        # yAxisLabel = "Magnitude"
        # chartLabel = "Number of Earthquake for magnitude"
        # return render_template('hBarChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
        return render_template('hBarChart.html')
  

@app.route("/piChart", methods=['POST', 'GET'])
def piChart():
        # cursor.execute("select mag, count(mag) as mag_count  from [dbo].[earthquakeMonthData] where mag > 4.1 and mag < 4.5 group by mag ")
        # df = pd.DataFrame.from_records(cursor.fetchall(), columns = [desc[0] for desc in cursor.description])
        # good_columns = np.array(df[['mag','mag_count']])
        
        # dict_data = {}

        # for i in range(len(good_columns)):
        #     dict_data[good_columns[i][0]] = good_columns[i][1]
        
        # print(dict_data)
        # chart_data = dict_data
        
        #chartLabel = "Number of Earthquake for magnitude"
        
        #chart_data = {4.18: 100.0, 4.2: 94.0, 4.3: 106.0, 4.34: 102.0}
        #return render_template("piChart.html", graphData = chart_data, chartLabel=json.dumps(chartLabel))

        #d= [{"x": "AL", "y": "46"}, {"x": "OK", "y": "10"}, {"x": "TX", "y": "70"}, {"x": "PA", "y": "50"}]
        #return render_template('piChart.html', graphData = (json.dumps(d)),chartLabel=json.dumps(chartLabel))
        return render_template('piChart.html')
        
@app.route("/lineChart", methods=['POST', 'GET'])
def lineChart():
        # cursor.execute("select mag, count(mag) as mag_count  from [dbo].[earthquakeMonthData] where mag > 4.0 and mag < 5.0 group by mag ")
        # df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
        # d = [
        #     dict([
        #         (colname, row[i])
        #         for i,colname in enumerate(df.columns)
        #     ])
        #     for row in df.values
        # ]
        # print (json.dumps(d))

        # d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
        # xAxisLabel = "Magnitude"
        # yAxisLabel = "# of earthquake"
        # chartLabel = "Number of Earthquake for magnitude"
        # return render_template('lineChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
        return render_template('lineChart.html')

@app.route("/scatterChart", methods=['POST', 'GET'])
def scatterChart():
        # cursor.execute("select mag, count(mag) as mag_count  from [dbo].[earthquakeMonthData] where mag > 4.0 and mag < 5.0 group by mag ")
        # df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
        # d = [
        #     dict([
        #         (colname, row[i])
        #         for i,colname in enumerate(df.columns)
        #     ])
        #     for row in df.values
        # ]
        # print (json.dumps(d))

        # d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
        # xAxisLabel = "Magnitude"
        # yAxisLabel = "# of earthquake"
        # chartLabel = "Number of Earthquake for magnitude"
        # return render_template('scatterChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))
        return render_template('scatterChart.html')


# Get Filter criteria 
@app.route("/filter_criteria", methods=['POST', 'GET'])
def filter_criteria():
    if request.method == 'POST':
        message = ""
        data = ""
        whereQuery = ""
        selectQuery = ""
        errorMessage=""
        sqlQuery = " "
        magnitudeCheckbox = request.form.get('magnitudeCheckbox')
        daysCheckbox = request.form.get('daysCheckbox')
        distanceCheckbox = request.form.get('distanceCheckbox')
        timeCheckbox = request.form.get('timeCheckbox')
        dateCheckbox = request.form.get('dateCheckbox')
        weekDayCheckbox = request.form.get('weekDayCheckbox')

        # Check if Magnitude value is selected for filter criteria
        if magnitudeCheckbox:
            selectValue = request.form['magnitudeRelationSelect']

            if selectValue == "between":
                fromValue = request.form['magFromText']
                toValue = request.form['magToText']  
                if (fromValue =="") or (toValue ==""):
                    errorMessage = "please enter magnitute values"
                   
                elif (fromValue > toValue):
                    whereQuery = "WHERE " + " mag <=" + fromValue + " AND mag >= " + toValue
                else: 
                    whereQuery = "WHERE " + " mag <=" + toValue + " AND mag >= "+ fromValue
            else:
                value = request.form['magnitudeValueTextbox']
                if(value==""):
                    errorMessage = "please enter magnitute value"
                    
                else:
                    whereQuery = "WHERE " + " mag " + selectValue + " "+ value 

        # check if days value selected for filter criteria
        if daysCheckbox:
            daysValue = request.form['daysTextbox']
            daysSelect = request.form['daysSelect']
            if (daysValue==""):
                errorMessage = "please enter "+ daysValue +" value"
            else:
                if(daysSelect == "days"):
                    if(whereQuery==""):
                        whereQuery = "WHERE " + "[time] < GETDATE() - " + daysValue
                    else: 
                        whereQuery = whereQuery + " AND " + "[time] < GETDATE() - " + daysValue
                elif(daysSelect == "weeks"):
                    if(whereQuery==""):
                        whereQuery = "WHERE " + "[time] < GETDATE() - " + (daysValue * 7)
                    else: 
                        whereQuery = whereQuery + " AND " + "[time] < GETDATE() - " + (daysValue* 7)
                else:
                    if(whereQuery==""):
                        whereQuery = "WHERE " + "[time] < GETDATE() - " + (daysValue * 30)
                    else:
                        whereQuery = whereQuery + " AND " + "[time] < GETDATE() - " + (daysValue* 30)
        
        # Check If the Date range selected for Filter criteria
        if dateCheckbox:
            startDateValue = request.form['startDateText']
            endDateValue = request.form['endDateText']

            if(startDateValue=="" or endDateValue==""):
                errorMessage = "please enter date value"
            else:
                if(whereQuery == ""):
                    whereQuery =  "WHERE " + " where CONVERT(datetime,[time]) > '"+ startDateValue + " 00:00:00' AND CONVERT(datetime,[time]) < '"+ endDateValue + " 23:59:59'"
                else:
                    whereQuery = whereQuery + " AND " + " where CONVERT(datetime,[time]) > '"+ startDateValue + " 00:00:00' AND CONVERT(datetime,[time]) < '"+ endDateValue + " 23:59:59'"
        
        # Check If the Time SLot selected for Filter criteria
        if timeCheckbox:
            startTimeText = request.form['startTimeText']
            endTimeText = request.form['endTimeText']
            m1 = datetime.strptime(startTimeText, '%H:%M:%S')
            m2 = datetime.strptime(endTimeText, '%H:%M:%S')
            #print(m1)
            #print(m2)
            
            if(m1>m2):
                print("TRUE")
            else:
                print("FALSE")

            if(startTimeText=="" or endTimeText==""):
                errorMessage = "please enter time value"
            else:
                if(whereQuery == ""):
                    whereQuery =  "WHERE " + " convert(varchar(15), CAST([time] AS smalldatetime), 108) >= '" + startTimeText +"' AND convert(varchar(15), CAST([time] AS smalldatetime), 108) <= '"+ endTimeText + "'"
                else:
                    whereQuery = whereQuery + " AND " + " convert(varchar(15), CAST([time] AS smalldatetime), 108) >= '" + startTimeText +"' AND convert(varchar(15), CAST([time] AS smalldatetime), 108) <= '"+ endTimeText + "'"

        # Check if Distance selected for filter criteria 
        if distanceCheckbox:
            distanceValue = request.form['distanceTextbox']

            if(distanceValue==""):
                errorMessage = "please enter distance value"
            else:
                sourceType = request.form['sourceLocationTypeSelect']
                zipcode = request.form['zipCodeTextBox']
                distanceMeasureValue = request.form['distanceMeasureSelect']
                distanceRelationValue = request.form['distanceRelationSelect']
                latitudeValue = ""
                longitudeValue = ""

                if(sourceType=="zip"):
                    if(zipcode==""):
                        errorMessage = "please enter Zipcode value"
                    else:
                        df = geopandas.tools.geocode(zipcode)
                        
                        df['lon'] = df['geometry'].x
                        df['lat'] = df['geometry'].y
                        
                        latitudeValue = str(df['lon'].values[0])
                        longitudeValue  = str(df['lat'].values[0])
                        
                elif(sourceType=="latitude"):
                    latitudeValue = request.form['latitudeTextBox']
                    longitudeValue = request.form['longitudeTextBox']

                    if(latitudeValue=="" or longitudeValue==""):
                        errorMessage = "please enter latitude / longitude value"
                else:
                    errorMessage = "please enter Zipcode or  latitude / longitude value"

                if(distanceMeasureValue=="miles"):
                    selectQuery = "SELECT CAST([time] AS smalldatetime) AS Occured,* FROM (SELECT (3959 * acos (cos(radians("+latitudeValue+"))*cos(radians(latitude))*cos(radians(longitude)-radians("+longitudeValue+"))+ sin(radians("+latitudeValue+")) * sin(radians(latitude)))) AS distance,* FROM earthquakeMonthData) t"
                elif(distanceMeasureValue=="km"):
                    selectQuery = "SELECT CAST([time] AS smalldatetime) AS Occured,* FROM (SELECT (6371 * acos (cos(radians("+latitudeValue+"))*cos(radians(latitude))*cos(radians(longitude)-radians("+longitudeValue+"))+ sin(radians("+latitudeValue+")) * sin(radians(latitude)))) AS distance,* FROM earthquakeMonthData) t"
                else:
                    errorMessage = "please select distance measure"

                if(whereQuery==""):
                    whereQuery = "WHERE " + " t.distance " + distanceRelationValue +" "+ distanceValue
                else:
                    whereQuery = whereQuery + " AND " + " t.distance " + distanceRelationValue +" " + distanceValue

        # Check if specific days of the week are selected for filter criteria 
        if weekDayCheckbox:
            sunday = request.form.get('sunday')
            monday = request.form.get('monday') 
            tuesday = request.form.get('tuesday') 
            wednesday = request.form.get('wednesday') 
            thrusday = request.form.get('thrusday') 
            friday = request.form.get('friday') 
            saturday = request.form.get('saturday') 

            if(sunday or tuesday or monday or wednesday or thrusday or friday or saturday):
                if sunday:
                    if (whereQuery == ""):
                        whereQuery = "WHERE " + " DATEPART(dw,[time]) = 1 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 1"
                
                if monday:
                    if (whereQuery == ""):
                            whereQuery = "WHERE " + " DATEPART(dw,[time]) = 2 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 2"
                
                if tuesday:
                    if (whereQuery == ""):
                        whereQuery = "WHERE " + " DATEPART(dw,[time]) = 3 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 3"
                
                if wednesday:
                    if (whereQuery == ""):
                            whereQuery = "WHERE " + " DATEPART(dw,[time]) = 4 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 4"
                
                if thrusday:
                    if (whereQuery == ""):
                            whereQuery = "WHERE " + " DATEPART(dw,[time]) = 5 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 5"
                
                if friday:
                    if(whereQuery == ""):
                            whereQuery = "WHERE " + " DATEPART(dw,[time]) = 6 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 6"
                
                if saturday:
                    if(whereQuery == ""):
                            whereQuery = "WHERE " + " DATEPART(dw,[time]) = 7 "
                    else:
                        whereQuery = whereQuery + " AND " + " DATEPART(dw,[time]) = 7"
            else :
                errorMessage = "Please select at least 1 day of the week to filter"
            
        # # sort criteria 
        # sortCoulmnValue =  request.form['sortSelect']
        # sortOrderValue = request.form['sortOrderSelect']

        # orderbyQuery = "ORDER BY " + sortCoulmnValue + " " + sortOrderValue 

        xAxisValue = request.form['xSelect']
        yAxisValue = request.form['ySelect']

        print(xAxisValue)
        print(yAxisValue)
     
        chartType = request.form['chartSelect']
           

        # if No error in input for filter criteria - Build Query and display results 
        if(errorMessage==""):
            if(selectQuery==""):
                selectQuery = "SELECT CAST([time] AS smalldatetime) AS Occured,*  FROM [dbo].[earthquakeMonthData] "

            #sqlQuery =  selectQuery + " "+ whereQuery +" "+ orderbyQuery
            sqlQuery =  selectQuery + " "+ whereQuery 

            print(chartType)
            if(chartType=="pi"):
                cursor.execute(sqlQuery)
                df = pd.DataFrame.from_records(cursor.fetchall(), columns = [desc[0] for desc in cursor.description])
                good_columns = np.array(df[['mag','mag_count']])
                
                dict_data = {}

                for i in range(len(good_columns)):
                    dict_data[good_columns[i][0]] = good_columns[i][1]
                
                # print(dict_data)
                chart_data = dict_data
                
                #chart_data = {4.18: 1.0, 4.2: 94.0, 4.3: 106.0, 4.34: 1.0, 4.38: 1.0, 4.39: 1.0, 4.4: 120.0}
                
                chartLabel = "Number of Earthquake for magnitude"
                
                return render_template("piChart.html", graphData = chart_data, chartLabel=json.dumps(chartLabel))
            
            elif(chartType=="line"):
                cursor.execute(sqlQuery)
                df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]
                # print (json.dumps(d))

                #d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
                
                xAxisLabel = "Magnitude"
                yAxisLabel = "# of earthquake"
                chartLabel = "Number of Earthquake for magnitude"
                return render_template('lineChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))

            elif(chartType=="hBar"):
                cursor.execute(sqlQuery)
                df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]
                # print (json.dumps(d))

                #d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
                
                xAxisLabel = "Magnitude"
                yAxisLabel = "# of earthquake"
                chartLabel = "Number of Earthquake for magnitude"
                return render_template('barChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))

            elif(chartType=="vBar"):
                cursor.execute(sqlQuery)
                df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]
                # print (json.dumps(d))

                #d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
                
                xAxisLabel = "Magnitude"
                yAxisLabel = "# of earthquake"
                chartLabel = "Number of Earthquake for magnitude"
                return render_template('barChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))

            elif(chartType=="point"):
                cursor.execute(sqlQuery)
                df = pd.DataFrame.from_records(cursor.fetchall(), columns =list('xy'))
                d = [
                    dict([
                        (colname, row[i])
                        for i,colname in enumerate(df.columns)
                    ])
                    for row in df.values
                ]
                # print (json.dumps(d))

                #d= [{"x": 4.18, "y": 1.0}, {"x": 4.2, "y": 2.0}, {"x": 4.3, "y": 3.0}, {"x": 4.32, "y": 3.0}, {"x": 4.34, "y": 1.0}, {"x": 4.38, "y": 5.0}, {"x": 4.39, "y": 1.0}, {"x": 4.4, "y": 10.0}, {"x": 4.5, "y": 8.0}, {"x": 4.6, "y": 7.0}, {"x": 4.7, "y": 3.0}, {"x": 4.8, "y": 7.0}, {"x": 4.9, "y": 6.0}, {"x": 4.99, "y": 1.0}]
                
                xAxisLabel = "Magnitude"
                yAxisLabel = "# of earthquake"
                chartLabel = "Number of Earthquake for magnitude"
                return render_template('scatterChart.html', graphData = (json.dumps(d)), xAxisLabel=json.dumps(xAxisLabel),yAxisLabel=json.dumps(yAxisLabel),chartLabel=json.dumps(chartLabel))


            else:
                return render_template('filter_criteria.html', errorMessage=errorMessage)
        else: 
            return render_template('filter_criteria.html', errorMessage=errorMessage)
    else:
        message = "The is GET method"
        return render_template('filter_criteria.html', message=message)

if __name__ == "__main__":
    app.run(debug = True)