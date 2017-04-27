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
            return cursorResult[0]

def getpasswordhash(pwd):
    return hashlib.sha1(b"%s" % pwd).hexdigest()


