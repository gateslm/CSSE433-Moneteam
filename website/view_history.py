
from scheduler import mongo_connect
import pandas as pd
import re


def view_history(employee_name,week_id):
    key = str(employee_name)+"_"+str(week_id)
    mongoClient = mongo_connect.mongoConn()
    db = mongoClient['employee_history']

    cursor = db.find_one({"key":key})
    json_schedule = cursor['schedule']

    df = pd.read_json(json_schedule)
    html_table = df.to_html()

    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)

    return html_table


view_history(103,1)