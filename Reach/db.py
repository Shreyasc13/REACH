import sqlite3

conn = sqlite3.connect('reach2.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE donor(
    d_id INTEGER PRIMARY KEY AUTOINCREMENT,
    f_name text,
    l_name text,
    phone_no integer UNIQUE,
    password text NOT NULL
)
""")
# text, integer,blob,real
cur.execute("""CREATE TABLE volunteer(
    v_id integer PRIMARY KEY AUTOINCREMENT,
    f_name text,
    l_name text,
    phone_no integer UNIQUE,
    password text NOT NULL,
    org_name text,
    org_location text
)
""")


cur.execute("""CREATE TABLE food_order(
    f_id integer PRIMARY KEY AUTOINCREMENT,
    d_id integer,
    f_type text,
    f_name text,
    quantity integer,
    f_location text,
    pin_code integer,
    FOREIGN KEY(d_id) REFERENCES donor(d_id)    
)
""")


cur.execute("""CREATE TABLE delivery_info(
    del_id integer PRIMARY KEY AUTOINCREMENT,
    v_id integer,
    del_name text,
    del_location text,
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id)     
)
""")
cur.execute("""CREATE TABLE transactions(
    t_id integer PRIMARY KEY AUTOINCREMENT,
    date_time integer,
    d_id integer,
    v_id integer,
    f_id integer,
    del_id integer,
    FOREIGN KEY(d_id) REFERENCES donor(d_id),
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id),
    FOREIGN KEY(f_id) REFERENCES food_order(f_id),
    FOREIGN KEY(del_id) REFERENCES delivery_info(del_id)
)
""")