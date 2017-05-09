import redis

def redisConn():
    conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
    return conn