import redis
import pandas as pd
import numpy as np
import re
from parameters import opening_time, closing_time


def import_schedule(name = "james", week_id = 1):
    conn = redis.Redis(host='moneteam-1.csse.rose-hulman.edu', port=6379);
    gen_list = []

    for day in range(1,8):
        key= "week"+str(week_id)+"_day"+str(day)+"_"+name
        info = conn.lrange(key,0,-1)
        tem_list=[]
        for i in range(opening_time,closing_time):
            if str(i) in info:
                tem_list.append(True)
            else:
                tem_list.append(False)
        gen_list.append(tem_list)
    return gen_list

def generate_html(week_id, employee_name):

    schedule = import_schedule(employee_name,week_id)
    schedule = np.transpose(schedule)
    df = pd.DataFrame(schedule,columns = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    df.index = range(opening_time,closing_time)

    print df

    html_table = df.to_html()
    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)

    target = open("schedule.html","w+")
    target.write(html_table)
    target.close()





# if __name__ == "__main__":



