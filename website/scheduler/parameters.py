import connections
import json
import redis
from redis_conn import redisConn
from redisweekidfunctions import redis_put_weeknum_into_monet

mc3 = connections.monetConn3()
curs3 = mc3.cursor()

# week_id = 1
opening_time = 8
closing_time = 22
closing_time = 22
opening_hours = closing_time-opening_time
shift_diff = opening_hours/2-1
bts=[]
bt_salary = 7
ssv_salary = 14
ssv = []
minimal_server = 2
hours_limit_per_week = 45
hours_min_per_week = 35
n_days_limit = 5

duty_dict = {"manager":"x_ssv","bartender":"x_bts"}

conn = redisConn()

def set_weekID(input):
    if conn == None:
        redis_put_weeknum_into_monet(input)
        print "redis is not connected for now, week_id is stored into monet"
        return False
    else:
        conn.set("currentWeekID",input)
        return True
    # print "week_ID is set to "+str(input)

# try:
#     conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
# except redis.ConnectionError:
#     print "redis is unreachable"

if not redisConn()==None:
    week_id = conn.get("currentWeekID")
# print "In parameter, week id is "+str(week_id)

def get_current_weekID():
    week_id = conn.get("currentWeekID")
    return week_id

def getAllemployee():
    query = "select empid, workinfo from employees;"
    c = curs3.execute(query)
    vals = curs3.fetchall()
    for v in vals:
        id = v[0]
        work_info = json.loads(v[1])
        position =  work_info['position']
        if duty_dict[position] == "x_ssv":
            ssv.append(str(id))
        elif duty_dict[position] == "x_bts":
            bts.append(str(id))
        else:
            print "unrecognized position"

getAllemployee()
print "there are current bar tenders:"
print bts


def get_current_employees(week_number):
    key1 = "week"+str(week_number)+"_bts"
    key2 = "week"+str(week_number)+"_ssv"
    try:
        conn = redisConn()
        if conn == None:
            return "False"
        tem_bts = conn.lrange(key1,0,-1)
        tem_ssv = conn.lrange(key2,0,-1)
        employees = []
        employees+=(tem_bts)
        employees+=(tem_ssv)
        return employees
    except redis.ConnectionError:
        print "redis is not connected"

def check_employee_consistent(week_number):
    current_employees = get_current_employees(week_number)
    # print current_employees
    # print bts
    # print ssv
    for b in bts:
        if b not in current_employees:
            return False
        current_employees.remove(b)
    for s in ssv:
        if s not in current_employees:
            return False
        current_employees.remove(s)
    return len(current_employees)==0



# print check_employee_consistent(1)

