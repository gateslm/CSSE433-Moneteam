import redis

def get_connnect(hosts=["localhost"],ports=[6379]):
    if not len(hosts)==len(ports):
        raise Exception("Invalid number of hosts and number of imports")
    for i in range(0,len(hosts)):
        host = hosts[i]
        port = ports[i]
        try:
            # print host
            # print port
            conn= redis.Redis(host=host, port=port,password="moneteamPassword433")
            conn.get("currentWeekID")
            # print "connected to redis on "+str(host)
            return conn
        except redis.ConnectionError:
            # print "catch connection error"
            continue
    return None


def redisConn():

    hosts = ['moneteam-1.csse.rose-hulman.edu','moneteam-2.csse.rose-hulman.edu','moneteam-3.csse.rose-hulman.edu']
    ports = [6379,6379,6379]

    con = get_connnect(hosts,ports)
    if con == None:
        print "not connected"
    return con

    # pool = redis.ConnectionPool(host='localhost', port=6379)
    # conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379)
    # return conn

# redisConn()