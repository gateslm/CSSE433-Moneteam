import pymonetdb
conn = pymonetdb.connect(database = "moneteamdb2", username = "monetdb", password = "monetdb", hostname = "moneteam-2.csse.rose-hulman.edu")
print(conn)
#cursor = conn.cursor()
#print(cursor)
#print(cursor.execute("select * from voctable"))
#cursor.execute('drop table victortable;')
#
#conn.set_autocommit(True)
#x = conn.execute('create table victortable (id int, val varchar(20));')
#print(x)

y = conn.execute('insert into victortable (id, val) values (11, \'hey\'), (12, \'jameswashere\');')
print(y)

conn.commit()


#import pymonetdb
#conn = pymonetdb.connect(database="moneteamdb1", hostname="moneteam-1.csse.rose-hulman.edu")
#curs = conn.cursor()
#curs.execute("select * from testtable")
# -> 1 (num elements in query)
#curs.fetchone()
# -> (11, u'hey')
