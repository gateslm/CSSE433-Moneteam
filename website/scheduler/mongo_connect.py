import pymongo
import redis
from generate_schedule_html_table import import_schedule
import numpy as np
from parameters import opening_time,closing_time
import pandas as pd

def mongoConn():
    mongoConn = pymongo.MongoClient(['moneteam-1.csse.rose-hulman.edu:40001', 'moneteam-2.csse.  rose-hulman.edu:40002', 'moneteam-3.csse.rose-hulman.edu:40003'])
    cc = mongoConn.moneteam
    return cc

# def store_work_history(week_id):
#     conn = mongoConn()
#     try:
#         conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
#     except redis.ConnectionError:
#         return "redis is unavailable now"
#     key1 = "week"+str(week_id)+"_bts"
#     key2 = "week"+str(week_id)+"_ssv"
#     bts = conn.lrange(key1,0,-1)
#     ssv = conn.lrange(key2,0,-1)
#
#     b = bts[0]
#     schedule = import_schedule(b,week_id,conn)
#     schedule = np.transpose(schedule)
#     df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
#
#     df.index = range(opening_time,closing_time+1)
#     print df.to_json()

# store_work_history(2)
    
    




