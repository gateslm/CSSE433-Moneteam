

import employeefunctions


def put_weeknum_into_monet(weeknum):
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    print("select filter weeknums count", count)
    print("res[0]", res[0])
    x = res[0]
    x.append(weeknum)
    y = {'vals': x}
    print(y)
    z = employeefunctions.getMonetConvertedVal(json.dumps(y))
    q2 = "update weeknumtable set weeknums = z;"
    conn3 = employeefunctions.getMC3()
    c2 = conn3.execute(q2)
    print("count of execute update", c2)
    return True


def get_weeknums_from_monet():
    q1  = "select json.filter(weeknums, \'vals\') from weeknumtable; "
    count, res = employeefunctions.executeEmpQueryCursorAll(q1)
    print("select filter weeknums count", count)
    print("returning", res[0])
    return res[0]




print(employeefunctions.getMonetConvertedVal({'vals':[1,2,3]}))
