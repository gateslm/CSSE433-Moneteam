import employeefunctions

from scheduler import mongo_connect
from scheduler import generate_schedule_html_table
from scheduler import redis_conn
from scheduler import parameters
from scheduler import redis_connect
import numpy as np
import pandas as pd

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
    employees = parameters.get_current_employees(week_id)
    mongoClient = mongo_connect.mongoConn()

    db = mongoClient['employee_history']


    for e in employees:
        e = employees[0]
        df= get_redis_history(week_id,e,)
        key = str(e)+"_"+str(week_id)
        doc = {"key":key,"schedule":df.to_json()}
        db.insert_one(doc)
    # print doc






def put_weeknum_into_monet(weeknum):
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    print("select filter weeknums count", count)
    print("res[0]", res[0])
    x = res[0]
    x.append(weeknum)
    y = {'vals': x}
    print(y)
    z = employeefunctions.getMonetConvertedVal(json.dumps(y))
    q2 = "update weeknumtable set weeknums = z;"
    conn3 = employeefunctions.getMC3()
    c2 = conn3.execute(q2)
    print("count of execute update", c2)
    return True


def get_weeknums_from_monet():
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    print("select filter weeknums count", count)
    print("returning", res[0])
    return res[0]




# print(employeefunctions.getMonetConvertedVal({'vals':[1,2,3]}))
