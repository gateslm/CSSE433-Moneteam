# Python code to be the main server file

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory

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

# https://flask-pymongo.readthedocs.io/en/latest/

mongoDB = connections.mongoConn() # Gives us the collection moneteam
fs = gridfs.GridFS(mongoDB)

#monetClient = connections.monetConn1() # TODO: Add the connection info FIXME: Need to fix this
redisClient = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379) # TODO: Add the connection info
app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'jpg', 'jpeg', 'gif', 'png'])

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    username = int(request.form['username'])
    pwd = request.form['pwd']
    result = employeefunctions.checkIfPwdsMatch(username,pwd)
    if result:
        print("PWD match")
        return render_template("employee_homepage.html", empid=username, message="")
    else:
        print("PWD don't match")
        return render_template('login_failed.html')

@app.route('/employee_homepage', methods=["POST"])
def go_to_employee_homepage():
    empid= request.form['empID']
    return render_template("employee_homepage.html", empid=empid, message="")


@app.route('/upload_resume_page', methods=["POST"])
def upload_resume_page():

    empid = request.form['empID']

    return render_template("resume_upload.html", empid=empid)

@app.route('/add_employee', methods=["POST"])
def add_employee():
    adminID = int(request.form['adminID'])
    empid = int(request.form['employeeID'])
    pwd = request.form['password']
    name = request.form['Name']
    address = request.form['address']
    city = request.form['city']
    bankName = request.form['bankName']
    bankAccountNum = int(request.form['accountNumber'])
    print("accountum")
    position = "bartender"
    wage = 7.00
    if(request.form.get('manager')):
        position = "manager"
        wage = 14.00
    result = employeefunctions.insertEmp(empid, name, pwd, address, city, position, wage, bankAccountNum, bankName)
    print("inserted !!!")
    if (result > 0):
        return render_template("admin_settings_page.html", empid=adminID, message ="Added new employee successfully.")
    else:
        return render_template("admin_settings_page.html", empid=adminID, message="Unable to add new employee.")

@app.route('/edit_employee', methods=["POST"])
def edit_employee():
    # Larry, could this be like the edit book page?
    #  I would like to have a drop down of each json column to change the specific information in that area, then have that saved.
    empid = int(request.form['employeeID'])
    #pwd = request.form['password']
    attr = request.form['attribute']
    newval = int(request.form['newval'])
    print("accountum")
    result = employeefunctions.updateEmp(empid, pwd, attr, newVal)
    print("inserted !!!")
    if (result > 0):
        return render_template("admin_settings_page.html", empid=adminID, message ="Edited information successfully.")
    else:
        return render_template("admin_settings_page.html", empid=adminID, message="Unable to change information.")


@app.route('/admin_login', methods=["POST"])
def login_admin():
    username = int(request.form['username'])
    pwd = request.form['pwd']

    '''

    # query = SELECT json.filter(password, password) FROM employees1 WHERE empid = %d;
    query = employeefunctions.changeQueryTable(query,username)
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
        return render_template("admin_settings_page.html", empid=username, message="")
    else:
        print("PWD don't match")
        return render_template('login_failed_admin.html')
    '''

    managerpwds = employeefunctions.getManagerPwds()
    givenpwdhashed = employeefunctions.getPwdHash(pwd)
    print(managerpwds, type(managerpwds[0]))
    print(givenpwdhashed, type(givenpwdhashed))
    if givenpwdhashed in managerpwds:
        print("PWD match")
        return render_template("admin_settings_page.html", empid=username, message="")
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

@app.route('/add_employee_page', methods=["POST"])
def add_employee_page():
    adminID = request.form['adminID']
    return render_template("add_employee.html", empid=adminID)

@app.route('/edit_employee_page', methods=["POST"])
def edit_employee_page():
    empID = request.form['empID']
    return render_template("edit_employee.html", empid=empID)

@app.route('/admin')
def admin():
     return render_template('login_admin.html')
     # return '<html><head></head><body>admin</body></html>'


@app.route('/admin_edit_page')
def admin_edit_age():
    return render_template('admin_edit.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python
@app.route('/upload_resume', methods=["POST"])
def upload():
    print("IN FUNCTION")
    if 'file' not in request.files:
        print("No file part")
    ff = request.files['file']
    empid = request.form['empid']
    print("After empid")
    if ff and allowed_file(ff.filename):
        print("IN if statement")
        result = fs.put(ff)
        mongoDB.fs.files.update({"_id":ObjectId(result)},{'$set':{'empid':int(empid)}})
        mongoDB.fs.files.update({"_id":ObjectId(result)},{'$set':{'filename':ff.filename}})
        print(result)
        return render_template("employee_homepage.html", empid=empid, message="ID returned")
    return render_template("employee_homepage.html", empid=empid, message="Did not upload file")

@app.route('/get_document_list/<string:emp>')
def get_document_list(emp):
    empid = int(emp)
    result = mongoDB.fs.files.find({"empid":empid})
    print(result)
    ls = []
    for r in result:
        print(r)
        ls.append([r['empid'], str(r['_id']), r['filename']])
    return json.dumps({"res":ls})

@app.route('/view_documents', methods=["POST"])
def view_documents():
    empid = int(request.form['empID'])
    return render_template("document.html", empid=empid)

@app.route('/get_a_document', methods=["POST"])
def get_a_document():
	objId = request.form['ObjectID']
	f = mongoDB.fs.files.find({"_id": ObjectId(objId)})
	return f



@app.route('/change_preferences/<string:emp>')
def make_change_preference_page(emp):
    print("here make change pref page")
    empid = int(emp)
    prefs = employeefunctions.getEmpsPrefs(empid)
    print("return from get prefs call")
    print(prefs)
    return jsonify(prefs)



@app.route('/change_preferences_page', methods=["POST"])
def change_preferences_page():
    print("here change pref page")
    empid = int(request.form['empID'])
    return render_template("change_preferences.html", empid=empid, message="Hope this works")




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
