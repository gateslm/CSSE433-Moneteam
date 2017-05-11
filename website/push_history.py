import employeefunctions

# from scheduler import mongo_connect
from connections import mongoConn
from scheduler import generate_schedule_html_table
from scheduler import redis_conn
from scheduler import parameters
from scheduler import redis_connect
import numpy as np
import pandas as pd
import json
import ast
from pymongo import errors


def get_redis_history(week_id,employee):
    conn = redis_conn.redisConn()
    schedule_raw = generate_schedule_html_table.import_schedule(employee,week_id,conn)
    schedule = np.transpose(schedule_raw)
    df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    opening_time = parameters.opening_time
    closing_time = parameters.closing_time
    df.index = range(opening_time,closing_time+1)
    return df


def import_history(week_id):
    # print "trying to import week: "+str(week_id)
    employees = parameters.get_current_employees(week_id)
    # print employees

    if len(employees) <1:
        return "the schedule for week "+str(week_id)+" is not generated yet, cannot be push to history"

    mongoClient = mongoConn()

    db = mongoClient['employee_history']

    # print("This is all employees: " + str(employees))
    
    for e in employees:
        df= get_redis_history(week_id,e)

        print df.empty
        key = str(e)+"_"+str(week_id)
        # print key
        doc = {"key":key,"schedule":df.to_json()}
        # print doc
        try:
            result = db.insert_one(doc)
            print("Import history insert_one result: " + str(result))
        except errors.ServerSelectionTimeoutError :
            put_weeknum_into_monet(week_id)
            return "Mongo is not availble right now, but the commands are stored to be executed later"

    # print "import work history done"
    return "all employees' working history for week "+str(week_id)+" should have been saved to mongo at this point"


    # print doc


def put_weeknum_into_monet(weeknum):
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    #print(res)
    #print(res[0])
    #print(res[0][0])
    aa = ast.literal_eval(res[0][0])[0]
    #print(aa)
    #print(type(aa))
    aa.append(weeknum)
    y = {'vals': aa}
    z = employeefunctions.getMonetConvertedVal(json.dumps(y))
    q2 = "update weeknumtable set weeknums = %s;" % z
    print("q2 = ", q2)
    conn3 = employeefunctions.getMC3()
    c2 = conn3.execute(q2)
    conn3.commit()
    print("count of execute update", c2)
    return True


def get_weeknums_from_monet():
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    # print("select filter weeknums count", count)
    # print("returning", res[0])
    return res[0]

def delete_weeknums_in_monet():
    data = {"vals": []}
    converted = employeefunctions.getMonetConvertedVal(json.dumps(data))
    q1  = "update weeknumtable set weeknums = %s" % converted
    conn3 = employeefunctions.getMC3()
    c1 = conn3.execute(q1)
    #print(c1)
    print(get_weeknums_from_monet())
    conn3.commit()




# print(employeefunctions.getMonetConvertedVal({'vals':[1,2,3]}))
# delete_weeknums_in_monet()
# put_weeknum_into_monet(99)
# put_weeknum_into_monet(98)
# put_weeknum_into_monet(97)
# put_weeknum_into_monet(1)
# put_weeknum_into_monet(2)
# put_weeknum_into_monet(3)
