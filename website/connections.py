import pymonetdb
import redis
import pymongo

#redisConn = redis.Redis()

def mongoConn():
    mongoConn = pymongo.MongoClient(['Amoneteam-1.csse.rose-hulman.edu:40001', 'Amoneteam-2.csse.rose-hulman.edu:40002', 'Amoneteam-3.csse.rose-hulman.edu:40003'], serverSelectionTimeoutMS=10000)
    cc = mongoConn.moneteam
    return cc

def monetConn1():
    monetConn = pymonetdb.connect(database = "moneteamdb1",
                                  username = 'monetdb',
                                  password = 'monetdb',
                                  port = 50001,
                                  hostname = "moneteam-1.csse.rose-hulman.edu")
    return monetConn

def monetConn2():
    monetConn = pymonetdb.connect(database = "moneteamdb2",
                                  username = 'monetdb',
                                  password = 'monetdb',
                                  port = 50002,
                                  hostname = "moneteam-2.csse.rose-hulman.edu")
    return monetConn

def monetConn3():
    monetConn = pymonetdb.connect(database = "moneteamdb3",
                                  username = 'monetdb',
                                  password = 'monetdb',
                                  port = 50003,
                                  hostname = "moneteam-3.csse.rose-hulman.edu")
    return monetConn
