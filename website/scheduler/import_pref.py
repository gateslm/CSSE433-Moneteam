
import pymonetdb
import connections
import json
import ast

mc3 = connections.monetConn3()
curs3 = mc3.cursor()

def getAllPrefs():
    query = "Select empid, preferences from employees;"
    c = curs3.execute(query)
    print(c)
    print("\n\n")
    vals = curs3.fetchall()
    preferences = []
    for v in vals:
        y = ast.literal_eval(v[1])
        y['empid'] = v[0]
        #print(y)
        preferences.append(y)

    return preferences



#x = getAllPrefs()
#print("All preferences = \n\n")
#print(x)
