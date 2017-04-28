import connections
import hashlib
import json
import pymonetdb


mc1 = connections.monetConn1()
mc2 = connections.monetConn2()
mc3 = connections.monetConn3()

#cursor = mc.cursor()


def insertEmp(empid,name,pwd,street,city,position,wage,banknum,bankname):
    if checkIfEmpExists(empid):
        return "An employee with this empID already exists."
    
    pwdhash = hashlib.sha1(b"%s"%pwd).hexdigest()
    passwordjson = pymonetdb.sql.monetize.convert({"password":pwdhash})
    addressjson = pymonetdb.sql.monetize.convert({"city":city,"street":street})
    positionjson = pymonetdb.sql.monetize.convert({"position":position,"wage":wage})
    bankjson = pymonetdb.sql.monetize.convert({"bankname":bankname,"banknum":banknum})
    query = "insert into employees "
    query += "(empid, name, password, address, workinfo, preferences, paymentinfo) "
    query += "values ("
    # Empid, Name, Password
    query += "%d, \'%s\', %s, " % (empid, name, passwordjson)
    # Address
    query += "%s, " % (addressjson)
    # Workinfo
    query += "%s, " % (positionjson)
    # Preferences
    preferences = {"monday_morning":0, "wednesday_evening":0}
    preferencesjson = pymonetdb.sql.monetize.convert(preferences)
    query += "%s, " % (positionjson)
    # Paymentinfo
    query += "%s, " % (bankjson)
    query += ");"
    print(query)

    x = executeEmpQuery(query, empid)
    print(x)


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


def checkIfEmpExists(empid):
    query = "Select count(*) from employees where empid = %d;" % empid
    x = executeEmpQuery(query, empid)
    if x > 0:
        return True
    return False


def updateEmp(empid, attr, newVal):
    if not checkIfEmpExists(empid):
        return "An employee with this empID does not exist."
    query = "update employees set %s = %s where empid = %d;" % (attr, newVal, empid)
    
    x = executeEmpQuery(query)
    print(x)


def getAllEmployees():
    query = "select * from employees;"
    cursor = mc3.cursor()
    x = cursor.execute(query)
    y = cursor.fetchall()
    print(x)
    print(y)
    


insertEmp(101,"james","123","1323 magnolia drive","greenfield","manager",14.00,5678765,"PNC")
'''
insertEmp(102,"johnny","456","1324 database drive","terre haute","bartender",7.00,4499777,"Chase")
insertEmp(103,"jone","789","1355 database drive","btown","bartender",7.00,4499449,"Chase")
insertEmp(104,"jake","234","5533 database blvd","shanghai","bartender",7.00,1347878,"PNC")

insertEmp(105,"amy","1234","1337 macdonald drive","indianapolis","bartender",7.00,1234567,"BMO")
insertEmp(106,"emily","4567","1399 wabash drive","terre haute","manager",14.00,1304120,"BMO")
insertEmp(107,"erica","55555","5544 monet road","terre haute","manager",14.00,1345254,"Chase")
insertEmp(108,"essabella","345","2345 monet road","shanghai","manager",14.00,5678998,"THSB")

mc3.execute('select * from employees;')
'''
#getAllEmployees()

#print(pymonetdb.sql.monetize.convert("hello"))
#print(pymonetdb.sql.monetize.convert(55))
#q = {"position": "manager", "wage": 14.00}
#print(q)
#print(json.dumps(q))
#print(pymonetdb.sql.monetize.convert(json.dumps(q)))
