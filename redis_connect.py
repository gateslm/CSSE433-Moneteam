import redis
import auto_scheduler as schedule
import pyomo
from pyomo.environ import *
from pyomo.opt import *
import re

def generate():
    raw = schedule.result
    raw_list = raw.split(";")
    # for r in raw_list:
    #     print r

    ssv_clean = clean_text(raw_list,"x_ssv")
    bts_clean = clean_text(raw_list,"x_bts")
    upload_redis(bts_clean)
    upload_redis(ssv_clean)

def clean_text(raw_list,key):
    gen_list = []
    for s in raw_list:
        if key in s:
            s=re.sub(key,"",s)
            s=re.sub("\[","",s)
            s=re.sub("\]","",s)
            info_list = s.split(",")
            gen_list.append(info_list)
    return gen_list

def upload_redis(list):
    for sublist in list:
        name = sublist[0]
        day = sublist[1]
        hour = sublist[2]
        key= "week"+str(week_id)+"_day"+str(day)+"_"+name
        conn.rpush(key,hour)

if __name__ == "__main__":
    conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    week_id = 1
    generate()

