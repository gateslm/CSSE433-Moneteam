
from scheduler import mongo_connect
import pandas as pd
import re
from push_history import import_history,get_weeknums_from_monet


def view_history(employee_name,week_id):
    unprocessed_weeks = get_weeknums_from_monet()
    # print "those are unprocessed weeks: "
    # print unprocessed_weeks
    # print unprocessed_weeks[0]
    raw_weeks = str(unprocessed_weeks[0]).replace("[","").replace("]","")
    weeks = raw_weeks.split(",")
    for week in weeks:
         import_history(int(week))

    # print weeks


    key = str(employee_name)+"_"+str(week_id)
    mongoClient = mongo_connect.mongoConn()
    db = mongoClient['employee_history']

    cursor = db.find_one({"key":key})
    json_schedule = cursor['schedule']

    df = pd.read_json(json_schedule)
    html_table = df.to_html()

    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)

    # print df
    return html_table


view_history(101,1)