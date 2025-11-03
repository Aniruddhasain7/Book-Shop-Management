import pymysql as cntr
import datetime as __dt
import matplotlib.pyplot as plt
from random import shuffle
from tempfile import mktemp
from os import system, startfile

__db = cntr.connect(host='localhost', user='root', passwd='root', database='book_shop')
__cur = __db.cursor()
__db.autocommit(True)

is_leapyear = lambda year: year % 4 == 0

def last_month(month, year):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month == 2 and is_leapyear(year):
        return 29
    elif month == 2:
        return 28
    else:
        return 30

clrscreen = lambda: system("cls")

def view_stock():
    __cur.execute("SELECT Book_No, Book_Name, Available_Stock FROM stock")
    data = __cur.fetchall()
    print("Book Number\tBook Name\tStock")
    for row in data:
        print(row[0], '\t\t', row[1], '\t', row[2])

def add_stock():
    print('Add Stock'.center(89, '='))
    bno = unique_book_no()
    if bno:
        print("Book Number:", bno)
    else:
        bno = int(input("Enter book number: "))
    bname = input("Enter the Book's Name: ")
    auth = input("Enter the Author of the Book: ")
    publ = input("Enter the Publisher of the Book: ")
    cost = float(input("Enter the Cost per Book: "))
    stock = int(input("Enter the Quantity purchased: "))
    __cur.execute(
        "INSERT INTO stock VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (bno, bname, auth, publ, cost, stock, 0, __dt.date.today())
    )
    print("Inserted Successfully!!!")

def add_user():
    user = input("Enter the username: ")
    passwd = input("Enter a Password: ")
    passwd2 = input("Confirm Password: ")
    if passwd != passwd2:
        print("You've entered different passwords")
        return
    __cur.execute("SELECT * FROM users WHERE username = %s", (user,))
    if __cur.rowcount > 0:
        print("This username already exists. Please choose another one.")
        return
    __cur.execute("INSERT INTO users VALUES (%s, %s)", (user, passwd))
    print("User created successfully!")

def sell_book():
    print('Purchase')
    cname = input("Enter the Customer Name: ")
    phno = input("Enter the phone number: ")
    bno = int(input("Enter book number: "))
    bname = input("Enter the name of the book: ")
    cost = float(input("Enter the cost of the book: "))
    __cur.execute("INSERT INTO purchased VALUES (%s, %s)", (bno, __dt.date.today()))
    __cur.execute("UPDATE stock SET qty_purchased = qty_purchased + 1 WHERE Book_No = %s", (bno,))
    __cur.execute("UPDATE stock SET Available_Stock = Available_Stock - 1 WHERE Book_No = %s", (bno,))
    print("Bought Successfully")
    q = f'''Book Shop
Name : {cname}
Phone No : {phno}
Book Number : {bno}
Book Name : {bname}
Cost : {cost}
Date Of Purchase : {__dt.date.today()}'''
    filename = mktemp('.txt')
    open(filename, 'w').write(q)
    startfile(filename, 'print')
    __cur.execute("SELECT Book_Name, Book_No, Author FROM stock WHERE Available_Stock = 0")
    data = __cur.fetchall()
    if data:
        print("STOCK EXHAUSTED:")
        print("Book Name:", data[0][0])
        print("Book Number:", data[0][1])
        print("Author:", data[0][2])
        __cur.execute("DELETE FROM stock WHERE Available_Stock = 0")

def unique_book_no():
    __cur.execute("SELECT MAX(Book_No) FROM stock")
    data = __cur.fetchone()
    if data and data[0]:
        L1 = [x for x in range(data[0] + 1, data[0] + 10000)]
        shuffle(L1)
        return L1.pop(0)
    return False

def view_sales():
    print('Overall Sales This Month')
    __cur.execute(f"""
        SELECT DISTINCT(s.Book_Name), s.qty_purchased
        FROM stock s, purchased p
        WHERE s.Book_No = p.Book_No
        AND p.purchased_on BETWEEN
        '{__dt.date.today().year}-{__dt.date.today().month}-01' AND
        '{__dt.date.today().year}-{__dt.date.today().month}-{last_month(__dt.date.today().month, __dt.date.today().year)}'
    """)
    data = __cur.fetchall()
    if not data:
        print("No sales found for this month.")
        return
    L1, L2 = [], []
    for row in data:
        L1.append(row[0])
        L2.append(row[1])
    plt.bar(L1, L2)
    plt.xlabel('Books')
    plt.ylabel('Sales')
    plt.title('Sales')
    plt.show()

def login():
    user = input("Enter the username: ")
    pwd = input("Enter the password: ")
    __cur.execute("SELECT * FROM users WHERE username = %s", (user,))
    data = __cur.fetchone()
    if not data:
        print("No such user found.")
        return False
    elif data[1] != pwd:
        print("Incorrect password.")
        return False
    else:
        print(f"Welcome, {user}!")
        return True

def update_stock():
    bno = int(input("Enter the book number: "))
    __cur.execute("SELECT Book_Name, Available_Stock FROM stock WHERE Book_No = %s", (bno,))
    data = __cur.fetchone()
    if not data:
        print("Book not found.")
        return
    print("Book Name:", data[0])
    print("Available Stock:", data[1])
    stock = int(input("Enter the new stock purchased: "))
    __cur.execute("UPDATE stock SET Available_Stock = Available_Stock + %s WHERE Book_No = %s", (stock, bno))
    print("Updated Successfully")
