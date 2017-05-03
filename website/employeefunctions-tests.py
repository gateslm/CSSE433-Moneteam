#insertEmp(101,"james","123","1323 magnolia drive","greenfield","manager",14.00,5678765,"PNC")
#insertEmp(102,"johnny","456","1324 database drive","terre haute","bartender",7.00,4499777,"Chase")
#insertEmp(103,"jone","789","1355 database drive","btown","bartender",7.00,4499449,"Chase")
#insertEmp(104,"jake","234","5533 database blvd","shanghai","bartender",7.00,1347878,"PNC")
#updateEmp(103,"789","name","jone2")

#insertEmp(105,"amy","1234","1337 macdonald drive","indianapolis","bartender",7.00,1234567,"BMO")
#insertEmp(106,"emily","4567","1399 wabash drive","terre haute","manager",14.00,1304120,"BMO")
#insertEmp(107,"erica","55555","5544 monet road","terre haute","manager",14.00,1345254,"Chase")
#insertEmp(108,"essabella","345","2345 monet road","shanghai","manager",14.00,5678998,"THSB")

#mc3.execute('select * from employees;')

#getAllEmployees()

#updateEmp(101, "123", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(102, "456", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(103, "789", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(104, "234", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(105, "1234", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(106, "4567", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(107, "55555", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')
#updateEmp(108, "345", "preferences", '[{"week_id": 1, "day": 1, "hour": 8}, {"week_id": 1, "day": 1, "hour" : 9}]')

#print(pymonetdb.sql.monetize.convert("hello"))
#print(pymonetdb.sql.monetize.convert(55))
#q = {"position": "manager", "wage": 14.00}
#print(q)
#print(json.dumps(q))
#print(pymonetdb.sql.monetize.convert(json.dumps(q)))

#checkIfPwdsMatch(101, "123")
#checkIfPwdsMatch(101, "134")
#pw = getManagerPwds()
#print pw
