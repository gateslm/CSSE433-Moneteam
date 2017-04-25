import redis
import pandas as pd
import numpy as np
import re
# import auto_scheduler

def import_schedule(conn, name = "james", week_id = 1):
    gen_list = []
    for day in range(1,8):
        key= "week"+str(week_id)+"_day"+str(day)+"_"+name
        info = conn.lrange(key,0,-1)
        # for l in info:
        #     print int(l)
        #     print int(l) in range(opening_time,closing_time)
        tem_list=[]
        for i in range(opening_time,closing_time):
            if str(i) in info:
                tem_list.append(True)
            else:
                tem_list.append(False)
        gen_list.append(tem_list)
    return gen_list






if __name__ == "__main__":
    conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    week_id = 1
    employee_name = "james"

    # opening_time = auto_scheduler.openning_time
    # closing_time = auto_scheduler.closing_time

    opening_time =8
    closing_time = 22

    schedule = import_schedule(employee_name,week_id)
    schedule = np.transpose(schedule)
    df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    df.index = range(opening_time,closing_time)

    html_table = df.to_html()
    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)

    print html_table
