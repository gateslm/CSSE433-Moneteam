import connections

monetConn = connections.monetConn()
#create table employees (empid int, name varchar(30) not null, address JSON, workinfo JSON, preferences JSON, paymentinfo JSON, primary key (empid) );
#Address -> street address: X, city: Y, state: Z, zip: 12345
#Workinfo -> position: X, wage: Y, startdate: 20170423
#Preferences -> monday_morning: 1, monday_evening: 0
#Paymentinfo -> bankaccount#: 1234567, bankname: PNC


def main():
    #mongoConn = conn.mongoConn()
    #redisConn = conn.redisConn()

    print("Welcome the StoreScheduler, by Moneteam.")
    command = ""
    while(True):
        command = raw_input("Scheduler>> ")
        command = command.lower()
        if (command == 'quit') or (command == 'exit'):
            break
        elif (command == 'help'):
            printhelp()
        else:
            handle(command)


def printhelp():
    print("To add an employee, type: \'add-emp <Name> <ID> <Age> <Wage>\'.")
    print("To get a list of employees, type: \'get-emp\'.")

def handle(command):
    args = command.split(" ")
    if args[0] == "add-emp":
        addEmp(args[1],args[2],args[3],args[4])
    elif args[0] == "get-emp":
        getEmp()

    else:
        printhelp()


def addEmp(name,empid,age,wage):
    cursor = monetConn.cursor()
    print("name=%s"%name)
    print("empid=%s"%empid)
    print("age=%s"%age)
    print("wage=%s"%wage)
    res = cursor.execute("insert into employee (name,empid,age,wage) values (\'%s\',%s,%s,%s);" % (name,empid,age,wage))
    if res == 1:
        print("The employee has been added.")

def getEmp():
    cursor = monetConn.cursor()
    cursor.execute("select * from employee")
    for x in cursor.fetchall():
        print(x) 


if __name__ == '__main__':
    main()
