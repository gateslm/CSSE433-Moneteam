import connections
import hashlib
import json
import pymonetdb


mc1 = connections.monetConn1()
mc2 = connections.monetConn2()
mc3 = connections.monetConn3()

jsonattrs = ["password","address","workinfo","preferences","paymentinfo"]

#cursor = mc.cursor()


def insertEmp(empid,name,pwd,street,city,position,wage,banknum,bankname):
    print("Starting to insert emp")
    if checkIfEmpExists(empid):
        print("An employee with this empID already exists. Exiting. \n\n")
        return 
    print("Emp not exist, now make query to insert emp")
    pwdhash = getPwdHash(pwd)
    print(pwdhash)
    idconvert = getMonetConvertedVal(empid)
    nameconvert = getMonetConvertedVal(name)
    passwordjson = getMonetConvertedVal(json.dumps({"password":pwdhash}))
    addressjson = getMonetConvertedVal(json.dumps({"city":city,"street":street}))
    positionjson = getMonetConvertedVal(json.dumps({"position":position,"wage":wage}))
    bankjson = getMonetConvertedVal(json.dumps({"bankname":bankname,"banknum":banknum}))
    query = "insert into employees1 "
    if empid % 2 == 0:
        query = "insert into employees2 "
    query += "(empid, name, password, address, workinfo, preferences, paymentinfo) "
    query += "values ("
    # Empid, Name, Password
    query += "%s, %s, %s, " % (idconvert, nameconvert, passwordjson)
    # Address
    query += "%s, " % (addressjson)
    # Workinfo
    query += "%s, " % (positionjson)
    # Preferences
    preferences = json.dumps({"monday_morning":0, "wednesday_evening":0})
    preferencesjson = pymonetdb.sql.monetize.convert(preferences)
    query += "%s, " % (preferencesjson)
    # Paymentinfo
    query += "%s " % (bankjson)
    query += ");"
    print(query)

    x = executeEmpQuery(query, empid)
    print(x)
    print("Employee has been inserted")


def executeEmpQuery(query, empid):
    print("started to exec query")
    if empid % 2 == 1:
        # Odd empIDs go to node 1
        x = mc1.execute(query)
        print("Mc1 execute result", x)
        mc1.commit()
    else:
        # Even empIDs go to node 2
        x = mc2.execute(query)
        print("Mc2 execute result", x)
        mc2.commit()
    print("returning from exec query")
    return x

def executeEmpQueryCursor(query, empid):
    print("started to exec query cursor")
    print(query)
    if empid % 2 == 1:
        # Odd empIDs go to node 1
        curs = mc1.cursor()
        print(curs)
        x = curs.execute(query)
        print("Mc1 cursor execute result", x)
    else:
        # Even empIDs go to node 2
        curs = mc2.cursor()
        print(curs)
        x = curs.execute(query)
        print("Mc2 cursor execute result", x)
    print("returning from exec query cursor")
    return x, curs.fetchall()


def checkIfEmpExists(empid):
    print("Start to check if emp exists")
    query = "Select count(*) from employees1 where empid = %d;" % empid
    if empid % 2 == 0:
        query = "Select count(*) from employees2 where empid = %d;" % empid
    print(query)
    c, vals = executeEmpQueryCursor(query, empid)
    print("check exists count", c)
    print(vals[0][0])
    print("executed check query")
    if vals[0][0] > 0:
        print("employee %d exists" % empid)
        return True
    print("employee %d does not exist" % empid)
    return False


def updateEmp(empid, pwd, attr, newVal):
    if not checkIfEmpExists(empid):
        return "An employee with this empID does not exist."
    query = "select password from employees1 where empid = %d;" % (empid)
    print("updating", query)
    realPwd = executeEmpQuery(query,empid)
    if realPwd !=  getPwdHash(pwd):
        print("Passwords do not match.") 
        return -1
    
    newvalconvert = getMonetConvertedVal(newVal)
    query = "update employees set %s = %s where empid = %d;" % (attr, empid)
    
def getPwdHash(pwd):
    return hashlib.sha1(b"%s"%pwd).hexdigest()

def getMonetConvertedVal(val):
    return pymonetdb.sql.monetize.convert(val)
    


def getAllEmployees():
    query = "select * from employees;"
    cursor = mc3.cursor()
    print(cursor)
    x = cursor.execute(query)
    y = cursor.fetchall()
    print('\n\n\n' + str(x) + '\n\n\n')
    print(y)
    


#insertEmp(101,"james","123","1323 magnolia drive","greenfield","manager",14.00,5678765,"PNC")
#insertEmp(102,"johnny","456","1324 database drive","terre haute","bartender",7.00,4499777,"Chase")
#insertEmp(103,"jone","789","1355 database drive","btown","bartender",7.00,4499449,"Chase")
#insertEmp(104,"jake","234","5533 database blvd","shanghai","bartender",7.00,1347878,"PNC")
#updateEmp(103,"789","name","jone2")

#insertEmp(105,"amy","1234","1337 macdonald drive","indianapolis","bartender",7.00,1234567,"BMO")
#insertEmp(106,"emily","4567","1399 wabash drive","terre haute","manager",14.00,1304120,"BMO")
#insertEmp(107,"erica","55555","5544 monet road","terre haute","manager",14.00,1345254,"Chase")
#insertEmp(108,"essabella","345","2345 monet road","shanghai","manager",14.00,5678998,"THSB")

#mc3.execute('select * from employees;')

getAllEmployees()

#print(pymonetdb.sql.monetize.convert("hello"))
#print(pymonetdb.sql.monetize.convert(55))
#q = {"position": "manager", "wage": 14.00}
#print(q)
#print(json.dumps(q))
#print(pymonetdb.sql.monetize.convert(json.dumps(q)))
