import employeefunctions
import ast
import json

def redis_put_weeknum_into_monet(weeknum):
    q1  = "select json.filter(weekids, \'vals\') from redisweekids; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    aa = ast.literal_eval(res[0][0])[0]
    #print(aa)
    aa.append(weeknum)
    y = {'vals': aa}
    z = employeefunctions.getMonetConvertedVal(json.dumps(y))
    q2 = "update redisweekids set weekids = %s;" % z
    #print("q2 = ", q2)
    conn3 = employeefunctions.getMC3()
    c2 = conn3.execute(q2)
    conn3.commit()
    #print("count of execute update", c2)
    return True


def redis_get_weeknums_from_monet():
    q1  = "select json.filter(weekids, \'vals\') from redisweekids; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    #print(res)
    #print(count)
    # print("select filter weeknums count", count)
    print("redis get weeknums returning", res[0], type(res[0]))
    return res[0]

def redis_delete_weeknums_in_monet():
    data = {"vals": []}
    converted = employeefunctions.getMonetConvertedVal(json.dumps(data))
    q1  = "update redisweekids set weekids = %s" % converted
    conn3 = employeefunctions.getMC3()
    c1 = conn3.execute(q1)
    #print(c1)
    #print(redis_get_weeknums_from_monet())
    conn3.commit()
