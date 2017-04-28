# Python code to be the main server file

from flask import Flask, render_template, request, jsonify

import getEmpPWD
import employeefunctions
import connections
import hashlib
from pymongo import MongoClient
import gridfs
import pymonetdb
import redis
import json
from bson.objectid import ObjectId
import ast
import generate_schedule_html_table as GenSched
import numpy as np
import re
import pandas as pd


mongoClient = MongoClient('mongodb://localhost:27017/') # TODO: Add the connection info
mongoDB = mongoClient.moneteam
fs = gridfs.GridFS(mongoDB)

monetClient = connections.monetConn1() # TODO: Add the connection info FIXME: Need to fix this
redisClient = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379) # TODO: Add the connection info
app = Flask(__name__)


@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    pwd = request.form['pwd']
    result = getEmpPWD.getpassword(username, monetClient) # FIXME: Use different query
    result = result.replace("[","").replace("]","").replace("\"","").replace(" ","")
    print(result)
    inputPwd = getEmpPWD.getpasswordhash(pwd)
    print(inputPwd)
    if result == inputPwd:
        print("PWD match")
        return render_template("index.html")
    else:
        print("PWD don't match")
        return render_template('login_failed.html')

@app.route('/admin_login', methods=["POST"])
def login_admin():
    username = int(request.form['username'])
    pwd = request.form['pwd']
    
    if username % 2 ==1:
        query = "SELECT json.filter(password, \'password\') FROM employees1 WHERE empid = %d;" % username
        result = employeefunctions.executeEmpQueryCursor(query, username)
    else:
        query = "SELECT json.filter(password, \'password\') FROM employees2 WHERE empid = %d;" % username
        result = employeefunctions.executeEmpQueryCursor(query, username)
    # result = getEmpPWD.getpasswordhashmgr(username, monetClient) # FIXME: Use correct query
    # result = result.replace("[","").replace("]","").replace("\"","").replace(" ","")
    print(result)
    print(result[1])
    if len(result[1]) == 0:
        return render_template("login_failed_admin.html")
    print(type(result[1][0]))
    print(type(result[1][0][0]))
    result = result[1][0][0]
    result = result.replace("[","").replace("]","").replace("\"","").replace(" ","")
    inputPwd = getEmpPWD.getpasswordhash(pwd)
    print(inputPwd)
    if result == inputPwd:
        print("PWD match")
        return render_template("admin_settings_page.html", empid=username)
    else:
        print("PWD don't match")
        return render_template('login_failed_admin.html')

@app.route('/employee_settings')
def employee_settings_login():
    return render_template('login.html')

@app.route('/schedule_generator')
def schedule_generator():
     week_id = 1
     employee_name = "james"

    # opening_time = auto_scheduler.openning_time
    # closing_time = auto_scheduler.closing_time

     opening_time =8
     closing_time = 22

     schedule = GenSched.import_schedule(redisClient, employee_name,week_id, opening_time, closing_time)
     schedule = np.transpose(schedule)
     df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
     df.index = range(opening_time,closing_time)

     html_table = df.to_html()
     html_table = re.sub("False","",html_table)
     html_table = re.sub("True","&#10004",html_table)
     return html_table

@app.route('/employee_settings')
def employee_settings():
     return '<html><head></head><body>employee_settings</body></html>'

@app.route('/admin')
def admin():
     return render_template('login_admin.html')
     # return '<html><head></head><body>admin</body></html>'


@app.route('/admin_edit_page')
def admin_edit_age():
    return render_template('admin_edit.html')


@app.route('/admin_get_employee_wage/<int:empid>')
def getEmpWage(empid):
    query = "SELECT json.filter(workinfo, \'wage\') FROM employees "
    query += "WHERE empid = %d;" % int(empid)
    return employeefunctions.executeEmpQueryCursor(query, empid)

@app.route('/user_get_employee_preferences/<int:empid>')
def getemployeepreferences(empid):
    query = "SELECT preferences FROM employees "
    query += "WHERE empid = %d;" % int(empid)
    return employeefunctions.executeEmpQueryCursor(query, empid)

@app.route('/view_work_history/<int:empid>')
def view_work_history(empid):
    result = mongoDB.pastWork.find()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
