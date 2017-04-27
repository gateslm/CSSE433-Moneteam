# Python code to be the main server file

from flask import Flask, render_template, request

import connections
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

monetClient = connections.monetConn() # TODO: Add the connection info
redisClient = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379) # TODO: Add the connection info
app = Flask(__name__)


@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    print(request.form['username'])
    print(request.form['pwd'])
    return render_template('index.html');

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
     return '<html><head></head><body>admin</body></html>'




if __name__ == '__main__':
    app.run(host='0.0.0.0')
