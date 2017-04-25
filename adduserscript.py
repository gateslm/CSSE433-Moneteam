import connections
import hashlib

mc = connections.monetConn()

cursor = mc.cursor()


def insertEmp(empid,name,pwd,street,city,position,wage,banknum,bankname):
    query = "insert into Employees "
    query += "(empid, name, password, address, workinfo, preferences, paymentinfo) "
    query += "values ("
    # Empid, Name, Password
    pwdhash = hashlib.sha1(b"%s"%pwd).hexdigest()
    query += "%d, \'%s\', \'{\"password\": \"%s\"}\'," % (empid, name, pwdhash)
    # Address
    query += "\'{\"city\": \"%s\", \"street\": \"%s\"}\'," % (city, street)
    # Workinfo
    query += "\'{\"position\": \"%s\", \"wage\": \"%f\"}\'," % (position, wage)
    # Preferences
    query += "\'{\"monday_morning\": \"1\", \"tuesday_evening\": \"1\"}\',"
    # Paymentinfo
    query += "\'{\"bankname\": \"%s\", \"bankaccountnum\": \"%d\"}\'" % (bankname, banknum)


    query += ");"
    #print(query)
    x = mc.execute(query)
    print(x)
    #y = cursor.commit()
    #print(y)
    #print(cursor.fetchone())
    #cursor.execute("Insert into Employees " + \
               #"\'{\"monday_morning\": \'1\', \"tuesday_evening\": \'1\'}\'" + \
               #"\'{\"bankaccount\": \'%d\', \"bankname\": \'%s\'});\'"
               #% (empid,name,pwd,city,street,position,wage,banknum,bankname))

insertEmp(11,"james","123","1323 magnolia drive","greenfield","manager",14.00,5678765,"PNC")

cursor.execute('select * from employees;')
print(cursor.fetchone())
#insertEmp(12,"johnny","456","1324 database drive","terre haute","bartender",7.00,4499777,"Chase")
#insertEmp(13,"jone","789","1355 database drive","btown","bartender",7.00,4499449,"Chase")
#insertEmp(14,"jake","234","5533 database blvd","shanghai","bartender",7.00,1347878,"PNC")

#insertEmp(15,"amy","1234","1337 macdonald drive","indianapolis","bartender",7.00,1234567,"BMO")
#insertEmp(16,"emily","4567","1399 wabash drive","terre haute","manager",14.00,1304120,"BMO")
#insertEmp(17,"erica","55555","5544 monet road","terre haute","manager",14.00,1345254,"Chase")
#insertEmp(18,"essabella","345","2345 monet road","shanghai","manager",14.00,5678998,"THSB")


