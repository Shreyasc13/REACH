import sqlite3
con=sqlite3.connect('reach2.db')
cur=con.cursor()

cur.execute("PRAGMA TABLE_INFO('donor')")
 
