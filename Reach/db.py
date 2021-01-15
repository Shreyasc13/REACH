import mysql.connector
import sqlite3

con = sqlite3.connect('reach2.db')
cur = con.cursor()

# mydb=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="!Ka19p9220",
#     auth_plugin='mysql_native_password',
#     database='reach',
# )

# cur=mydb.cursor()
# cur.execute("DROP DATABASE reach")
# cur.execute("CREATE DATABASE reach")
# cur.execute("USE reach;")

cur.execute("""CREATE TABLE donor(
    d_id integer AUTOINCREMENT,
    f_name text,
    l_name text,
    phone_no integer,
    password text,
    PRIMARY KEY(d_id)
)
""")
# text, integer,blob,real
cur.execute("""CREATE TABLE volunteer(
    v_id integer,
    f_name text,
    l_name text,
    phone_no integer,
    org_name text,
    org_location text,
    PRIMARY KEY(v_id)
)
""")


cur.execute("""CREATE TABLE food_order(
    f_id integer,
    d_id integer,
    food_type text,
    quantity integer,
    f_location text,
    PRIMARY KEY(f_id),
    FOREIGN KEY(d_id) REFERENCES donor(d_id)    
)
""")


cur.execute("""CREATE TABLE delivery_info(
    del_id integer,
    v_id integer,
    del_name text,
    del_location text,
    PRIMARY KEY(del_id),
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id)     
)
""")
cur.execute("""CREATE TABLE transactions(
    date_time integer,
    t_id integer,
    d_id integer,
    v_id integer,
    f_id integer,
    del_id integer,
    PRIMARY KEY(t_id),
    FOREIGN KEY(d_id) REFERENCES donor(d_id),
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id),
    FOREIGN KEY(f_id) REFERENCES food_order(f_id),
    FOREIGN KEY(del_id) REFERENCES delivery_info(del_id)
)
""")