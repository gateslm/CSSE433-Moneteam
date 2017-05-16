
# from scheduler import mongo_connect
from scheduler import connections
from scheduler import employeefunctions
import pandas as pd
import numpy as np
import re
from push_history import import_history,get_weeknums_from_monet,delete_weeknums_in_monet


def view_history(employee_name,week_id):
    unprocessed_weeks = get_weeknums_from_monet()
    # print "those are unprocessed weeks: "
    # print unprocessed_weeks
    # print unprocessed_weeks[0]
    raw_weeks = str(unprocessed_weeks[0]).replace("[","").replace("]","")
    if not len(raw_weeks)<=0:
        weeks = raw_weeks.split(",")
        for week in weeks:
            print "process week: "+week+" now."
            import_history(int(week))
        delete_weeknums_in_monet()
        print "finished processing un_processed weeks"

    key = str(employee_name)+"_"+str(week_id)
    mongoClient = connections.mongoConn()
    db = mongoClient['employee_history']

    if db.find({"key":key}).count() <1:
        return "<b> week history not generated yet </b>"

    cursor = db.find_one({"key":key})


    # print "this is cursor size"
    # print cursor.count()

    json_schedule = cursor['schedule']

    df = pd.read_json(json_schedule)

    hours = np.sum(np.sum(df))
    wages = int(employeefunctions.getWage(employee_name))
    total_wages = hours*wages

    html_table = df.to_html()

    html_table = re.sub("False","",html_table)
    html_table = re.sub("True","&#10004",html_table)

    html_table += "<div> You have earned $"+"<strong>"+str(total_wages)+"</strong>"+" in this week </div>"

    # print df
    return html_table


#view_history(101,1)
