import connections
import hashlib


mc1 = connections.monetConn1()
mc2 = connections.monetConn2()
mc3 = connections.monetConn3()

#cursor = mc.cursor()


def insertEmp(empid,name,pwd,street,city,position,wage,banknum,bankname):
    query = "insert into employees "
    query += "(empid, name, password, address, workinfo, preferences, paymentinfo) "
    query += "values ("
    # Empid, Name, Password
    pwdhash = hashlib.sha1(b"%s"%pwd).hexdigest()
    query += '%d, \'%s\', \'{\"password\": \"%s\"}\',' % (empid, name, pwdhash)
    # Address
    query += '\'{\"city\": \"%s\", \"street\": \"%s\"}\',' % (city, street)
    # Workinfo
    query += '\'{\"position\": \"%s\", \"wage\": \"%f\"}\',' % (position, wage)
    # Preferences
    query += '\'{\"monday_morning\": \"1\", \"tuesday_evening\": \"1\"}\','
    # Paymentinfo
    query += '\'{\"bankname\": \"%s\", \"bankaccountnum\": \"%d\"}\'' % (bankname, banknum)


    query += ");"
    print(query)
    if empid % 2 == 1:
        # Odd empIDs go to node 1
        x = mc1.execute(query)
        mc1.commit()
    else:
        # Even empIDs go to node 2
        x = mc2.execute(query)
        mc2.commit()

    print(x)

insertEmp(10,"james","123","1323 magnolia drive","greenfield","manager",14.00,5678765,"PNC")

mc3.execute('select * from employees;')
#insertEmp(12,"johnny","456","1324 database drive","terre haute","bartender",7.00,4499777,"Chase")
#insertEmp(13,"jone","789","1355 database drive","btown","bartender",7.00,4499449,"Chase")
#insertEmp(14,"jake","234","5533 database blvd","shanghai","bartender",7.00,1347878,"PNC")

#insertEmp(15,"amy","1234","1337 macdonald drive","indianapolis","bartender",7.00,1234567,"BMO")
#insertEmp(16,"emily","4567","1399 wabash drive","terre haute","manager",14.00,1304120,"BMO")
#insertEmp(17,"erica","55555","5544 monet road","terre haute","manager",14.00,1345254,"Chase")
#insertEmp(18,"essabella","345","2345 monet road","shanghai","manager",14.00,5678998,"THSB")


