import redis

import pyomo
from pyomo.environ import *
from pyomo.opt import *
import re
import pandas as pd
from parameters import bts,ssv,get_current_weekID,week_id
print "try to generate week: "+str(week_id)

# week_id = get_current_weekID()

employees_involved = []

def save_employees(conn):
    key1 = "week"+str(week_id)+"_bts"
    key2 = "week"+str(week_id)+"_ssv"
    if conn.exists(key1):
        conn.delete(key1)
    if conn.exists(key2):
        conn.delete(key2)
    for bt in bts:
        conn.rpush(key1,bt)
        # print "store week bts"
    for s in ssv:
        conn.rpush(key2,s)
        # print "store week ssv"


def generate():

    import auto_scheduler as schedule
    raw = schedule.result
    raw_list = raw.split(";")
    ssv_clean = clean_text(raw_list,"x_ssv")
    bts_clean = clean_text(raw_list,"x_bts")

    try:
        conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
        delete_old(conn)
        upload_redis(bts_clean,conn)
        upload_redis(ssv_clean,conn)
        save_employees(conn)

    except redis.ConnectionError:
        print "redis cannot be connected"
        return "Sorry, redis server is currently unreachable, Please try again later"
    return "schedule has been generated successfully"

def clean_text(raw_list,key):
    gen_list = []
    for s in raw_list:
        if key in s:
            s=re.sub(key,"",s)
            s=re.sub("\[","",s)
            s=re.sub("\]","",s)
            info_list = s.split(",")
            if info_list[0] not in employees_involved:
                employees_involved.append(info_list[0])
            gen_list.append(info_list)
    return gen_list

def delete_old(conn):
    for name in employees_involved:
        for day in range(1,8):
            key= "week"+str(week_id)+"_day"+str(day)+"_"+name
            if conn.exists(key)==1:
             conn.delete(key)



def upload_redis(list,conn):
    # print "get run"
    # print employees_involved

    # delete_old()

    # for sublist in list:
    #     name = sublist[0]
    #     day = sublist[1]
    #     key= "week"+str(week_id)+"_day"+str(day)+"_"+name
    #     if conn.exists(key)==1:
    #         conn.delete(key)
    #         if conn.exists(key):
    #             print "key delete not sucess"
    #         # else:
    #         #     print "key delete succeed"
    #

    for sublist in list:
        name = sublist[0]
        day = sublist[1]
        hour = sublist[2]
        key= "week"+str(week_id)+"_day"+str(day)+"_"+name
        conn.rpush(key,hour)

if __name__ == "__main__":
    # conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    generate()

