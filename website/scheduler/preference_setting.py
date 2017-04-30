from import_pref import getPrefs

preferences = getPrefs()

def add_pref(var,name,day,hour,count):
    string = ""
    string+="def conn_pref_"+str(count)+"(model):\n"
    string+="\t return model."+str(var)+ "['"+str(name)+"'," +str(day)+","+str(hour)+"] <=0 \n"
    string+="model.con_"+str(count)+" = Constraint(rule =conn_pref_"+str(count)+")"

    return string

if __name__ == '__main__':
    print add_pref("x_bts","james",1,9,1)
