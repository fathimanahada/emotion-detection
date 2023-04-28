import mysql.connector

db=mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root123"
)

nw_cursor=db.cursor()
nw_cursor.execute("CREATE DATABASE testdb")
nw_cursor.excecute('''CREATE TABLE [IF NOT EXISTS] test(
   SI.NO INT AUTO_INCREMENT PRIMARY KEY,
   Name TEXT ,
   Dominant_emotion TEXT,
   Time TEXT
) ENGINE=INNODB;''')

db.commit()
db.close()