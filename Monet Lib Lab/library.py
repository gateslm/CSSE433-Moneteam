import pymonetdb
import monetdb.sql

def add_book(title,author, isbn, pages):
    insert_book_query = "INSERT INTO books (Authors, ISBN, Title, Pages) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');" %(author ,isbn ,title,pages)
    conn.execute(insert_book_query)
    conn.commit()

def edit_book(book_isbn,property,newValue):
    update_query = "UPDATE books SET %s = \'%s\' WHERE ISBN = \'%s\'" %(property, newValue, book_isbn)
    conn.execute(update_query)
    conn.commit()

def add_borrower(name, username, phone):
    insert_borrower_query = "INSERT INTO borrowers (Name, Username, PhoneNumber) VALUES (\'%s\', \'%s\', \'%s\');" %(name,username,phone)
    conn.execute(insert_borrower_query)
    conn.commit()

def edit_borrower(username, Property, newValue):
    update_query = "UPDATE borrowers SET %s = \'%s\' WHERE Username = \'%s\';" %(Property, newValue, username)
    conn.execute(update_query)
    conn.commit()


def delete_book(isbn):
    delete_query = "DELETE FROM books WHERE ISBN = \'%s\';" %(isbn);
    conn.execute(delete_query)
    conn.commit()

def delete_borrower(username):
    delete_query = "DELETE FROM borrowers WHERE Username = \'%s\';" %(username);
    conn.execute(delete_query)
    conn.commit()

def sort_book_property(property):
    sort_query = "SELECT * FROM books ORDER BY %s;" %(property)
    cursor = conn.cursor()
    cursor.execute(sort_query)
    print cursor.fetchall()


def has_book(property, value):
    has_query = "SELECT * FROM books WHERE %s =\'%s\';" %(property,value)
    cursor = conn.cursor()
    cursor.execute(has_query)
    return len(cursor.fetchall()) > 0

def borrower_checkout_book(username,isbn):
    borrow_query = "INSERT INTO borrow_list (Username,ISBN) VALUES (\'%s\', \'%s\');" %(username,isbn)
    conn.execute(borrow_query)
    conn.commit()


def borrower_has_book(username,isbn):
    cursor = conn.cursor()
    has_query = "SELECT * FROM borrow_list WHERE Username = \'%s\' AND ISBN = \'%s\';" %(username,isbn)
    cursor.execute(has_query)
    return len(cursor.fetchall()) >0


def borrower_return_book(username,isbn):
    return_query = "DELETE FROM borrow_list WHERE Username = \'%s\' AND ISBN = \'%s\';" %(username,isbn)
    conn.execute(return_query)
    conn.commit()


def get_borrower_checked_books(username):
    select_borrowed_book_query = "SELECT ISBN FROM borrow_list WHERE Username = \'%s\'; " %(username)
    cursor = conn.cursor()
    cursor.execute(select_borrowed_book_query)
    print "books checked by "+str(username)+": "+str(cursor.fetchall())




def init():
    create_books_table = "CREATE TABLE books(Authors Varchar(50), ISBN Varchar(50) not null, Title VARCHAR(20), Pages VARCHAR(10) );"
    create_borrowers_table = "CREATE TABLE borrowers(Name Varchar(50), Username Varchar(50) not null, PhoneNumber VARCHAR(20));"
    create_borrowlist_table = "CREATE TABLE borrow_list(Username Varchar(50), ISBN Varchar(50));"
    conn.execute(create_books_table)
    conn.execute(create_borrowers_table)
    conn.execute(create_borrowlist_table)
    conn.commit()


if __name__ == '__main__':
    # conn = pymonetdb.connect(database="library",username="monetdb", password="monetdb",hostname="moneteam-1.csse.rose-hulman.edu")
    # cursor = conn.cursor()

    conn = monetdb.sql.connect(database="library",username="monetdb", password="monetdb",hostname="moneteam-1.csse.rose-hulman.edu")

    # init()
    # add_book("book title1","prof2",1233,46)
    # add_book("book title1","prof1",1244,99)
    # edit_book(1233,'Title',"edited_title")
    # add_borrower("james","jkr","8798")
    # edit_borrower("jkr","PhoneNumber","987235")
    # delete_book(1233)
    # delete_borrower("jkr")
    sort_book_property("Pages")
    print has_book("Pages","46")

    # borrower_checkout_book("jkr",1233)
    # borrower_checkout_book("jkr",1244)

    borrower_return_book("jkr",1244)

    get_borrower_checked_books("jkr")




