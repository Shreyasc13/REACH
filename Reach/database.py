import mysql.connector


mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="!Ka19p9220",
    auth_plugin='mysql_native_password',
    database='reach',
)

cur=mydb.cursor()
cur.execute("DROP DATABASE reach")
cur.execute("CREATE DATABASE reach")
cur.execute("USE reach;")

cur.execute("""CREATE TABLE donor(
    d_id INT NOT NULL AUTO_INCREMENT,
    f_name VARCHAR(25),
    l_name VARCHAR(25),
    phone_no INT UNIQUE,
    password VARCHAR(25)  NOT NULL,
    PRIMARY KEY(d_id)
)
""")

cur.execute("""CREATE TABLE volunteer(
    v_id INT NOT NULL AUTO_INCREMENT,
    f_name VARCHAR(25),
    l_name VARCHAR(25),
    phone_no INT UNIQUE,
    password varchar(25)  NOT NULL,
    org_name VARCHAR(50),
    org_location VARCHAR(50),
    PRIMARY KEY(v_id)
)
""")


cur.execute("""CREATE TABLE food_order(
    f_id INT NOT NULL AUTO_INCREMENT,
    d_id INT,
    f_type VARCHAR(10),
    f_name VARCHAR(10),
    quantity INT,
    f_location VARCHAR(250),
    pin_code INT,
    PRIMARY KEY(f_id),
    FOREIGN KEY(d_id) REFERENCES donor(d_id)    
)
""")


cur.execute("""CREATE TABLE delivery_info(
    del_id INT NOT NULL AUTO_INCREMENT,
    v_id INT,
    del_name VARCHAR(20),
    del_location VARCHAR(30),
    PRIMARY KEY(del_id),
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id)     
)
""")
cur.execute("""CREATE TABLE transactions(
    date_time VARCHAR(20),
    t_id INT NOT NULL AUTO_INCREMENT,
    d_id INT,
    v_id INT,
    f_id INT,
    del_id INT,
    PRIMARY KEY(t_id),
    FOREIGN KEY(d_id) REFERENCES donor(d_id),
    FOREIGN KEY(v_id) REFERENCES volunteer(v_id),
    FOREIGN KEY(f_id) REFERENCES food_order(f_id),
    FOREIGN KEY(del_id) REFERENCES delivery_info(del_id)
)
""")