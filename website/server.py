# Python code to be the main server file

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory, make_response

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
from scheduler import generate_schedule_html_table as GenSched
from scheduler import redis_connect
from scheduler import parameters
import numpy as np
import re
import pandas as pd

# https://flask-pymongo.readthedocs.io/en/latest/

mongoDB = connections.mongoConn() # Gives us the collection moneteam
fs = gridfs.GridFS(mongoDB)

#monetClient = connections.monetConn1() # TODO: Add the connection info FIXME: Need to fix this
redisClient = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379) # TODO: Add the connection info
app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['pdf'])

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

@app.route('/admin_homepage', methods=["POST"])
def go_to_admin_homepage():
    empid=request.form['adminID']

    return render_template("admin_settings_page.html", empid=empid, message="")


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

@app.route('/edit_employee_submit', methods=["POST"])
def edit_employee_info():
    empID = int(request.form['empID'])
    name = request.form['Name']
    addr = request.form['address']
    city = request.form['city']
    bank_name = request.form['bankName']
    bank_acct_num = request.form['accountNumber']

    # TODO:Update infomation
    res = employeefunctions.changeEmpInfo(empID,name,addr,city,bank_name,bank_acct_num)

    print(res)

    return render_template("employee_homepage.html", empid=empID, message=res)

@app.route('/load_change_password_page', methods=["POST"])
def load_change_password_page():
    empID = request.form['empID']
    return render_template("edit_password.html", empid=empID)

@app.route('/change_password', methods=["POST"])
def change_password():
    empID = int(request.form['empID'])
    oldpass = request.form['orgPassword']
    newpass = request.form['newPassword']
    newpass2 = request.form['newPasswordCheck']
    res = employeefunctions.changePassword(empID,oldpass,newpass)
    return render_template("employee_homepage.html", empid=empID, message=res)

@app.route('/load_employee_edit_page', methods=["POST"])
def load_employee_edit_page():
    empid = int(request.form['empID'])

    # TODO:Run Query
    query = "select name, json.filter(address, \'street\') as street, "
    query += "json.filter(address, \'city\') as city, "
    query += "json.filter(paymentinfo, \'bankname\') as bankname, "
    query += "json.filter(paymentinfo, \'banknum\') as banknum from employees "
    query += "where empid = %d;" % empid

    res = employeefunctions.executeEmpQueryCursorAll(query)
    print(res)
    print(type(res[1][0]))
    res = res[1][0]

    #empName = "JOHN SMITH"
    #empAddr = "WHERE AM I"
    #empCity = "NOT REAL"
    #empBankName = "FIXME"
    #empBankNum = "-1"
    empName = res[0]
    empAddr = res[1][2:-2]
    empCity = res[2][2:-2]
    empBankName = res[3][2:-2]
    empBankNum = int(res[4][2:-2])
    return render_template("edit_employee.html", empid=empid, emp_name=empName, emp_addr=empAddr, emp_city=empCity, emp_bank_name=empBankName, emp_bank_num=empBankNum)


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

@app.route('/schedule_generator', methods=["POST"])
def schedule_generator():
     print("In schedule generator")
     empName = request.form['empName']
     week_id = int(request.form['weekID'])
     if empName == None or empName =="":
         employee_name = "Invalid_EMPID"
     else:
         employee_name = empName

     print("After selecting name: " + employee_name)

     schedule = GenSched.generate_html(week_id, employee_name)

     return render_template("schedule_shell.html", html=schedule, empName=employee_name)

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
    return render_template("document.html", empid=empid, message="")

@app.route('/get_a_document', methods=["POST"])
def get_a_document():
    print("Getting a document")
    objId = request.form['ObjectID']
    print(objId)
    fInfo = mongoDB.fs.files.find_one({"_id": ObjectId(objId)})
    print(fInfo['filename'])
    f = fs.get(ObjectId(objId))
    resp = make_response(f.read())
    resp.headers['Content-Type'] = 'application/pdf'
    resp.headers['Content-Disposition'] = "attachment; filename={}".format(fInfo['filename'])
    print("Got file")
    return resp

@app.route('/delete_document', methods=["POST"])
def delete_document():
    objId = request.form['ObjectID']
    empid = request.form['empid']
    fs.delete(ObjectId(objId))
    exists = fs.exists(ObjectId(objId))
    return render_template("document.html", empid=empid, message="File Deleted: " + str(not exists) )


@app.route('/change_preferences/<string:emp>')
def make_change_preference_page(emp):
    print("here make change pref page")
    empid = int(emp)
    prefs = employeefunctions.getEmpsPrefs(empid)
    print("return from get prefs call")
    print(prefs)
    return jsonify(prefs)

@app.route('/generate_new_schedules', methods=["POST"])
def generate_new_schedules():
    adminID = request.form['adminID']
    weekID = request.form['weekID']
    parameters.set_weekID(weekID)
    res = redis_connect.generate()
    #res = "hey"
    return render_template("admin_settings_page.html", empid=adminID, message=res)


@app.route('/change_preferences_page', methods=["POST"])
def change_preferences_page():
    #print("here change pref page")
    empid = int(request.form['empID'])
    return render_template("change_preferences.html", empid=empid, message="Hope this works")


@app.route('/save_preferences/<int:empid>/<string:prefs>')
def save_preferences(empid,prefs):
    vv = json.loads(prefs)
    for x in vv:
        print(x)
    #vv2 = str(vv).encode('ascii','ignore')
    vv2 = employeefunctions.getMonetConvertedVal(json.dumps(vv))
    query = "update employees1 set preferences = %s where empid = %d" % (vv2,empid)
    query = employeefunctions.changeQueryTable(query,empid)
    print(query)
    res = employeefunctions.executeEmpQuery(query,empid)
    print(res)
    return "here save prefs"


@app.route('/edit_wages_page',methods=["POST"])
def getEmpWage():
    adminID = request.form['adminID']
    return render_template("edit_wages.html", adminID=adminID)

@app.route('/edit_wage_submit',methods=["POST"])
def setEmpWage():
    adminid = int(request.form['adminID'])
    empid = int(request.form['empid'])
    wage = float(request.form['wage'])
    res = employeefunctions.updateWage(empid,wage)
    return render_template("admin_settings_page.html", empid=adminid, message=res)

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
