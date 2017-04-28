import hashlib

def getpassword(empid, conn):
    query = "SELECT json.filter(password, \'password\') FROM employees "
    query += "where empid = %d;" % int(empid)
    cursor = conn.cursor()
    x = cursor.execute(query)
    if x != 1:
        return "User not found"
    else:
        cursorResult = cursor.fetchone()
        if isinstance(cursorResult, unicode):
            return cursorResult.encode('utf-8')
        else:
            return cursorResult

def getpasswordhash(pwd):
    return hashlib.sha1(b"%s" % pwd).hexdigest()

def getpasswordhashmgr(empid, conn):
    query = "SELECT json.filter(password, \'password\') FROM employees "
    query += "WHERE json.filter(workinfo, \'position\') = \'manager\';"
    cursor = conn.cursor()
    x = cursor.execute(query)
    if x != 1:
        return "User not found"
    else:
        cursorResult = cursor.fetchone()
        if isinstance(cursorResult, unicode):
            return cursorResult.encode('utf-8')
        else:
            return cursorResult        
