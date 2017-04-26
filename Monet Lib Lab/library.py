import pymonetdb
import monetdb.sql

def add_book(title,author, isbn, pages):
    insert_book_query = "INSERT INTO books (Authors, ISBN, Title, Pages) VALUES (%s, %s, %s, %s);" %(title,author ,isbn ,pages)
    print insert_book_query
    print cursor.execute(insert_book_query)

def init():
    create_books_table = "CREATE TABLE books(Authors Varchar(50), ISBN Varchar(50) not null, Title VARCHAR(20), Pages Int );"
    print(cursor.execute(create_books_table))


if __name__ == '__main__':
    # conn = pymonetdb.connect(database="library",username="monetdb", password="monetdb",hostname="moneteam-1.csse.rose-hulman.edu")
    # cursor = conn.cursor()

    conn = monetdb.sql.connect(database="library",username="monetdb", password="monetdb",hostname="moneteam-1.csse.rose-hulman.edu")
    cursor = conn.cursor()
    cursor.arraysize = 100

    # init()
    cursor.execute("INSERT INTO books (Authors, ISBN, Title, Pages) VALUES (database, prof, 1234, 89);")
    conn.commit()

    # print cursor.execute("select * from books;")

    # add_book("database","prof","1343",908)


