import pymysql as cntr

db = cntr.connect(host='localhost', user='root', passwd='root')
db.autocommit(True)
cur = db.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS book_shop")
cur.execute("USE book_shop")

cur.execute("""
CREATE TABLE IF NOT EXISTS stock (
    Book_No BIGINT PRIMARY KEY,
    Book_Name VARCHAR(255),
    Author VARCHAR(255),
    Publisher VARCHAR(255),
    Cost_per_Book FLOAT,
    Available_Stock BIGINT,
    qty_purchased BIGINT,
    purchased_on DATE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    CHECK (username <> 'ADMIN')
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS purchased (
    Book_No BIGINT,
    purchased_on DATE,
    FOREIGN KEY (Book_No) REFERENCES stock(Book_No)
)
""")

try:
    cur.execute("CREATE UNIQUE INDEX Book_Index ON stock(Book_No)")
except:
    pass


cur.execute("INSERT IGNORE INTO users VALUES ('admin', 'admin@123')")

print("Database and Tables created successfully!")
input("Press any key to continue---->")

cur.close()
db.close()
