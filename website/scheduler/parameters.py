import connections
import json
import ast
mc3 = connections.monetConn3()
curs3 = mc3.cursor()

week_id = 1
opening_time = 8
closing_time = 22
closing_time = 22
opening_hours = closing_time-opening_time
shift_diff = opening_hours/2-1
# bts = ["james","jone","jake","johnny"]
bts=[]
bt_salary = 7
ssv_salary = 14
# ssv = ["amy","emily",'erica','essabella']
ssv = []
minimal_server = 2
hours_limit_per_week = 45
hours_min_per_week = 35
n_days_limit = 5

duty_dict = {"manager":"x_ssv","bartender":"x_bts"}


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

