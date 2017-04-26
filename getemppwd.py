import connections

mc = connections.monetConn()
cursor = mc.cursor()

def getpassword(empid):
    query = "select json.filter(password,\'password\') from employees "
    query += "where empid = %s;" % empid
    x = cursor.execute(query)
    print(x)
    print(cursor.fetchone())
    
getpassword(10)
