# Python code to be the main server file

from flask import Flask, render_template

import connections
from pymongo import MongoClient
import pymonetdb
import redis
import json
from bson.objectid import ObjectId
import ast
import generate_schedule_html_table.py


mongoClient = MongoClient() # TODO: Add the connection info
monetClient = connections.monetConn() # TODO: Add the connection info
redisClient = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379) # TODO: Add the connection info
app = Flask(__name__)


@app.route('/')
def index():
     return render_template('index.html')

@app.route('/schedule_generator')
def schedule_generator():
     week_id = 1
     employee_name = "james"

    # opening_time = auto_scheduler.openning_time
    # closing_time = auto_scheduler.closing_time

     opening_time =8
     closing_time = 22

     schedule = import_schedule(employee_name,week_id)
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
