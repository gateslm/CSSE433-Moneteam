
import pymonetdb
import connections
import json
import ast
from parameters import duty_dict

mc3 = connections.monetConn3()
curs3 = mc3.cursor()

def getAllPrefs():
    query = "Select empid, preferences, workinfo from employees;"
    c = curs3.execute(query)
    # print(c)
    print("\n\n")
    vals = curs3.fetchall()
    preferences = []
    for v in vals:
        work_info = json.loads(v[2])
        position =  work_info['position']
        this_pref = []
        y = ast.literal_eval(v[1])
        for x in y:
            # print(x)
            x['empid'] = v[0]
            x['duty'] = position
            #print(y)
            preferences.append(x)
        #preferences.append(this_pref)

    return (preferences)

# getAllPrefs()


# x = getAllPrefs()
# print x
# print x
#print("All preferences = \n\n")
#print(x)
