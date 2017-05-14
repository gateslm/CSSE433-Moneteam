import redis
import pandas as pd
import numpy as np
import re
from parameters import opening_time, closing_time, check_employee_consistent


def import_schedule(name , week_id , conn):
    # conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    gen_list = []

    for day in range(1,8):
        key= "week"+str(week_id)+"_day"+str(day)+"_"+name
        info = conn.lrange(key,0,-1)
        tem_list=[]
        for i in range(opening_time,closing_time+1):
            if str(i) in info:
                tem_list.append(True)
            else:
                tem_list.append(False)
        gen_list.append(tem_list)
    return gen_list

def generate_html(week_id, employee_name):

    ### check week_id in MonetDB

    ## Todo: generate new schedule if there is weekID in monetDB

    if not check_employee_consistent(week_id):
        print "schedule is inconsistent, generating new schedule now"
        from redis_connect import generate
        generate()

    try:
        conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
        schedule = import_schedule(employee_name,week_id,conn)
        print "connected to monteam-1"
    except redis.ConnectionError:
        # print "connection to moneteam-1 failed, trying moneteam-2 now"
        # try:
        #     conn = redis.Redis(host='moneteam-2.csse.rose-hulman.edu', port=6379);
        #     schedule = import_schedule(employee_name,week_id,conn)
        #     print "connected to monteam-2"
        # except redis.ConnectionError:
        #     try:
        #         conn = redis.Redis(host='moneteam-3.csse.rose-hulman.edu', port=6379);
        #         schedule = import_schedule(employee_name,week_id,conn)
        #         print "connected to monteam-3"
        #     except redis.ConnectionError:
        #         # target = open("schedule.html","w+")
        #         # target.write("<b> Sorry, redis server is currently unreachable, Please try again later </b>")
        #         # target.close
        return "<b> Sorry, redis server is currently unreachable, Please try again later </b>"

    schedule = np.transpose(schedule)
    df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

    df.index = range(opening_time,closing_time+1)

    # print df

    html_table = df.to_html()
    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)
    return html_table

    # target = open("schedule.html","w+")
    # target.write(html_table)
    # target.close()





if __name__ == "__main__":
    generate_html(1,"101")



