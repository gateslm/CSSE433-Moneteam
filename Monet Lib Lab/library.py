import pymonetdb
import monetdb.sql
import argparse

def add_book(title,author, isbn, pages):
    if has_book("ISBN",isbn):
        print "Book with ISBN-"+str(isbn)+" has already existed in the library"
        return
    insert_book_query = "INSERT INTO books (Authors, ISBN, Title, Pages) VALUES (\'%s\', \'%s\', \'%s\', \'%s\');" %(author ,isbn ,title,pages)
    conn.execute(insert_book_query)
    conn.commit()
    print "add book sucessfully"

def edit_book(book_isbn,property,newValue):
    if not has_book("ISBN",book_isbn):
        print "book trying to edit does not exist"
        return
    update_query = "UPDATE books SET %s = \'%s\' WHERE ISBN = \'%s\'" %(property, newValue, book_isbn)
    conn.execute(update_query)
    conn.commit()
    print "edit book successfully"

def has_borrower(property, value):
    has_query = "SELECT * FROM borrowers WHERE %s =\'%s\';" %(property,value)
    cursor = conn.cursor()
    cursor.execute(has_query)
    return len(cursor.fetchall()) > 0

def add_borrower(name, username, phone):
    if has_borrower("Username",username):
        print "borrower with username: "+str(username)+ " has already existed in the library system"
        return
    insert_borrower_query = "INSERT INTO borrowers (Name, Username, PhoneNumber) VALUES (\'%s\', \'%s\', \'%s\');" %(name,username,phone)
    conn.execute(insert_borrower_query)
    conn.commit()

def edit_borrower(username, Property, newValue):
    if not has_borrower("Username",username):
        print "borrower trying to edit does not exist"
        return
    update_query = "UPDATE borrowers SET %s = \'%s\' WHERE Username = \'%s\';" %(Property, newValue, username)
    conn.execute(update_query)
    conn.commit()


def delete_book(isbn):
    if not has_book("ISBN",isbn):
        print "book trying to delete does not exist"
        return
    delete_query = "DELETE FROM books WHERE ISBN = \'%s\';" %(isbn);
    conn.execute(delete_query)
    conn.commit()

def delete_borrower(username):
    if not has_borrower("Username".username):
        print "username trying to delete is not in the system"
        return
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
    if not has_borrower("Username",username):
        print "borrower does not exist"
        return
    if not has_book("ISBN",isbn):
        print "book does not exist"
        return
    borrow_query = "INSERT INTO borrow_list (Username,ISBN) VALUES (\'%s\', \'%s\');" %(username,isbn)
    conn.execute(borrow_query)
    conn.commit()
    print "borrower check out book successfully"


def borrower_has_book(username,isbn):
    cursor = conn.cursor()
    has_query = "SELECT * FROM borrow_list WHERE Username = \'%s\' AND ISBN = \'%s\';" %(username,isbn)
    cursor.execute(has_query)
    return len(cursor.fetchall()) >0


def borrower_return_book(username,isbn):
    if not has_borrower("Username",username):
        print "borrower does not exist"
        return
    if not has_book("ISBN",isbn):
        print "book does not exist"
        return
    return_query = "DELETE FROM borrow_list WHERE Username = \'%s\' AND ISBN = \'%s\';" %(username,isbn)
    conn.execute(return_query)
    conn.commit()


def get_borrower_checked_books(username):
    if not has_borrower("Username",username):
        print "borrower does not exist"
        return

    select_borrowed_book_query = "SELECT ISBN FROM borrow_list WHERE Username = \'%s\'; " %(username)
    cursor = conn.cursor()
    cursor.execute(select_borrowed_book_query)
    print "books checked by "+str(username)+": "+str(cursor.fetchall())

def check_requirement(list):
    checked = True
    if ("title" in list and args.title == None):
        print "     Please specific -title"
        checked = False
    if ("isbn" in list and args.isbn == None):
        print "     Please specific -isbn"
        checked = False
    if ("author" in list and args.author == None):
        print "     Please specific -author"
        checked = False
    if ("author" in list and args.pages == None):
        print "     Please specific -pages"
        checked = False
    if ("property" in list and args.property == None):
        print "     Please specific -property"
        checked = False
    if ("author" in list and args.pages == None):
        print "     Please specific -pages"
        checked = False
    if ("newValue" in list and args.newValue == None):
        print "     Please specific -newValue"
        checked = False
    if ("searchValue" in list and args.searchValue == None):
        print "     Please specific -searchValue"
        checked = False
    if ("bname" in list and args.bname == None):
        print "     Please specific -bname"
        checked = False
    if ("busername" in list and args.busername == None):
        print "     Please specific -busername"
        checked = False
    if ("bphone" in list and args.bphone == None):
        print "     Please specific -bphone"
        checked = False
    if ("attr" in list and args.attr == None):
        print "     Please specific -attr"
        checked = False
    return checked




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
    # sort_book_property("Pages")
    # print has_book("Pages","46")

    # borrower_checkout_book("jkr",1233)
    # borrower_checkout_book("jkr",1244)

    # borrower_return_book("jkr",1244)

    # get_borrower_checked_books("jkr")

    parser = argparse.ArgumentParser()
    parser.add_argument("-fn", help="specify called function")
    parser.add_argument("-isbn", help = "specify ISBN")
    parser.add_argument("-author", help = " specify author of the book", type = str, nargs = "+")
    parser.add_argument('-pages',help = "specify number of pages")
    parser.add_argument("-title",help = "specify book title")
    parser.add_argument("-property", help = "specify property for search or edit")
    parser.add_argument("-newValue", help = "specify new value")
    parser.add_argument("-searchValue",help="specify search value")
    parser.add_argument("-bname",help="specify borrower name")
    parser.add_argument("-bphone",help="specify borrower phone number")
    parser.add_argument("-busername",help="specify borrower username")
    parser.add_argument("-attr",help="specify attribute in a document")

    args = parser.parse_args()

    if args.fn == "add_book":
        if check_requirement(["title",'isbn','author','pages']):
            globals()[args.fn](args.title,args.isbn,args.author,args.pages)
    elif args.fn == "delete_book":
        if (check_requirement(["isbn"])):
            globals()[args.fn](args.isbn)
    elif args.fn =="edit_book":
        if (check_requirement(['isbn','property','newValue'])):
            globals()[args.fn](args.isbn,args.property,args.newValue)
    elif args.fn =="search_book":
        if (check_requirement(['property','searchValue'])):
            globals()[args.fn](args.property,args.searchValue)
    elif args.fn == "sort_book_property":
        if check_requirement(['property']):
            globals()[args.fn](args.property)
    elif args.fn == "add_borrower":
        if check_requirement(['bname','busername','bphone']):
            globals()[args.fn](args.bname,args.busername,args.bphone)
    elif args.fn == "delete_borrower":
        if check_requirement(['busername']):
            globals()[args.fn](args.busername)
    elif args.fn == "edit_borrower":
        if check_requirement(["busername","property","newValue"]):
            globals()[args.fn](args.busername,args.property,args.newValue)
    elif args.fn == "search_borrower":
        if check_requirement(["property",'searchValue']):
            globals()[args.fn](args.property,args.searchValue)
    elif args.fn == "borrower_checkout_book":
        if check_requirement(['busername','isbn']):
            globals()[args.fn](args.busername,args.isbn)
    elif args.fn == "get_borrower_checked_books":
        if check_requirement(["busername"]):
            globals()[args.fn](args.busername)
    elif args.fn == "borrower_return_book":
        if check_requirement(['busername','isbn']):
            globals()[args.fn](args.busername,args.isbn)
    elif args.fn == "get_book_checked_users":
        if check_requirement(['isbn']):
            globals()[args.fn](args.isbn)
    elif args.fn == "delete_attr":
        if check_requirement(['property','searchValue',"attr"]):
            globals()[args.fn](args.property,args.searchValue,args.attr)
    else:
        print "     Invalid Function"




