import pymongo
import redis

def mongoConn():
    mongoConn = pymongo.MongoClient(['moneteam-1.csse.rose-hulman.edu:40001', 'moneteam-2.csse.  rose-hulman.edu:40002', 'moneteam-3.csse.rose-hulman.edu:40003'])
    cc = mongoConn.moneteam
    return cc

def store_work_history(week_id):
    conn = mongoConn()
    try:
        conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
    except redis.ConnectionError:
        return "redis is unavailable now"
    key1 = "week"+str(week_id)+"_bts"
    key2 = "week"+str(week_id)+"_ssv"
    bts = conn.lrange(key1,0,-1)




