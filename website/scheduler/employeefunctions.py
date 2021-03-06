import connections
import hashlib
import json
import pymonetdb
import ast


mc1 = connections.monetConn1()
mc2 = connections.monetConn2()
mc3 = connections.monetConn3()

#mcurs3 = mc3.cursor()


jsonattrs = ["password","address","workinfo","preferences","paymentinfo"]

#cursor = mc.cursor()


def insertEmp(empid,name,pwd,street,city,position,wage,banknum,bankname):
    print("Starting to insert emp")
    if checkIfEmpExists(empid):
        print("An employee with this empID already exists. Exiting. \n\n")
        return -1
    print("Emp not exist, now make query to insert emp")
    pwdhash = getPwdHash(pwd)
    idconvert = getMonetConvertedVal(empid)
    nameconvert = getMonetConvertedVal(name)
    passwordjson = getMonetConvertedVal(json.dumps({"password":pwdhash}))
    addressjson = getMonetConvertedVal(json.dumps({"city":city,"street":street}))
    positionjson = getMonetConvertedVal(json.dumps({"position":position,"wage":wage}))
    bankjson = getMonetConvertedVal(json.dumps({"bankname":bankname,"banknum":banknum}))
    query = "insert into employees1 "
    query = changeQueryTable(query,empid)
    query += "(empid, name, password, address, workinfo, preferences, paymentinfo) "
    query += "values ("
    # Empid, Name, Password
    query += "%s, %s, %s, " % (idconvert, nameconvert, passwordjson)
    # Address
    query += "%s, " % (addressjson)
    # Workinfo
    query += "%s, " % (positionjson)
    # Preferences
    preferences = json.dumps([{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}])
    preferencesjson = pymonetdb.sql.monetize.convert(preferences)
    query += "%s, " % (preferencesjson)
    # Paymentinfo
    query += "%s " % (bankjson)
    query += ");"
    print(query)

    x = executeEmpQuery(query, empid)
    print("Employee has been inserted")
    return 1


def executeEmpQuery(query, empid):
    if empid % 2 == 1:
        # Odd empIDs go to node 1
        x = mc1.execute(query)
        mc1.commit()
    else:
        # Even empIDs go to node 2
        x = mc2.execute(query)
        mc2.commit()
    return x

def executeEmpQueryCursor(query, empid):
    if empid % 2 == 1:
        # Odd empIDs go to node 1
        curs = mc1.cursor()
        x = curs.execute(query)
        y = curs.fetchall()
    else:
        # Even empIDs go to node 2
        curs = mc2.cursor()
        x = curs.execute(query)
        y = curs.fetchall()
    return x, y

def executeEmpQueryCursorAll(query):
    #print("started to exec query /cursor/ all")
    print('cursorALL query=', query)
    #c = mc3.cursor()
    c = mc3.cursor()
    x = c.execute(query)
    y = c.fetchall()
    global mc3
    mc3 = connections.monetConn3()
    return x, y


def checkIfEmpExists(empid):
    empid = int(empid)
    query = "Select count(*) from employees1 where empid = %d;" % empid
    query = changeQueryTable(query,empid)
    #if empid % 2 == 0:
        #query = "Select count(*) from employees2 where empid = %d;" % empid
    print(query)
    c, vals = executeEmpQueryCursor(query, empid)
    if vals[0][0] > 0:
        print("employee %d exists" % empid)
        return True
    print("employee %d does not exist" % empid)
    return False


def updateEmp(empid, pwd, attr, newVal):
    if not checkIfEmpExists(empid):
        return "An employee with this empID does not exist."
    query = "select password from employees where empid = %d;" % (empid)
    #query = changeQueryTable(query, empid)
    #if empid % 2 == 0:
        #query = "select password from employees2 where empid = %d;" % (empid)
    c, vals = executeEmpQueryCursor(query,empid)
    realPwd = repr(vals[0][0])[16:-3]
    #print(repr(vals[0][0])[16:-3])
    if realPwd != getPwdHash(pwd):
        print("Passwords do not match.")
        return -1

    newvalconvert = getMonetConvertedVal(newVal)
    #print(newvalconvert)
    query = "update employees1 set %s = %s where empid = %d;" % (attr, newvalconvert, empid)
    query = changeQueryTable(query, empid)
    executeEmpQuery(query,empid)

def getPwdHash(pwd):
    return hashlib.sha1(b"%s"%pwd).hexdigest()

def getMonetConvertedVal(val):
    return pymonetdb.sql.monetize.convert(val)

def changeQueryTable(query, empid):
    if empid % 2 == 0:
        return query.replace("1", "2", 1)
    return query

def getAllEmployees():
    query = "select * from employees;"
    cursor = mc3.cursor()
    x = cursor.execute(query)
    y = cursor.fetchall()

def checkIfPwdsMatch(empid, givenPwd):
    query = "select password from employees where empid = %d;" % (empid)
    c, vals = executeEmpQueryCursorAll(query)
    realPwd = repr(vals[0])[17:-5]
    if realPwd != getPwdHash(givenPwd):
        print("Passwords do not match.")
        return False
    return True
    
def getManagerPwds():
    query = "SELECT json.filter(password, \'password\') as pwd, "
    query += "json.filter(workinfo, \'position\') FROM employees "
    x, cursorResult = executeEmpQueryCursorAll(query)
    #cursor = mc3.cursor()
    #x = cursor.execute(query)
    #cursorResult = cursor.fetchall()
    pwds = []
    for y in cursorResult:
        if y[1] == '["manager"]':
            #print(y[0][2:-2])
            pwds.append(y[0][2:-2])
    return pwds

def getEmpsPrefs(empid):
    query = "select preferences from employees where empid = %d;" % empid
    c, vals = executeEmpQueryCursorAll(query)
    print('getEmpsPrefs query=', query)
    print('getEmpsPrefs return=', vals)
    pp = json.loads(vals[0][0])
    return pp

def changeEmpInfo(empid,name,addr,city,bank_name,bank_acct_num):
    nameconvert = getMonetConvertedVal(name)
    addressjson = getMonetConvertedVal(json.dumps({"city":city,"street":addr}))
    bankjson = getMonetConvertedVal(json.dumps({"bankname":bank_name,"banknum":bank_acct_num}))
    #print(addressjson)
    #print(bankjson)
    query1 = "update employees1 set name = %s where empid = %d" % (nameconvert, empid)
    query2 = "update employees1 set address = %s where empid = %d" % (addressjson, empid)
    query3 = "update employees1 set paymentinfo = %s where empid = %d" % (bankjson, empid)
    query1 = changeQueryTable(query1,empid)
    query2 = changeQueryTable(query2,empid)
    query3 = changeQueryTable(query3,empid)
    r1 = executeEmpQuery(query1,empid)
    r2 = executeEmpQuery(query2,empid)
    r3 = executeEmpQuery(query3,empid)
    #print(r1)
    #print(r2)
    #print(r3)
    return "edit successful"

def updateWage(empid,newWage):
    query1 = "select json.filter(workinfo,\'position\') from employees where empid = %d" % empid
    c, vals = executeEmpQueryCursorAll(query1)

    #print(vals[0][0][2:-2])
    job = vals[0][0][2:-2]
    
    workconvert = getMonetConvertedVal(json.dumps({"position":job,"wage":newWage}))
    query2 = "update employees1 set workinfo = %s where empid = %d" % (workconvert, empid)
    query2 = changeQueryTable(query2, empid)

    res = executeEmpQuery(query2,empid)
    #print(res)

def changePassword(empid,orgpass,newpass):
    if not checkIfEmpExists(empid):
        print("This empid is not valid.")
        return "EmpID is not valid."
    if not checkIfPwdsMatch(empid,orgpass):
        print("Old password is not valid.")
        return "Old password is not valid."

    newPwdHash = getPwdHash(newpass)
    pwdJSONconvert = getMonetConvertedVal(json.dumps({"password":newPwdHash}))
    q = "update employees1 set password = %s where empid = %d;" % (pwdJSONconvert, empid) 
    q = changeQueryTable(q,empid)
    x = executeEmpQuery(q,empid)
    return "Password change successfully."

def getMC3():
    return mc3

def getWage(empid):
    empid = int(empid)
    q = "select json.filter(workinfo, \'wage\') from employees "
    q += "where empid = %d;" % empid
    c, vals = executeEmpQueryCursorAll(q)
    #print(vals[0][0], type(vals[0][0]))
    res = ast.literal_eval(vals[0][0])[0]
    #print("returning ", res, type(res))
    return res


#getEmpsPrefs(101)
