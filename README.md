# CSSE433-Moneteam
RHIT-Advanced Databases final project. Using multiple databases to create a scheduling assistant. 

## Purpose of the Project  
The purpose of the project is to expand our knowledge and work with NoSQL databases. By using multiple databases, we can learn how to utilize different types of NoSQL databases, spread data across multiple databases, and have polyglot persistence when a database goes down. To extend our knowledge, the databases needs to have an interface to help users navigate the data. 

## Databases and Tools Users

[Redis](https://redis.io/) - Key value store database and is able to be stored entirely in memory

[MongoDB](https://www.mongodb.com/) - Document store database

[MonetDB](https://www.monetdb.org/Home) - Columnar database with access in a SQL type language

[Flask](http://flask.pocoo.org/) - Microframwoerk for Python to create a server for a website

[Pandas](http://pandas.pydata.org/) - Python library providing high-performance, easy-to-use data structures and data analysis. 

[NumPy](http://www.numpy.org/) - Fundamental package for scientific computing in Python. 

[Pyomo](http://www.pyomo.org/) - A Python library for optimization modeling language with a diverse set of optimization capabilities. 

[GLPK](https://www.gnu.org/software/glpk/) - Package that is built for solving large-scale linear programming, mixed integer programming, and other related math problems. 

## Monet Setup

#### Set monetdb to certain ip address
`monetdbd set port=0.0.0.0 yourDataFarm/ `

#### create a database in monetdb
`monetdb create db`

#### release a database in monetdb 
`monetdb release db`
#### Examples of connecting to remote monetdb server through pymonetdb
```
import pymonetdb
conn = pymonetdb.connect()
cursor = conn.cursor()
cursor.execute("select * from voctable")
```

## Mongo Setup

#### Set mongoDB Replica Sets
```
rs.initiate()
rs.add("moneteam-X....:00000")

# set arbiter
rs.add("...",{arbiter:true})

# check heart beat
rs.status()

# allow read on secondary
rs.slaveOK()
```
mongod --fork --logpath
