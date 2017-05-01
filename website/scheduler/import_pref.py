
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
        this_pref = []
        y = ast.literal_eval(v[1])
        for x in y:
            print(x)
            x['empid'] = v[0]
            #print(y)
            preferences.append(x)
        #preferences.append(this_pref)

    #print(len(preferences))
    return preferences



#x = getAllPrefs()
#print("All preferences = \n\n")
#print(x)
