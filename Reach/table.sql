PRAGMA TABLE_INFO('location');

-- ALTER TABLE delivery_info ADD COLUMN email TEXT;

-- drop TABLE volunteer;

-- DROP TABLE delivery_info;

-- CREATE TABLE delivery_info(
--     del_id integer PRIMARY KEY AUTOINCREMENT,
--     del_name text,
--     del_phone integer,
--     del_password text,
--     del_location text
-- );

-- ALTER TABLE food_order RENAME COLUMN satatus TO status;

-- UPDATE food_order SET status='1' where d_id='2';

-- CREATE TABLE volunteer(
--     v_id integer PRIMARY KEY AUTOINCREMENT,
--     f_name text,
--     l_name text,
--     phone_no integer UNIQUE,
--     password text NOT NULL,
--     org_name text,
--     org_location text,
--     email text);


-- CREATE TABLE delete_log(
--     f_id INTEGER,
--     d_id INTEGER,
--     f_type TEXT,
--     f_name TEXT,
--     quantity INTEGER,
--     f_location TEXT,
--     pin_code INTEGER,
--     status INTEGER
-- );


-- CREATE TABLE location(
--     pin_code integer PRIMARY KEY,
--     l_location text,
--     FOREIGN KEY(pin_code) REFERENCES food_order(pin_code),
--     FOREIGN KEY(l_location) REFERENCES food_order(f_location)
-- )


-- CREATE TABLE appoint(
--     del_id integer PRIMARY KEY,
--     v_id text,
--     FOREIGN KEY(del_id) REFERENCES delivery_info(del_id),
--     FOREIGN KEY(v_id) REFERENCES food_order(volunteer)
-- )
            
-- CREATE TRIGGER update_status AFTER INSERT ON transactions
-- BEGIN
--     UPDATE food_order SET status=0 WHERE f_id=new.f_id and d_id=new.d_id;
-- END

-- DROP trigger aft_delete;